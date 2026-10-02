"""Top-3 cosine retrieval with an abstain threshold."""
from dataclasses import dataclass, field

from index import embed, get_collection

TOP_K = 3
ABSTAIN_THRESHOLD = 0.35  # re-tune once KB is ~51 docs
CANDIDATES = 15           # chunks pulled before de-duplicating to TOP_K docs


@dataclass
class Hit:
    doc_id: str
    title: str
    score: float          # cosine similarity of the doc's best chunk
    chunks: list[str] = field(default_factory=list)


@dataclass
class Result:
    query: str
    hits: list[Hit]
    abstain: bool

    @property
    def top_score(self) -> float:
        return self.hits[0].score if self.hits else 0.0

    @property
    def doc_ids(self) -> list[str]:
        return [h.doc_id for h in self.hits]


def retrieve(query: str, k: int = TOP_K, threshold: float = ABSTAIN_THRESHOLD, col=None) -> Result:
    """Return the top-k *documents* (a doc may have several chunks; it is
    ranked by its best one). Abstain if the best score is below threshold."""
    col = col or get_collection()
    res = col.query(query_embeddings=embed([query]),
                    n_results=min(CANDIDATES, col.count()),
                    include=["documents", "metadatas", "distances"])
    by_doc: dict[str, Hit] = {}
    for text, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        score = 1.0 - dist    # Chroma cosine distance -> similarity
        hit = by_doc.setdefault(meta["doc_id"], Hit(meta["doc_id"], meta["title"], score))
        hit.chunks.append(text)
    hits = sorted(by_doc.values(), key=lambda h: -h.score)[:k]
    abstain = not hits or hits[0].score < threshold
    return Result(query, hits, abstain)


if __name__ == "__main__":
    import sys
    r = retrieve(" ".join(sys.argv[1:]) or "How long do I have to return something?")
    print("ABSTAIN" if r.abstain else "ANSWER", f"(top {r.top_score:.3f})")
    for h in r.hits:
        print(f"  {h.doc_id}  {h.score:.3f}  {h.title}")
