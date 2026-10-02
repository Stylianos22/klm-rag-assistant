"""Run the 10 frozen queries and score retrieval; print a report.

Retrieval hit = gold doc(s) in top-3 (ALL golds for multi-doc queries).
Answer approval is a human judgement (correct + grounded + cited + right edge behaviour).

Usage:  python src/run_eval.py            # report at the configured threshold
        python src/run_eval.py --sweep    # show how each threshold would behave
        python src/run_eval.py --reindex  # rebuild the Chroma index from KB/ first
"""
import json
import sys

from index import build_index, get_collection
from ingest import ROOT
from retrieve import ABSTAIN_THRESHOLD, TOP_K, retrieve

# Queries the system must NOT answer from the KB (abstain / redirect).
MUST_ABSTAIN = {"out-of-kb-absent", "out-of-kb-domain"}


def load_queries(path=ROOT / "eval" / "queries.json") -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(threshold: float = ABSTAIN_THRESHOLD) -> dict:
    cfg = load_queries()
    col = get_collection()
    rows, hits, answerable, abstain_ok, abstain_total = [], 0, 0, 0, 0
    for q in cfg["queries"]:
        r = retrieve(q["query"], k=cfg["scoring"]["top_k"], threshold=threshold, col=col)
        if q["gold"]:
            answerable += 1
            ok = not r.abstain and all(g in r.doc_ids for g in q["gold"])
            hits += ok
            verdict = "HIT" if ok else ("MISS (abstained)" if r.abstain else "MISS")
        elif q["type"] in MUST_ABSTAIN:
            abstain_total += 1
            abstain_ok += r.abstain
            verdict = "abstain OK" if r.abstain else "RISK: would answer"
        else:
            verdict = "abstain" if r.abstain else "retrieved (judge at generation)"
        rows.append((q, r, verdict))
    return {"rows": rows, "hits": hits, "answerable": answerable,
            "abstain_ok": abstain_ok, "abstain_total": abstain_total, "cfg": cfg}


def report(threshold: float = ABSTAIN_THRESHOLD):
    out = run(threshold)
    print(f"\nRetrieval eval — top-{TOP_K}, abstain < {threshold}\n")
    print(f"{'id':<4} {'type':<26} {'gold':<10} {'top-3 (score)':<34} verdict")
    for q, r, verdict in out["rows"]:
        top = " ".join(f"{h.doc_id}({h.score:.2f})" for h in r.hits)
        gold = ",".join(q["gold"]) if q["gold"] else "-"
        print(f"{q['id']:<4} {q['type']:<26} {gold:<10} {top:<34} {verdict}")
    rate = out["hits"] / out["answerable"]
    target = out["cfg"]["scoring"]["retrieval_target"]
    print(f"\nRetrieval: {out['hits']}/{out['answerable']} = {rate:.0%}  "
          f"(target >{target:.0%}: {'PASS' if rate > target else 'FAIL'})")
    print(f"Out-of-KB abstain (Q9, Q10): {out['abstain_ok']}/{out['abstain_total']}")
    print("Q7 (clarify) and Q8 (live order data) are judged at the generation step.")


def sweep():
    """Margin check: the lowest answerable top score vs the highest out-of-KB one."""
    out = run(threshold=0.0)
    ans = [(q["id"], r.top_score) for q, r, _ in out["rows"] if q["gold"]]
    ook = [(q["id"], r.top_score) for q, r, _ in out["rows"] if q["type"] in MUST_ABSTAIN]
    lo = min(ans, key=lambda x: x[1])
    hi = max(ook, key=lambda x: x[1])
    print("\nTop-1 scores")
    for qid, s in sorted(ans + ook, key=lambda x: -x[1]):
        tag = "answerable" if (qid, s) in ans else "OUT-OF-KB"
        print(f"  {qid:<4} {s:.3f}  {tag}")
    print(f"\nLowest answerable: {lo[0]} {lo[1]:.3f}   Highest out-of-KB: {hi[0]} {hi[1]:.3f}")
    if lo[1] > hi[1]:
        mid = (lo[1] + hi[1]) / 2
        print(f"Separable. Gap = {lo[1] - hi[1]:.3f}; midpoint threshold = {mid:.3f}")
    else:
        print("NOT separable by a single threshold — some query will be wrong either way.")


if __name__ == "__main__":
    if "--reindex" in sys.argv:
        print(f"indexed {build_index().count()} chunks")
    else:
        get_collection()  # fail fast with a clear error if the index is missing
    sweep() if "--sweep" in sys.argv else report()
