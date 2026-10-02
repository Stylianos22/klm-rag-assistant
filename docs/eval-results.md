# Retrieval eval results — full 51-doc KB

Run on 2026-10-01 with `python src/run_eval.py --reindex` and `--sweep` (all-MiniLM-L6-v2, title+body embeddings, top-3, abstain < 0.35). Unedited output:

```
indexed 51 chunks

Retrieval eval — top-3, abstain < 0.35

id   type                       gold       top-3 (score)                      verdict
Q1   answerable                 26         26(0.72) 27(0.59) 32(0.59)         HIT
Q2   answerable                 35         35(0.41) 22(0.37) 33(0.37)         HIT
Q3   answerable-multidoc        32,30,29   30(0.72) 34(0.71) 26(0.67)         MISS
Q4   answerable-multidoc        16,17      16(0.64) 15(0.62) 17(0.60)         HIT
Q5   answerable                 07         07(0.43) 30(0.37) 34(0.26)         HIT
Q6   answerable                 27         35(0.35) 26(0.33) 22(0.33)         MISS (abstained)
Q7   ambiguous-should-clarify   -          33(0.49) 26(0.47) 28(0.47)         retrieved (judge at generation)
Q8   out-of-kb-live-data        -          18(0.52) 02(0.48) 22(0.38)         retrieved (judge at generation)
Q9   out-of-kb-absent           -          31(0.38) 12(0.34) 32(0.24)         RISK: would answer
Q10  out-of-kb-domain           -          44(0.08) 40(0.08) 26(0.07)         abstain OK

Retrieval: 4/6 = 67%  (target >80%: FAIL)
Out-of-KB abstain (Q9, Q10): 1/2
Q7 (clarify) and Q8 (live order data) are judged at the generation step.

Top-1 scores
  Q1   0.717  answerable
  Q3   0.717  answerable
  Q4   0.643  answerable
  Q5   0.434  answerable
  Q2   0.415  answerable
  Q9   0.379  OUT-OF-KB
  Q6   0.349  answerable
  Q10  0.083  OUT-OF-KB

Lowest answerable: Q6 0.349   Highest out-of-KB: Q9 0.379
NOT separable by a single threshold — some query will be wrong either way.
```

**Reading it:** retrieval is 4/6 = 67% (target >80%) and Q9 (price-match, deliberately absent from the KB) would be answered. The sweep shows no single similarity threshold can both answer Q6 and refuse Q9. Analysis and fix options: [DL13](decision-logs/DL13-full-kb-broke-abstain-threshold.md).
