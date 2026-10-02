---
type: note
author: claude
project: KLM RAG (Research Project)
date: 2026-09-29
---

# KLM RAG — 10 Test Queries (v1)

> ❄️ **FROZEN 2026-09-29.** Locked before any KB document was written. Queries are not edited after this point — if one turns out flawed, note it and record the fix rather than silently rewriting. This lock is the freeze-then-test evidence.

> **Freeze-then-test:** written 2026-09-29, **before** any knowledge-base document exists. This is the ruler; the KB gets built to cover a realistic store, NOT reverse-engineered to pass these. Do not edit a query to match a doc after the fact — add a note instead. *(DL-04 / log #9.)*

**Design (agreed with Stylianos):** realistic phrasing, weighted **hard** (paraphrase + multi-doc), all **three** out-of-KB types, plus one **ambiguous** case. "Gold doc" = the topic the answer must come from; those docs don't exist yet — that's expected.

**Scoring per query**
- **Retrieval hit** = the gold doc(s) appear in the retrieved top-k. (Refusal/ambiguous cases: correct if the system finds nothing truly relevant and does not force a match.)
- **Answer approved** = human judges it correct + grounded (answerable), a correct refusal (out-of-KB), or a correct clarifying question (ambiguous).
- **Citation** = every claim points to a doc that actually supports it; refusals cite nothing and say it's not covered.

---

## Answerable (6)

**Q1 — baseline, single-doc (easy)**
"How long do I have to return something?"
- Gold: Returns window policy. · Tests: basic retrieval works at all.

**Q2 — paraphrase + right-doc discrimination (hard)**
"The boots I ordered turned up with a ripped seam — can I get my money back?"
- Gold: Faulty/defective items policy (NOT the standard change-of-mind returns doc). · Tests: meaning-based retrieval; not grabbing the wrong but similar doc.

**Q3 — multi-doc synthesis (hard)**
"I'm sending back a sale item I bought about 3 weeks ago — do I get a refund or store credit, and who pays the return postage?"
- Gold: Sale-items exception + Returns window + Return-shipping/refund-method. · Tests: combining 2–3 docs into one answer.

**Q4 — multi-doc, conditional (hard)**
"Shipping to Germany — how long does it take, and do I get free delivery on a €45 order?"
- Gold: International shipping times + Free-shipping threshold. · Tests: two facts from two docs, with a numeric condition.

**Q5 — synonym / paraphrase (medium)**
"Do you do pay-later, like Klarna?"
- Gold: Payment methods policy. · Tests: mapping "pay later / Klarna" → the BNPL section without those exact words in the query.

**Q6 — legal-anchored discrimination (hard)**
"Nothing's actually wrong with it, I just changed my mind — can I still send it back?"
- Gold: EU 14-day right-of-withdrawal doc (NOT the faulty-items doc). · Tests: picking the correct legal basis over the superficially-similar returns doc.

## Ambiguous — should ask, not guess (1)

**Q7 — under-specified**
"Can I return it?"
- Expected behavior: **ask a clarifying question** (which item? bought when? faulty or change-of-mind?) rather than assume one policy. · Tests: handling missing context instead of guessing.

## Out-of-KB — must refuse, not invent (3)

**Q8 — needs live / personal data**
"Where's my order #48213? It's been a week."
- Expected: it CAN'T know order status; point to account/tracking, don't invent a status. · Tests: refusing on data the KB structurally can't hold.

**Q9 — plausible but deliberately absent**
"Do you price-match other shops if I find it cheaper?"
- Expected: honest "that isn't covered / we don't have that policy." *(Decision: do NOT write a price-match doc — keep this genuinely absent.)* · Tests: the "answer isn't there" case.

**Q10 — out-of-domain**
"Which of your laptops is best for gaming?"
- Expected: no product recommendation, no invented specs; redirect to browsing/support. · Tests: not hallucinating outside the policy domain.

---
*Next: build the ~50-doc KB covering the gold topics above (plus others, so the set isn't the whole KB), then run retrieval and score against this file.*


---

## Scoring spec (added 2026-09-29 — how the queries are graded)

**Retrieval accuracy** — measured over the **6 answerable** queries (Q1–Q6):
- Retrieve **top-3** documents per query.
- A query passes if its **gold doc** is in the top-3. For multi-doc queries (Q3, Q4), **all** required gold docs must be in the top-3.
- Accuracy = passes ÷ 6. **Target >80%** (≥5 of 6).

**Answer approval** — over **all 10**; a human marks a query *approved* only if it passes **every** check:
- **Correct** — matches the store's policy.
- **Grounded** — uses only retrieved docs; nothing invented.
- **Cited** — every factual claim cites a doc that actually supports it; a **wrong or missing citation is an automatic fail** (this is also the 100%-citation gate).
- **Right behavior on the hard ones** — Q8–Q10 refuse/redirect (no invented answer); Q7 asks a clarifying question.
- Approval rate = approved ÷ 10. **Target >70%** (≥7 of 10).

**Citations: 100%** — enforced through the approval gate above, not scored separately.
