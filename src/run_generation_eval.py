"""End-to-end generation eval: answer() over the 10 frozen queries.

Prints per query: answer, cited ids, citation_ok, edge behaviour (Q7–Q10), tokens + cost.
Saves eval/generation_results.md with a blank human-approval column.
eval/queries.json, the gold labels and top_k are only read.

Usage:  python src/run_generation_eval.py
"""
from datetime import date

from generate import KB, MODEL, EFFORT, answer, cost_usd
from index import get_collection
from ingest import ROOT
from run_eval import load_queries
from verify import verify

RESULTS = ROOT / "eval" / "generation_results.md"
REDIRECT_DOCS = {"18", "04"}   # Tracking your order, Your account


def behaviour(q: dict, r: dict) -> tuple[str, bool | None]:
    """Expected edge behaviour for Q7–Q10; None for answerable queries."""
    t = q["type"]
    if t in ("out-of-kb-absent", "out-of-kb-domain"):
        return "refuse", r["refused"]
    if t == "out-of-kb-live-data":
        return "redirect to tracking/account (18/04)", bool(REDIRECT_DOCS & set(r["cited_ids"]))
    if t == "ambiguous-should-clarify":   # asks back instead of refusing; it may cite why it asks
        return "ask one clarifying question", not r["refused"] and "?" in r["answer"]
    return "answer", None


def main():
    cfg = load_queries()
    col = get_collection()
    rows, total_cost, tin, tout = [], 0.0, 0, 0
    for q in cfg["queries"]:
        r = answer(q["query"], col=col)
        v = verify(r)
        expect, ok = behaviour(q, r)
        c = cost_usd(r["usage"])
        total_cost += c
        tin += r["usage"]["input_tokens"]
        tout += r["usage"]["output_tokens"]
        gold_in = all(g in r["retrieved_ids"] for g in q["gold"]) if q["gold"] else None
        rows.append((q, r, v, expect, ok, c, gold_in))

        print(f"\n=== {q['id']} ({q['type']}): {q['query']}")
        print(r["answer"])
        print(f"  cited {r['cited_ids']}  retrieved {r['retrieved_ids']}  "
              f"citation_ok={v['citation_ok']} {'; '.join(v['problems'])}")
        if ok is not None:
            print(f"  behaviour: expected {expect} -> {'OK' if ok else 'WRONG'}")
        print(f"  tokens in/out {r['usage']['input_tokens']}/{r['usage']['output_tokens']}  ~${c:.5f}")

    cit_ok = sum(v["citation_ok"] for _, _, v, *_ in rows)
    edge = [row[4] for row in rows if row[4] is not None]
    print(f"\nCitations OK: {cit_ok}/{len(rows)} · edge behaviour OK: {sum(edge)}/{len(edge)} · "
          f"tokens {tin}/{tout} · total ~${total_cost:.4f} (~${total_cost / len(rows):.5f}/query)")

    mark = lambda b: "—" if b is None else ("✅" if b else "❌")
    out = [
        "# Generation eval — grounded, cited answers (DL15)\n",
        f"Run {date.today().isoformat()} · model `{MODEL}` (effort {EFFORT}) · top-3 docs from the current "
        "retriever (score gate off; the model decides to refuse) · frozen `eval/queries.json` unchanged.\n",
        "**Auto checks:** `citation_ok` = every cited id is a real KB doc and was retrieved, and an answer "
        "has at least one citation. Edge behaviour = Q9/Q10 refuse, Q8 cites the tracking/account doc "
        "(18/04), Q7 asks a clarifying question.  ",
        "**Human check (fill in):** for each answer — is it correct, does every cited doc actually support "
        "its claim, and is nothing invented (Q8: no made-up order status)? Mark yes/no.\n",
        "## Summary\n",
        "| Query | Type | Gold in top-3 | Cited | Retrieved | citation_ok | Edge behaviour | Tokens in/out | Cost (USD) | Human-approved (yes/no) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for q, r, v, expect, ok, c, gold_in in rows:
        cited = ", ".join(r["cited_ids"]) or "—"
        edge_s = "—" if ok is None else f"{mark(ok)} {expect}"
        out.append(f"| {q['id']} | {q['type']} | {mark(gold_in)} | {cited} | {', '.join(r['retrieved_ids'])} | "
                   f"{mark(v['citation_ok'])} | {edge_s} | {r['usage']['input_tokens']}/"
                   f"{r['usage']['output_tokens']} | {c:.5f} |  |")
    out.append(f"\n**Citations OK:** {cit_ok}/{len(rows)} (target 100%) · **Edge behaviour OK:** "
               f"{sum(edge)}/{len(edge)} · **Total cost:** ~${total_cost:.4f} for {len(rows)} queries "
               f"(~${total_cost / len(rows):.5f}/query; {tin} in / {tout} out tokens)  ")
    out.append("**Answer approval:** ___ / 6 answerable = ___ % (target >70%) — fill after the human check.\n")
    out.append("## Answers\n")
    for q, r, v, expect, ok, c, gold_in in rows:
        out.append(f"### {q['id']} — {q['query']}\n")
        out.append("\n".join("> " + line for line in r["answer"].splitlines()) or "> (empty)")
        docs = ", ".join(f"[{d}] {KB[d][0]}" for d in r["retrieved_ids"])
        out.append(f"\nRetrieved: {docs}  ")
        out.append(f"Cited: {', '.join(r['cited_ids']) or '—'} · citation_ok {mark(v['citation_ok'])}"
                   + (f" ({'; '.join(v['problems'])})" if v["problems"] else "") + "\n")
    RESULTS.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Saved to {RESULTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
