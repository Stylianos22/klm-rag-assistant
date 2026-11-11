"""Reranker EXPERIMENT — a measurement to inform a decision (DL14), not the fix.

Bi-encoder (current pipeline) vs bi-encoder top-15 chunks -> cross-encoder rerank -> top-3 docs.
Scored exactly like run_eval.py; eval/queries.json, gold labels and top_k=3 are only read.
Nothing here is wired into retrieve.py.

Usage:  python src/rerank_experiment.py            # assumes the index exists
        python src/rerank_experiment.py --reindex  # rebuild it from KB/ first
"""
import math
import sys
import time

import torch
from sentence_transformers import CrossEncoder

from index import build_index, embed, get_collection
from ingest import ROOT
from retrieve import retrieve
from run_eval import load_queries

RERANKER = "cross-encoder/ms-marco-MiniLM-L-6-v2"
CANDIDATES = 15
RESULTS = ROOT / "eval" / "rerank_results.md"
SHOULD_REFUSE_STRICT = {"Q9", "Q10"}     # what run_eval.py requires to abstain
SHOULD_REFUSE_BRIEF = {"Q8", "Q9", "Q10"}  # all three out-of-KB queries (Q8 = live order data)


def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def passage(meta: dict, text: str) -> str:
    head = f"{meta['title']} — {meta['section']}" if meta["section"] else meta["title"]
    return f"{head}. {text}"


def rerank(query: str, ce: CrossEncoder, col, k: int) -> tuple[list[tuple[str, float]], float]:
    """Top-15 chunks from the bi-encoder, re-scored by the cross-encoder, best score per doc."""
    res = col.query(query_embeddings=embed([query]), n_results=min(CANDIDATES, col.count()),
                    include=["documents", "metadatas"])
    metas, texts = res["metadatas"][0], res["documents"][0]
    t0 = time.perf_counter()
    logits = ce.predict([(query, passage(m, t)) for m, t in zip(metas, texts)],
                        activation_fn=torch.nn.Identity())  # raw logits; sigmoid applied below
    ms = (time.perf_counter() - t0) * 1000
    best: dict[str, float] = {}
    for m, s in zip(metas, logits):
        best[m["doc_id"]] = max(best.get(m["doc_id"], -math.inf), float(s))
    return sorted(best.items(), key=lambda x: -x[1])[:k], ms


def gap(top: dict[str, float], refuse: set[str], answerable: list[str]) -> tuple:
    lo = min(answerable, key=lambda q: top[q])
    hi = max(refuse, key=lambda q: top[q])
    return lo, hi, top[lo] - top[hi]


