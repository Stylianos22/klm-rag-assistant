"""Generation step (Decision Log #15): answer ONLY from the top-3 retrieved docs,
cite every claim as [id], refuse with one fixed sentence, or ask one clarifying question.

Abstention lives here, not in retrieval (DL14): retrieve() runs with the score
gate off, so the model always sees the top-3 docs and decides itself.

The LLM call sits behind one swappable function, complete(system, user) -> str.
"""
import os
import re
import sys

from dotenv import load_dotenv

load_dotenv()

from ingest import KB_DIR  # noqa: E402
from retrieve import TOP_K, retrieve  # noqa: E402

# Pinned model + prompt = reproducible. claude-3-5-haiku-latest (the brief's pin) was
# retired on 2026-02-19 and now returns 404, so this is the current Haiku.
MODEL = "claude-haiku-5-5"
EFFORT = "medium"                        # Haiku 5.5's default, pinned explicitly
MAX_TOKENS = 4096
PRICE_IN, PRICE_OUT = 0.10, 0.50         # USD per 1M tokens (prompts < 100K tokens)

REFUSAL = "I don't have that information."
SYSTEM = (
    "You are Northbound's support assistant. Answer ONLY using the numbered policy "
    "documents provided. Cite every factual claim with its doc id in square brackets, "
    "e.g. [26]. If the documents don't contain the answer, reply exactly: "
    f"'{REFUSAL}' If the question is too vague to answer from them, ask one short "
    "clarifying question instead."
)


def _load_kb() -> dict[str, tuple[str, str]]:
    """doc id -> (title, full text without the H1)."""
    kb = {}
    for p in sorted(KB_DIR.glob("*.md")):
        body = re.sub(r"^# .*\n?", "", p.read_text(encoding="utf-8").strip(), count=1).strip()
        kb[p.stem.split()[0]] = (p.stem.split("—", 1)[-1].strip(), body)
    return kb


KB = _load_kb()

# --- the swappable LLM backend -------------------------------------------------
_client = None
last_usage = {"input_tokens": 0, "output_tokens": 0}   # filled by complete(); 0 for a local model


def complete(system: str, user: str) -> str:
    """One LLM call. Swap this function to change backend (e.g. a local model)."""
    global _client
    import anthropic
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    r = _client.messages.create(
        model=MODEL, max_tokens=MAX_TOKENS, system=system,
        output_config={"effort": EFFORT},
        messages=[{"role": "user", "content": user}],
    )
    last_usage.update(input_tokens=r.usage.input_tokens, output_tokens=r.usage.output_tokens)
    if r.stop_reason == "refusal":
        return REFUSAL
    return "".join(b.text for b in r.content if b.type == "text").strip()
# -------------------------------------------------------------------------------


_CITE = re.compile(r"\[(\d{1,3}(?:\s*,\s*\d{1,3})*)\]")


def parse_citations(text: str) -> list[str]:
    """[26], [16][17] and [16, 17] -> ids in order of first use. [7] maps to KB id "07"."""
    ids: list[str] = []
    for group in _CITE.findall(text):
        for raw in re.split(r"\s*,\s*", group):
            cid = raw.zfill(2) if raw.zfill(2) in KB else raw
            if cid not in ids:
                ids.append(cid)
    return ids


def build_user_message(query: str, doc_ids: list[str]) -> str:
    docs = "\n\n".join(f"[{d}] {KB[d][0]}: {KB[d][1]}" for d in doc_ids)
    return f"Policy documents:\n\n{docs}\n\nCustomer question: {query}"


def answer(query: str, col=None) -> dict:
    retrieved = retrieve(query, k=TOP_K, threshold=0.0, col=col).doc_ids
    text = complete(SYSTEM, build_user_message(query, retrieved))
    return {
        "answer": text,
        "cited_ids": parse_citations(text),
        "retrieved_ids": retrieved,
        "refused": text.replace("’", "'").startswith(REFUSAL),
        "usage": dict(last_usage),
    }


def cost_usd(usage: dict) -> float:
    return (usage["input_tokens"] * PRICE_IN + usage["output_tokens"] * PRICE_OUT) / 1e6


if __name__ == "__main__":
    r = answer(" ".join(sys.argv[1:]) or "How long do I have to return something?")
    print(r["answer"])
    print(f"\ncited {r['cited_ids']}  retrieved {r['retrieved_ids']}  refused={r['refused']}")
