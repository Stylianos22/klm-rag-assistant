# Reranker experiment — bi-encoder vs cross-encoder rerank

Bi-encoder: all-MiniLM-L6-v2 (title+body, cosine), top-3 docs — the current pipeline.  
Reranked: same bi-encoder pulls the top 15 chunks -> `cross-encoder/ms-marco-MiniLM-L-6-v2` re-scores each (query, "title — section. text") -> best score per doc -> top-3.  
Frozen `eval/queries.json`, gold labels and top_k=3 unchanged. Hit = all gold docs in top 3. Not wired into the pipeline.

## Retrieval per query

| Query | Type | Gold | Bi-encoder top-3 (cosine) | | Reranked top-3 (logit) | |
|---|---|---|---|---|---|---|
| Q1 | answerable | 26 | 26 (0.72), 27 (0.59), 32 (0.59) | ✅ hit | 26 (4.97), 35 (4.80), 27 (3.23) | ✅ hit |
| Q2 | answerable | 35 | 35 (0.41), 22 (0.37), 33 (0.37) | ✅ hit | 22 (-9.25), 35 (-10.19), 33 (-10.20) | ✅ hit |
| Q3 | answerable-multidoc | 32, 30, 29 | 30 (0.72), 34 (0.71), 26 (0.67) | ❌ miss | 34 (2.12), 30 (1.85), 32 (1.22) | ❌ miss |
| Q4 | answerable-multidoc | 16, 17 | 16 (0.64), 15 (0.62), 17 (0.60) | ✅ hit | 16 (0.44), 15 (-0.02), 17 (-0.78) | ✅ hit |
| Q5 | answerable | 07 | 07 (0.43), 30 (0.37), 34 (0.26) | ✅ hit | 07 (4.74), 30 (-0.99), 29 (-11.16) | ✅ hit |
| Q6 | answerable | 27 | 35 (0.35), 26 (0.33), 22 (0.33) | ❌ miss | 29 (0.38), 26 (0.02), 35 (-1.37) | ❌ miss |
| Q7 | ambiguous-should-clarify | — | 33 (0.49), 26 (0.47), 28 (0.47) | — | 33 (4.50), 26 (4.35), 28 (1.74) | — |
| Q8 | out-of-kb-live-data | — | 18 (0.52), 02 (0.48), 22 (0.38) | — | 18 (-6.12), 36 (-7.59), 22 (-7.78) | — |
| Q9 | out-of-kb-absent | — | 31 (0.38), 12 (0.34), 32 (0.24) | — | 31 (-10.54), 12 (-10.59), 15 (-11.01) | — |
| Q10 | out-of-kb-domain | — | 44 (0.08), 40 (0.08), 26 (0.07) | — | 26 (-11.25), 15 (-11.27), 35 (-11.29) | — |

**Retrieval (6 answerable):** bi-encoder **4/6 = 67%** · reranked **4/6 = 67%** · target >80%

## Abstention — is there a separating gap?

Gap = lowest top-1 score among the answerable queries minus highest top-1 among the should-refuse queries. Positive = a single threshold can separate them. Cross-encoder logits are unbounded, so the gap is also shown after a sigmoid (0–1), the only scale where DL14's "≥ 0.10" is comparable to cosine.

| Should-refuse set | Signal | Lowest answerable | Highest should-refuse | Gap |
|---|---|---|---|---|
| Q8, Q9, Q10 (brief) | cosine | Q6 0.349 | Q8 0.518 | **-0.169** |
| Q8, Q9, Q10 (brief) | rerank logit | Q2 -9.25 | Q8 -6.12 | **-3.13** |
| Q8, Q9, Q10 (brief) | rerank sigmoid | Q2 0.000 | Q8 0.002 | **-0.002** |
| Q9, Q10 (run_eval) | cosine | Q6 0.349 | Q9 0.379 | **-0.030** |
| Q9, Q10 (run_eval) | rerank logit | Q2 -9.25 | Q9 -10.54 | **+1.29** |
| Q9, Q10 (run_eval) | rerank sigmoid | Q2 0.000 | Q9 0.000 | **+0.000** |

**Top-1 score per query**

| Query | Cosine | Rerank logit | Rerank sigmoid |
|---|---|---|---|
| Q1 | 0.717 | 4.97 | 0.993 |
| Q2 | 0.415 | -9.25 | 0.000 |
| Q3 | 0.717 | 2.12 | 0.893 |
| Q4 | 0.643 | 0.44 | 0.608 |
| Q5 | 0.434 | 4.74 | 0.991 |
| Q6 | 0.349 | 0.38 | 0.593 |
| Q7 | 0.494 | 4.50 | 0.989 |
| Q8 | 0.518 | -6.12 | 0.002 |
| Q9 | 0.379 | -10.54 | 0.000 |
| Q10 | 0.083 | -11.25 | 0.000 |

**Rerank latency (CPU, 15 pairs/query):** median 55 ms, max 360 ms — excludes the one-off model load.

