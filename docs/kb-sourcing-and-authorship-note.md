---
type: note
author: claude
project: KLM RAG (Research Project)
date: 2026-10-01
---

# KB — sourcing & authorship note (for the ethics section / LO6)

**What the knowledge base is.** 51 documents for a single **fictional** store, "Northbound" (apparel + general goods, EU). Nothing is copied from a real company — this is the self-authored route chosen in decision log #9, so there is no copyright question.

**Who wrote it, and the disclosure.** All 51 docs are **AI-authored by Claude (in the Cowork chat)** — the 9 gold docs on 2026-09-29 and the 42 filler docs on 2026-10-01. The author **knew the 10 test queries**. To keep the evaluation honest despite that:
- The docs were written as **realistic store policy**, not reverse-engineered to pass specific queries.
- The **queries were frozen first** (2026-09-29, before the KB existed) — freeze-then-test, decision log #9.
- Two gaps were **deliberately preserved**: there is **no price-match document** (so Q9 "do you price-match?" stays genuinely unanswerable) and **no faked order-status content** (Q8 "where's my order #…" is redirected to the account/tracking, never invented).

**Why this matters for the grade.** The integrity risk of self-authored data is "writing docs to fit the test." The mitigations above (freeze-first, realistic content, preserved gaps, this disclosure) are the defense. Flag this note in the ethics section (LO6) and when presenting retrieval results.
