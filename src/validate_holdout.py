"""Held-out validation of the FROZEN judge v2 (DL16 C1).

Runs faithfulness.check() (judge v2, unchanged) on eval/faithfulness_holdout.json:
answers the v2 prompt never saw, labelled by hand by Stylianos. Reports agreement
and per-case / per-claim verdicts. Report only: nothing here tunes the judge.

Refuses to run until every case has a label ("faithful" / "unfaithful").
Records a hash of the v2 prompt so the report proves which prompt was tested.

Usage:  python src/validate_holdout.py
"""
import hashlib
import json
import sys
from datetime import datetime

from faithfulness import JUDGE_SYSTEM_V2, check, config
from generate import cost_usd
from ingest import ROOT

CASES = ROOT / "eval" / "faithfulness_holdout.json"
OUT = ROOT / "eval" / "faithfulness_holdout_results.md"
FROZEN_V2_SHA = "568c148316dd"   # sha256[:12] of JUDGE_SYSTEM_V2 at commit 7519554


def main():
    prompt_sha = hashlib.sha256(JUDGE_SYSTEM_V2.encode()).hexdigest()[:12]
    if prompt_sha != FROZEN_V2_SHA:
        sys.exit(f"Judge v2 prompt changed (sha {prompt_sha} != frozen {FROZEN_V2_SHA}). "
                 "The held-out test is only valid on the frozen prompt.")
    cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
    unlabelled = [c["id"] for c in cases if c.get("label") not in ("faithful", "unfaithful")]
    if unlabelled:
        sys.exit(f"Label these first (\"faithful\" or \"unfaithful\") in {CASES.relative_to(ROOT)}: "
                 + ", ".join(unlabelled))

    rows, cost = [], 0.0
    for c in cases:
        f = check(c, question=c["question"], version="v2")
        cost += cost_usd(f["usage"])
        pred = "faithful" if f["grounded"] else "unfaithful"
        rows.append((c, f, pred))
        print(f"{c['id']:<4} label={c['label']:<10} judge={pred:<10} {'OK' if pred == c['label'] else 'MISMATCH'}")
        for x in f["claims"]:
            print(f"     {x['verdict']:<12} {x['claim'][:80]}\n                  -> {x['reason']}")

    n = len(rows)
    agree = sum(p == c["label"] for c, _, p in rows)
    unf = [r for r in rows if r[0]["label"] == "unfaithful"]
    fai = [r for r in rows if r[0]["label"] == "faithful"]
    caught = sum(p == "unfaithful" for _, _, p in unf)
    passed = sum(p == "faithful" for _, _, p in fai)
    summary = (f"Judge v2 on the held-out set: agreement {agree}/{n} = {agree / n:.0%} (bar ≥90%; in-sample was 100%) · "
               f"unfaithful caught {caught}/{len(unf)} · faithful passed {passed}/{len(fai)} · cost ~${cost:.4f}")
    print("\n" + summary)

    cfg = config("v2")
    md = [
        "# Faithfulness check — held-out validation, judge v2 (DL16 C1)\n",
        f"Run {datetime.now().isoformat(timespec='minutes')} · judge `{cfg['judge_model']}` (effort {cfg['judge_effort']}) · "
        f"{cfg['judge_version']} · prompt sha256 `{prompt_sha}` (frozen, untouched) · cases: "
        "`eval/faithfulness_holdout.json` (labels by Stylianos)\n",
        f"**{summary}**\n",
        "Report only: the judge was not tuned on this result. One run of a non-deterministic judge; "
        "8 cases is a small sample, so one case moves agreement by 12.5 points.\n",
        "## Results\n", "| Case | Question | Label | Judge | Match | Claims flagged |", "|---|---|---|---|---|---|",
    ]
    for c, f, p in rows:
        flagged = sum(x["supported"] is False for x in f["claims"])
        md.append(f"| {c['id']} | {c['question']} | {c['label']} | {p} | {'✅' if p == c['label'] else '❌'} | {flagged} |")
    md.append("\n## Per-claim verdicts\n")
    for c, f, p in rows:
        md.append(f"### {c['id']} — label {c['label']}" + (f" ({c['label_reason']})" if c.get("label_reason") else "") + "\n")
        md.append("| Verdict | Cited | Claim | Judge's reason |\n|---|---|---|---|")
        for x in f["claims"]:
            md.append(f"| {x['verdict']} | {', '.join(x['cited_ids'])} | {x['claim'].replace('|', chr(92) + '|')} | "
                      f"{x['reason'].replace('|', chr(92) + '|')} |")
        md.append("")
    OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Saved to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
