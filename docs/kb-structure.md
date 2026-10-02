---
type: note
author: claude
project: KLM RAG (Research Project)
date: 2026-09-29
---

# KB Structure — the ~50-document plan

**Store (fictional, single):** **"Northbound"** — a mid-size online store selling apparel + general goods, ships across the EU. *(Placeholder name — rename if you like; keep it ONE store so the KB never contradicts itself.)*

**How to read this:** each line is one document to write. **★ = gold doc** (a frozen test query depends on it — see Test Queries (v1 — frozen before KB)). Everything else is realistic filler so the KB is bigger than the test set (the queries aren't the whole KB).

**Deliberate exclusions (keep these true):**
- **No price-match document** — Q9 ("do you price-match?") must stay unanswerable. Don't write one.
- **No order-status/tracking-lookup content that invents live data** — Q8 ("where's my order #…") is answered by *pointing to* the account/tracking page, never by a doc that fakes a status.

**Count:** 51 docs across 7 sections (8 gold, 43 filler).

---

## 1. Store basics (6)
1. About Northbound — who we are
2. Contact us & support hours
3. How to place an order
4. Your account: create, manage, close
5. Newsletter & communication preferences
6. Where we ship / countries served

## 2. Payment (8)
7. **★ Payment methods we accept** — cards, PayPal, **Klarna / pay-later (BNPL)**
8. Payment security & verification (3-D Secure)
9. Declined or failed payments
10. Promo codes & vouchers — how to apply
11. Gift cards — buying & redeeming
12. Prices, currency & VAT
13. Order confirmation & invoices
14. Pre-orders & backorders

## 3. Shipping & delivery (11)
15. Domestic shipping options & delivery times
16. **★ International shipping times**
17. **★ Shipping costs & the free-shipping threshold**
18. Tracking your order *(points to account — no live data)*
19. Delivery partners & delivery windows
20. Missed delivery & redelivery
21. Parcel marked delivered but not received
22. Damaged in transit
23. Customs, duties & import charges (outside home country)
24. Click & collect / pickup points
25. Address changes before dispatch

## 4. Returns, refunds & exchanges (12)
26. **★ Standard returns policy & return window**
27. **★ EU right of withdrawal — 14-day cooling-off** *(change-of-mind, distinct from faulty)*
28. How to start a return (RMA steps)
29. **★ Return shipping — who pays & how**
30. **★ Refunds — method & timing**
31. Exchanges
32. **★ Sale & clearance items — return exceptions**
33. Final-sale / non-returnable items (hygiene, personalised)
34. Store credit & return vouchers
35. **★ Faulty, defective or wrong item received**
36. Missing parts or accessories
37. Warranty & guarantee terms

## 5. Products & sizing (5)
38. Sizing guide & fit
39. Product care instructions
40. Stock availability & restock notifications
41. Materials & product authenticity
42. Product safety & recalls

## 6. Account, privacy & legal (6)
43. Privacy policy — how we handle your data
44. Cookie policy
45. Terms & conditions of sale
46. Your statutory consumer rights (summary)
47. Complaints & dispute resolution (EU ODR)
48. Accessibility statement

## 7. Loyalty & extras (3)
49. Loyalty / rewards programme
50. Gift wrapping & gift receipts
51. Sustainability & packaging

---

## Gold-doc → query map (the 8 that must exist and be findable)
| Doc | Query it answers |
|---|---|
| #7 Payment methods | Q5 "do you do pay-later, like Klarna?" |
| #16 International shipping times | Q4 (part 1) |
| #17 Free-shipping threshold | Q4 (part 2) |
| #26 Returns window | Q1 "how long to return?" |
| #27 EU 14-day withdrawal | Q6 "changed my mind, can I still send it back?" |
| #29 Return shipping who-pays | Q3 (part) |
| #30 Refunds method & timing | Q3 (part) |
| #32 Sale-items return exception | Q3 (part) |
| #35 Faulty / defective item | Q2 "boots arrived with a ripped seam" |

*(Q3 is the multi-doc one — it needs #29 + #30 + #32 together, which is why it's the hardest retrieval case.)*

## Next
Write the content, ~1 topic per doc, in Northbound's voice. Suggested order: the **8 gold docs first** (so the pipeline can be tested early on a real slice), then the filler. Then the 5-doc spike (DL-05 stack confirmation) can run against a handful of these.
