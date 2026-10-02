"""Load KB markdown docs and split them into chunks for indexing.

Doc id = leading number in the filename (e.g. "26 — Returns policy & window.md" -> "26").
Keep each chunk's doc id + title so retrieval and citations can name the source.
"""
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB_DIR = ROOT / "kb"


@dataclass
class Chunk:
    doc_id: str
    title: str
    text: str
    section: str = ""   # "" = whole doc / intro; otherwise the "## " heading

    @property
    def chunk_id(self) -> str:
        return f"{self.doc_id}#{self.section or 'main'}"


def load_docs(kb_dir: Path = KB_DIR) -> list[Chunk]:
    chunks: list[Chunk] = []
    for p in sorted(Path(kb_dir).glob("*.md")):
        doc_id = p.stem.split()[0]                          # leading number
        title = p.stem.split("—", 1)[-1].strip()            # "Returns policy & window"
        body = p.read_text(encoding="utf-8")
        for section, text in chunk(body):
            chunks.append(Chunk(doc_id, title, text, section))
    return chunks


def chunk(body: str) -> list[tuple[str, str]]:
    """Structure-aware split: drop the H1 (the title is embedded separately),
    then one chunk per "## " section. Docs without sections stay one chunk —
    policy docs are short, and splitting mid-list would separate a rule from
    its exceptions."""
    body = re.sub(r"^# .*\n?", "", body.strip(), count=1).strip()
    parts = re.split(r"^## +(.+)$", body, flags=re.M)
    out = []
    intro = parts[0].strip()
    if intro:
        out.append(("", intro))
    for heading, text in zip(parts[1::2], parts[2::2]):
        if text.strip():
            out.append((heading.strip(), text.strip()))
    return out


if __name__ == "__main__":
    cs = load_docs()
    print(f"{len(cs)} chunks from {len({c.doc_id for c in cs})} docs")
    for c in cs:
        print(f"  {c.chunk_id:<12} {c.title}  ({len(c.text)} chars)")
