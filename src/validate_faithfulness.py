"""Validate the faithfulness check against hand-labelled cases (DL16 C1).

Reads eval/faithfulness_cases.json (real answers + corrupted copies, labelled
faithful/unfaithful), runs faithfulness.check() with the chosen judge, and reports
agreement with the labels and the share of corrupted cases caught. A corrupted
case counts as caught only if its injected claim (corrupted_text) is itself flagged.

Output never overwrites the v1 baseline (eval/faithfulness_validation.md, judge v1,
original labels): v2 -> eval/faithfulness_validation_v2.md,
v1 re-run -> eval/faithfulness_validation_v1_rerun.md.

Usage:  python src/validate_faithfulness.py            # judge v2 (default)
        python src/validate_faithfulness.py --judge v1
"""
import argparse
import json
import re
from datetime import datetime

from faithfulness import DEFAULT_JUDGE, JUDGES, check, config
from generate import cost_usd
from ingest import ROOT

CASES = ROOT / "eval" / "faithfulness_cases.json"
V1_BASELINE = ROOT / "eval" / "faithfulness_validation.md"     # recorded v1 run, original labels
OUT = {"v1": ROOT / "eval" / "faithfulness_validation_v1_rerun.md",
       "v2": ROOT / "eval" / "faithfulness_validation_v2.md"}
AGREEMENT_BAR = 0.90      # DL16 C1 (provisional until teacher sign-off); corrupted catch must be 100%


def v1_recorded_vs_current_labels(cases: list[dict]) -> str | None:
    """Re-score the RECORDED v1 verdicts (no new API call) against today's labels."""
    if not V1_BASELINE.exists():
        return None
    preds = dict(re.findall(r"^\| (Q\d+-\w+) \| \w+ \| (faithful|unfaithful) \|", V1_BASELINE.read_text(), re.M))
    scored = [(c, preds.get(c.get("previous_id", c["id"]))) for c in cases]
    scored = [(c, p) for c, p in scored if p]
    agree = sum(p == c["label"] for c, p in scored)
    return f"{agree}/{len(scored)} = {agree / len(scored):.0%}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", choices=sorted(JUDGES), default=DEFAULT_JUDGE)
    version = ap.parse_args().judge

    data = json.loads(CASES.read_text(encoding="utf-8"))
    cases = data["cases"]
    rows, cost = [], 0.0
    for c in cases:
        f = check(c, question=c["question"], version=version)
        cost += cost_usd(f["usage"])
        pred = "faithful" if f["grounded"] else "unfaithful"
        flagged = [x for x in f["claims"] if x["supported"] is False]
        inj = c.get("corrupted_text")
        injected_caught = None if not inj else any(inj in x["claim"] for x in flagged)
        rows.append((c, f, pred, injected_caught))
        print(f"{c['id']:<13} label={c['label']:<10} predicted={pred:<10} "
              f"{'OK' if pred == c['label'] else 'MISMATCH'}  ({len(flagged)} unsupported)"
              + ("" if inj is None else f"  injected claim flagged: {injected_caught}"))
        for x in flagged:
            print(f"    UNSUPPORTED {x['cited_ids']} {x['claim'][:90]}\n      -> {x['reason']}")

    n = len(rows)
    agree = sum(p == c["label"] for c, _, p, _ in rows)
    corrupted = [r for r in rows if r[0].get("corrupted_text")]
    caught = sum(bool(r[3]) for r in corrupted)
    real = [r for r in rows if not r[0].get("corrupted_text")]
    real_agree = sum(p == c["label"] for c, _, p, _ in real)
    ok = agree / n >= AGREEMENT_BAR and caught == len(corrupted)
    summary = (f"Judge {version}: agreement {agree}/{n} = {agree / n:.0%} (bar ≥{AGREEMENT_BAR:.0%}) · "
               f"corrupted caught {caught}/{len(corrupted)} = {caught / len(corrupted):.0%} (bar 100%; the "
               f"injected claim itself must be flagged) · real answers {real_agree}/{len(real)} · "
               f"judge cost ~${cost:.4f} → C1 {'MET' if ok else 'NOT MET'}")
    v1_rescored = v1_recorded_vs_current_labels(cases)
    print("\n" + summary)
    if v1_rescored:
        print(f"Baseline: recorded v1 verdicts vs the corrected labels = {v1_rescored} (60% vs the original labels)")

    cfg = config(version)
    changes = [c for c in cases if c.get("label_change")]
    md = [
        f"# Faithfulness check — validation, judge {version} (DL16 C1)\n",
        f"Run {datetime.now().isoformat(timespec='minutes')} · judge `{cfg['judge_model']}` (effort "
        f"{cfg['judge_effort']}) · {cfg['judge_version']} · cases: `eval/faithfulness_cases.json` "
        "(labels corrected 2026-11-10)\n",
        f"**{summary}**\n",
    ]
    if v1_rescored:
        md.append(f"**Baseline (v1, not re-run):** 6/10 = 60% against the original labels "
                  f"(`eval/faithfulness_validation.md`); the same recorded v1 verdicts score "
                  f"{v1_rescored} against the corrected labels.\n")
    md.append("One run of a non-deterministic judge: re-run before quoting a number as stable.\n")
    if changes:
        md.append("## Label changes\n\n| Case | From → to | Claim | Cited doc says | Reason |\n|---|---|---|---|---|")
        for c in changes:
            lc = c["label_change"]
            md.append(f"| {c['id']} | {lc['from']} → {lc['to']} | {lc['claim']} | {lc['cited_doc_text']} | {lc['reason']} |")
        md.append("")
    md += ["## Results\n", "| Case | Label | Predicted | Match | Claims judged | Unsupported | Injected claim flagged |",
           "|---|---|---|---|---|---|---|"]
    for c, f, p, ic in rows:
        judged = [x for x in f["claims"] if x["supported"] is not None]
        uns = sum(x["supported"] is False for x in judged)
        md.append(f"| {c['id']} | {c['label']} | {p} | {'✅' if p == c['label'] else '❌'} | {len(judged)} | {uns} | "
                  f"{'—' if ic is None else ('✅' if ic else '❌')} |")
    md.append("\n## Per-claim verdicts\n")
    for c, f, p, _ in rows:
        md.append(f"### {c['id']} — {c['note']}\n")
        md.append("| Verdict | Cited | Claim | Judge's reason |\n|---|---|---|---|")
        for x in f["claims"]:
            cited = ", ".join(x["cited_ids"]) + ("" if x["cited_in_sentence"] else " (answer-level)")
            md.append(f"| {x['verdict']} | {cited} | {x['claim'].replace('|', chr(92) + '|')} | "
                      f"{x['reason'].replace('|', chr(92) + '|')} |")
        md.append("")
    OUT[version].write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Saved to {OUT[version].relative_to(ROOT)}")


if __name__ == "__main__":
    main()