def main():
    if "--reindex" in sys.argv:
        build_index()
    cfg = load_queries()
    k = cfg["scoring"]["top_k"]
    col = get_collection()
    ce = CrossEncoder(RERANKER)

    rows, bi_hits, ce_hits, bi_top, ce_top, timings = [], 0, 0, {}, {}, []
    answerable = [q["id"] for q in cfg["queries"] if q["gold"]]
    for q in cfg["queries"]:
        bi = retrieve(q["query"], k=k, threshold=0.0, col=col)       # current pipeline, abstain off
        ce_docs, ms = rerank(q["query"], ce, col, k)
        timings.append(ms)
        bi_top[q["id"]], ce_top[q["id"]] = bi.top_score, ce_docs[0][1]
        bi_ids, ce_ids = bi.doc_ids, [d for d, _ in ce_docs]
        bi_ok = ce_ok = None
        if q["gold"]:
            bi_ok = all(g in bi_ids for g in q["gold"])
            ce_ok = all(g in ce_ids for g in q["gold"])
            bi_hits += bi_ok
            ce_hits += ce_ok
        rows.append((q, bi, ce_docs, bi_ok, ce_ok))

    n = len(answerable)
    lines = []
    out = lines.append
    out(f"# Reranker experiment — bi-encoder vs cross-encoder rerank\n")
    out(f"Bi-encoder: all-MiniLM-L6-v2 (title+body, cosine), top-{k} docs — the current pipeline.  ")
    out(f"Reranked: same bi-encoder pulls the top {CANDIDATES} chunks -> `{RERANKER}` re-scores each "
        f"(query, \"title — section. text\") -> best score per doc -> top-{k}.  ")
    out("Frozen `eval/queries.json`, gold labels and top_k=3 unchanged. Hit = all gold docs in top 3. "
        "Not wired into the pipeline.\n")
    out("## Retrieval per query\n")
    out("| Query | Type | Gold | Bi-encoder top-3 (cosine) | | Reranked top-3 (logit) | |")
    out("|---|---|---|---|---|---|---|")
    mark = lambda ok: "—" if ok is None else ("✅ hit" if ok else "❌ miss")
    for q, bi, ce_docs, bi_ok, ce_ok in rows:
        bi_s = ", ".join(f"{h.doc_id} ({h.score:.2f})" for h in bi.hits)
        ce_s = ", ".join(f"{d} ({s:.2f})" for d, s in ce_docs)
        gold = ", ".join(q["gold"]) if q["gold"] else "—"
        out(f"| {q['id']} | {q['type']} | {gold} | {bi_s} | {mark(bi_ok)} | {ce_s} | {mark(ce_ok)} |")
    out(f"\n**Retrieval (6 answerable):** bi-encoder **{bi_hits}/{n} = {bi_hits / n:.0%}** · "
        f"reranked **{ce_hits}/{n} = {ce_hits / n:.0%}** · target >"
        f"{cfg['scoring']['retrieval_target']:.0%}\n")

    out("## Abstention — is there a separating gap?\n")
    out("Gap = lowest top-1 score among the answerable queries minus highest top-1 among the should-refuse "
        "queries. Positive = a single threshold can separate them. Cross-encoder logits are unbounded, so "
        "the gap is also shown after a sigmoid (0–1), the only scale where DL14's \"≥ 0.10\" is comparable "
        "to cosine.\n")
    out("| Should-refuse set | Signal | Lowest answerable | Highest should-refuse | Gap |")
    out("|---|---|---|---|---|")
    for label, refuse in [("Q8, Q9, Q10 (brief)", SHOULD_REFUSE_BRIEF), ("Q9, Q10 (run_eval)", SHOULD_REFUSE_STRICT)]:
        lo, hi, g = gap(bi_top, refuse, answerable)
        out(f"| {label} | cosine | {lo} {bi_top[lo]:.3f} | {hi} {bi_top[hi]:.3f} | **{g:+.3f}** |")
        lo, hi, g = gap(ce_top, refuse, answerable)
        out(f"| {label} | rerank logit | {lo} {ce_top[lo]:.2f} | {hi} {ce_top[hi]:.2f} | **{g:+.2f}** |")
        s_lo, s_hi = sigmoid(ce_top[lo]), sigmoid(ce_top[hi])
        out(f"| {label} | rerank sigmoid | {lo} {s_lo:.3f} | {hi} {s_hi:.3f} | **{s_lo - s_hi:+.3f}** |")
    out("\n**Top-1 score per query**\n")
    out("| Query | Cosine | Rerank logit | Rerank sigmoid |")
    out("|---|---|---|---|")
    for q in cfg["queries"]:
        i = q["id"]
        out(f"| {i} | {bi_top[i]:.3f} | {ce_top[i]:.2f} | {sigmoid(ce_top[i]):.3f} |")
    timings.sort()
    out(f"\n**Rerank latency (CPU, {CANDIDATES} pairs/query):** median {timings[len(timings) // 2]:.0f} ms, "
        f"max {timings[-1]:.0f} ms — excludes the one-off model load.\n")

    report = "\n".join(lines)
    RESULTS.write_text(report + "\n", encoding="utf-8")
    print(report)
    print(f"\nSaved to {RESULTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
