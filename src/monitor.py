"""Grounding monitor (Decision Log #16): one run = generate + verify + faithfulness
over the 10 frozen queries, summarised as a grounding score tracked across runs.

Writes eval/monitor_latest.json (full result) and appends a summary row to
eval/monitor_runs.json, so the trend builds one real run at a time.
The frozen eval/queries.json and the RAG core are only read.

Usage:  python src/monitor.py
        (or the "Run monitor" button on the /monitor page, which calls main(progress=...))
"""
import json
from datetime import datetime

from faithfulness import check, config
from generate import KB, MODEL, answer, cost_usd
from index import get_collection
from ingest import ROOT
from run_eval import load_queries
from run_generation_eval import behaviour
from verify import verify

RUNS = ROOT / "eval" / "monitor_runs.json"
LATEST = ROOT / "eval" / "monitor_latest.json"
# PROVISIONAL: placeholder numbers pending teacher sign-off (DL16 C3), not a validated threshold.
TARGET = {"target": 95.0, "band_low": 93.0, "band_high": 97.0, "provisional": True,
          "note": "Placeholder pending teacher sign-off (DL16); not a validated threshold."}


def faithfulness_label(q: dict, r: dict, f: dict, edge_ok) -> tuple[str, str]:
    """(label, note) for the dashboard's Faithfulness column."""
    if r["refused"]:
        if q["gold"]:
            return "Wrongly refused", "Answerable question, but the assistant refused."
        return ("Correct refusal", "") if edge_ok is not False else ("Unexpected refusal", "")
    bad = [c for c in f["claims"] if c["supported"] is False]
    if bad:
        return "Unsupported claim detected", f"“{bad[0]['claim']}” — {bad[0]['reason']}" + (
            f" (+{len(bad) - 1} more)" if len(bad) > 1 else "")
    if not [c for c in f["claims"] if c["supported"] is not None]:
        return "No claims", "Clarifying question; nothing to verify." if q["type"].startswith("ambiguous") else ""
    if q["type"] == "out-of-kb-live-data" and edge_ok:
        return "Supported", "Redirected to tracking/account; no order status invented."
    return "Supported", ""


def main(progress=None, col=None) -> dict:
    """One monitor run. progress(step, total, label) is called as work completes
    (used by the web page's progress ring); returns the run summary."""
    cfg = load_queries()
    col = col or get_collection()
    rows = []
    queries = cfg["queries"]
    total = 2 * len(queries) + 1                   # answer + judge per question, then save
    tick = progress or (lambda *a: None)
    for i, q in enumerate(queries):
        tick(2 * i, total, f"{q['id']} · Generating the answer ({i + 1} of {len(queries)})")
        r = answer(q["query"], col=col)
        v = verify(r)
        tick(2 * i + 1, total, f"{q['id']} · Checking every claim against its sources ({i + 1} of {len(queries)})")
        f = check(r, question=q["query"])          # default judge (v2: sees the question)
        _, edge_ok = behaviour(q, r)
        label, note = faithfulness_label(q, r, f, edge_ok)
        judged = [c for c in f["claims"] if c["supported"] is not None]
        gen_cost, judge_cost = cost_usd(r["usage"]), cost_usd(f["usage"])
        rows.append({
            "id": q["id"], "type": q["type"], "question": q["query"],
            "answer": r["answer"], "refused": r["refused"],
            "retrieved_ids": r["retrieved_ids"], "cited_ids": r["cited_ids"],
            "sources": [{"id": d, "title": KB[d][0]} for d in r["cited_ids"] if d in KB],
            "citation_ok": v["citation_ok"], "citation_problems": v["problems"],
            "edge_behaviour_ok": edge_ok,
            "claims": f["claims"], "claims_judged": len(judged),
            "claims_supported": sum(c["supported"] for c in judged),
            "faithfulness": label, "faithfulness_note": note,
            "flagged": (not v["citation_ok"]) or label in ("Unsupported claim detected", "Wrongly refused",
                                                           "Unexpected refusal") or edge_ok is False,
            "cost_usd": {"generation": round(gen_cost, 6), "faithfulness": round(judge_cost, 6),
                         "total": round(gen_cost + judge_cost, 6)},
        })
        print(f"{q['id']:<4} {label:<28} claims {rows[-1]['claims_supported']}/{len(judged)}  "
              f"citations {'ok' if v['citation_ok'] else 'FAIL'}")

    answerable = [x for x in rows if x["type"].startswith("answerable")]
    supported = sum(x["claims_supported"] for x in answerable)
    judged = sum(x["claims_judged"] for x in answerable)
    grounding = round(100 * supported / judged, 1) if judged else None
    all_cites = [(x, d) for x in rows for d in x["cited_ids"]]
    valid_cites = sum(d in KB and d in x["retrieved_ids"] for x, d in all_cites)
    oos = [x for x in rows if x["type"].startswith("out-of-kb")]
    oos_ok = sum(bool(x["edge_behaviour_ok"]) for x in oos)
    gen_total = sum(x["cost_usd"]["generation"] for x in rows)
    all_total = sum(x["cost_usd"]["total"] for x in rows)

    tick(total - 1, total, "Scoring the run and saving it")
    runs = json.loads(RUNS.read_text(encoding="utf-8")) if RUNS.exists() else []
    now = datetime.now().isoformat(timespec="seconds")
    summary = {
        "run": len(runs) + 1, "timestamp": now,
        "grounding_score": grounding, "claims_supported": supported, "claims_judged": judged,
        "answers_grounded": sum(x["faithfulness"] == "Supported" for x in answerable), "answerable": len(answerable),
        "citations_valid": valid_cites, "citations_total": len(all_cites),
        "answers_citation_ok": sum(x["citation_ok"] for x in rows), "answers": len(rows),
        "out_of_scope_ok": oos_ok, "out_of_scope_total": len(oos),
        "avg_cost_generation_usd": round(gen_total / len(rows), 6),
        "avg_cost_total_usd": round(all_total / len(rows), 6),
        "kb_docs": len(KB), "model": MODEL, **{k: v for k, v in config().items() if k != "judge_model"},
    }
    runs.append(summary)
    RUNS.write_text(json.dumps(runs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LATEST.write_text(json.dumps({"summary": summary, "target": TARGET, "rows": rows},
                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    band = ("below band" if grounding < TARGET["band_low"] else
            "above band" if grounding > TARGET["band_high"] else "within band") if grounding is not None else "n/a"
    print(f"\nRun {summary['run']}: grounding {grounding}% ({supported}/{judged} claims; {band} of the "
          f"PROVISIONAL {TARGET['band_low']:.0f}–{TARGET['band_high']:.0f}% band) · citations valid "
          f"{valid_cites}/{len(all_cites)} · out-of-scope OK {oos_ok}/{len(oos)} · avg cost/question "
          f"${summary['avg_cost_total_usd']:.5f} (generation ${summary['avg_cost_generation_usd']:.5f})")
    print(f"Saved {LATEST.relative_to(ROOT)} and appended to {RUNS.relative_to(ROOT)}")
    tick(total, total, "Done")
    return summary


if __name__ == "__main__":
    main()
