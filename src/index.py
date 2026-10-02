"""Embed chunks (TITLE + body — the spike lesson) and store them in Chroma."""
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import ROOT, Chunk, load_docs

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR = ROOT / ".chroma"
COLLECTION = "northbound_kb"


@lru_cache(maxsize=1)
def model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed(texts: list[str]):
    return model().encode(texts, normalize_embeddings=True).tolist()


def embed_text(c: Chunk) -> str:
    # KEY LESSON from the spike: title + body (body-only = 67%, title+body = 100%).
    head = f"{c.title} — {c.section}" if c.section else c.title
    return f"{head}. {c.text}"


def build_index(chunks: list[Chunk] | None = None):
    """(Re)build the collection from scratch so it always mirrors KB/."""
    chunks = chunks if chunks is not None else load_docs()
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    col.add(
        ids=[c.chunk_id for c in chunks],
        embeddings=embed([embed_text(c) for c in chunks]),
        documents=[c.text for c in chunks],
        metadatas=[{"doc_id": c.doc_id, "title": c.title, "section": c.section} for c in chunks],
    )
    return col


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_collection(COLLECTION)


if __name__ == "__main__":
    col = build_index()
    print(f"indexed {col.count()} chunks into {CHROMA_DIR}")
