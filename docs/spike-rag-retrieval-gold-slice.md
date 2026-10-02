---
type: note
author: claude
project: KLM RAG (Research Project)
date: 2026-10-01
---

# Spike — RAG retrieval on the 9 gold docs

**Goal:** prove the stack works end-to-end on a small slice before writing all ~51 docs, and confirm the provisional stack (DL-05).

**Setup:** 9 gold docs (whole-doc chunks) · embeddings **all-MiniLM-L6-v2** (local, free) · cosine similarity, **top-3** · out-of-KB abstain threshold 0.35. Scored against the frozen queries using the agreed rule (gold doc in top-3; multi-doc = all golds in top-3).

> ⚠️ **CORRECTION (2026-10-01).** The **100% in Run 2** below was measured on the **hand-written one-line summaries** inside `spike.py`, **not** the real KB document text. When the actual pipeline (Claude Code) embedded the **full docs** (title+body), retrieval was **67%**, not 100%. Takeaway: the stack runs end-to-end and abstains correctly, but **title+body alone does not hit the target on real docs**; the fix (likely a reranker) is being decided on the full KB. Treat the tables below as a spike-slice artifact, not the real-KB result.

## Run 1 — embed body only
| Query | Need | Result |
|---|---|---|
| Q1 how long to return | 26 | ❌ MISS (26 ranked 4th; sale/faulty/refunds above it) |
| Q2 ripped seam, money back | 35 | ✅ HIT |
| Q3 sale item, refund/credit + postage | 32+30+29 | ❌ MISS (got 30,32,35 — missed 29) |
| Q4 Germany time + free over €45 | 16+17 | ✅ HIT |
| Q5 pay-later / Klarna | 07 | ✅ HIT |
| Q6 changed my mind | 27 | ✅ HIT |
| Q9 price-match (out-of-KB) | — | ✅ abstain (top 0.29 < 0.35) |
| Q10 laptop advice (out-of-KB) | — | ✅ abstain (top 0.07) |

**Retrieval: 4/6 = 67%** — below the >80% target. Cause: closely-related return docs (standard/sale/faulty/refunds) competed, and whole-doc embeddings gave muddy signals, so the plain "returns window" doc got out-ranked by its siblings.

## Fix tried
Embed **the document title together with its body** (title carries the distinguishing topic word).

## Run 2 — embed title + body
| Query | Need | Result |
|---|---|---|
| Q1 | 26 | ✅ HIT |
| Q2 | 35 | ✅ HIT |
| Q3 | 32+30+29 | ✅ HIT (all three in top-3) |
| Q4 | 16+17 | ✅ HIT |
| Q5 | 07 | ✅ HIT |
| Q6 | 27 | ✅ HIT (but 27 ranked 3rd at 0.31 — thin margin; watch) |
| Q9 / Q10 | — | ✅ abstain |

**Retrieval: 6/6 = 100%** (target >80%). Abstention still clean.

## Conclusion
- **Stack confirmed (DL-05):** sentence-transformers + cosine top-3 + abstain threshold works end-to-end on the slice. Chroma is the storage layer for the full set; the spike used in-memory cosine (same math).
- **Carry forward into the full build:** (1) embed title + body, not body alone; (2) keep the 0.35 abstain threshold as the "not in KB" guard — re-tune once the KB is 51 docs; (3) watch Q6 — change-of-mind retrieves the returns doc strongly, withdrawal doc only 3rd.
- **Caveat:** 9 docs is tiny; scores will move at 51 docs. Re-run this exact harness after the full KB and after structure-aware chunking.

## Script
```python
# all-MiniLM-L6-v2, cosine top-3, abstain<0.35; embed title + body.
# Full script kept with the project; recreate by embedding (title + ". " + body)
# for each gold doc, then cosine against each frozen query, take top-3,
# score hit = gold doc(s) in top-3.
```
