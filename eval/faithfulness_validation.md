# Faithfulness check — validation against labelled cases (DL16 C1)

Run 2026-11-10T13:23 · judge `claude-haiku-5-5` (effort medium) · faithfulness-judge v1 · cases: `eval/faithfulness_cases.json`

**Agreement 6/10 = 60% (bar ≥90%) · corrupted caught 4/4 = 100% (bar 100%) · faithful passed 2/6 · judge cost ~$0.0108 → C1 NOT MET**

Labels: the 6 real answers are labelled *faithful* per the brief (not yet confirmed in the human-approval column); the corrupted copies change one fact but keep the real citation. One run of a non-deterministic judge, so re-run before quoting a number as stable.

| Case | Label | Predicted | Match | Claims judged | Unsupported |
|---|---|---|---|---|---|
| Q1-faithful | faithful | unfaithful | ❌ | 10 | 1 |
| Q2-faithful | faithful | unfaithful | ❌ | 10 | 4 |
| Q3-faithful | faithful | unfaithful | ❌ | 6 | 1 |
| Q4-faithful | faithful | faithful | ✅ | 5 | 0 |
| Q5-faithful | faithful | faithful | ✅ | 2 | 0 |
| Q6-faithful | faithful | unfaithful | ❌ | 7 | 1 |
| Q1-corrupted | unfaithful | unfaithful | ✅ | 10 | 2 |
| Q2-corrupted | unfaithful | unfaithful | ✅ | 9 | 3 |
| Q4-corrupted | unfaithful | unfaithful | ✅ | 4 | 2 |
| Q5-corrupted | unfaithful | unfaithful | ✅ | 2 | 1 |

## Per-claim verdicts

### Q1-faithful — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 26 | For most items, you have 30 days from delivery to return them for a refund. | The documents state that most items can be returned within 30 days of delivery for a refund, matching the sentence. |
| SUPPORTED | 26 | The item must be unused, in original condition, with tags and original packaging. | The documents state that to qualify for a return, items must be unused, in original condition, with tags and original packaging. |
| SUPPORTED | 26 | You can start a return from Your account → Returns. | The documents state that returns are started from Your account → Returns. |
| SUPPORTED | 26, 32, 27 (answer-level) | Some items have different rules: | The documents state that sale/clearance items, faulty items, and personalised or hygiene-sealed items follow different return rules from standard items. |
| SUPPORTED | 32 | Regular sale or discounted items: returnable within 14 days of delivery, refunded as store credit only. | The document states regular sale/discounted items are returnable within 14 days of delivery and refunded as store credit only, matching the sentence exactly. |
| SUPPORTED | 32 | Clearance or items marked "Final sale": not returnable. | The documents explicitly state that clearance items and items marked "Final sale" are not returnable, so the sentence matches the policy exactly. |
| SUPPORTED | 26 | Personalised or hygiene-sealed items: non-returnable unless faulty. | The documents state that personalised or hygiene-sealed items are non-returnable unless faulty, matching the sentence exactly. |
| SUPPORTED | 27 | Separately, you have a 14-day statutory right to withdraw from your order for any reason, which always applies. | The document states the 14-day right of withdrawal for any reason and that it always applies, so the sentence matches it. |
| SUPPORTED | 27 | Personalised goods and hygiene-sealed items are exceptions to this right. | The documents list personalised goods and hygiene-sealed items (once unsealed) as exceptions allowed by law to the 14-day right of withdrawal. |
| UNSUPPORTED | 32, 26 | Faulty, damaged, or wrong items are covered by their own rules, even if they were on sale. | The documents say faulty sale items remain covered, but they don't state that damaged or wrong sale items are also exempt from the sale return exceptions. |
| NOT_A_CLAIM | 26, 32, 27 (answer-level) | What type of item are you returning? | The sentence is a question back to the customer and states no policy fact. |
| NOT_A_CLAIM | 26, 32, 27 (answer-level) | I can give you a more specific answer. | The sentence is an offer to help further and states no policy fact. |

### Q2-faithful — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| UNSUPPORTED | 35, 22, 33 (answer-level) | Yes, you can likely get a full refund. | The documents grant a full refund only for faulty, damaged, or wrong items reported within 30 days; after that they offer only replacement or repair for manufacturing defects, so a general 'likely a full refund' is not stated. |
| SUPPORTED | 35 | Items that arrive faulty, damaged in transit, or not as ordered are covered: report the issue within 30 days for a free replacement or a full refund. | The documents state that faulty, damaged-in-transit, or wrong items are covered, with reporting within 30 days for a free replacement or full refund. |
| UNSUPPORTED | 35, 22, 33 (answer-level) | A ripped seam would generally count as faulty or damaged in transit. | The documents never say a ripped seam counts as faulty or damaged in transit, and their exclusion for normal wear or misuse makes that classification uncertain rather than something the documents establish. |
| NOT_A_CLAIM | 35, 22, 33 (answer-level) | To make the claim: | The sentence is a bare lead-in ending in a colon with no policy fact stated. |
| UNSUPPORTED | 35 | Report it within 30 days of delivery. | The documents give a 30-day reporting window but never say it runs from delivery, so the phrase "of delivery" adds an unstated condition. |
| SUPPORTED | 35 | Include your order number and a photo of the issue. | The documents say to include your order number and a photo of the issue, so the sentence matches the stated guidance. |
| SUPPORTED | 22 | Also photograph the packaging, and keep it until the issue is resolved. | The documents say to take photos of the item and packaging and to keep the packaging until the issue is resolved, which matches the sentence. |
| UNSUPPORTED | 35, 22, 33 (answer-level) | Return shipping is free. | The documents say Northbound pays return shipping only for faulty, damaged, or wrong items, and the change-of-mind return terms are not provided, so a blanket claim that return shipping is free is not supported. |
| SUPPORTED | 35 | Northbound sends a prepaid label. | The documents state that Northbound pays return shipping and sends a free label for faulty or wrong items, which means it sends a prepaid label. |
| SUPPORTED | 35 | If you're past 30 days, items are still covered for up to 2 years against manufacturing defects, though not damage from normal wear or misuse. | The documents state that beyond 30 days items are covered for up to 2 years against manufacturing defects, not damage from normal wear or misuse, which matches the sentence exactly. |
| SUPPORTED | 33 | Even if the boots were marked "Final sale," your statutory rights for faulty goods still apply. | The documents state that items marked "Final sale" are not returnable and that statutory rights for faulty goods always still apply, so the sentence follows directly from them. |

### Q3-faithful — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| UNSUPPORTED | 30 | Sale items are refunded as store credit only, not to your original payment method. | The documents say sale items *may* be refunded as store credit only and defer to a separate section that isn't provided, so the sentence's flat statement that they *are* refunded that way, never to the original payment method, goes beyond the documents. |
| SUPPORTED | 34 | Store credit is added to your account and does not expire. | Document [34] states that credit is added to your account and does not expire, matching the sentence exactly. |
| SUPPORTED | 30 | For postage, return postage is not refunded for change-of-mind returns. | The documents state that return postage is not refunded for change-of-mind returns. |
| SUPPORTED | 26 | Your return is within the 30-day window if it was delivered recently enough, since returns are accepted within 30 days of delivery. | The documents state that most items can be returned within 30 days of delivery, and the sentence restates that window without adding any new fact. |
| SUPPORTED | 26 | The items must be unused, in original condition, with tags and original packaging. | The documents state that to qualify for a return, items must be unused, in original condition, with tags and original packaging. |
| SUPPORTED | 26 | You can start the return from Your account → Returns. | The documents state that a return is started from Your account → Returns. |
| NOT_A_CLAIM | 30, 34, 26 (answer-level) | My documents don't include the full "Return shipping: who pays" article or the "Sale & clearance items: return exceptions" article, so I can't confirm any other conditions that apply to sale items. | The sentence only says the documents lack certain articles and therefore cannot confirm conditions, which is a remark about what the documents don't cover rather than a policy fact. |

### Q4-faithful — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 16 | Delivery to Germany takes 2–3 business days after dispatch, and orders are dispatched within 1 business day. | The documents state Germany delivery is 2–3 business days counted from dispatch and that orders are dispatched within 1 business day. |
| SUPPORTED | 16 | Estimates may be longer during sale periods and public holidays. | The document explicitly states that delivery estimates may be longer during sale periods and public holidays. |
| SUPPORTED | 16, 17 (answer-level) | You won't get free delivery on a €45 order. | A €45 order is below both the €50 Netherlands and €75 rest-of-EU free-shipping thresholds, and the document's own example confirms a €45 order to Germany pays €6.95 shipping. |
| SUPPORTED | 17 | Free standard shipping to the rest of the EU applies only on orders over €75. | Document 17 states that standard shipping to the rest of the EU is free on orders over €75, which matches the sentence. |
| SUPPORTED | 17 | Your order would be charged the standard EU rate of €6.95. | The documents state that the standard Rest-of-EU rate is €6.95, applying to orders not qualifying for the €75 free-shipping threshold, and the sentence states only that rate. |

### Q5-faithful — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| NOT_A_CLAIM | 07 (answer-level) | Yes. | The sentence "Yes." states no policy fact on its own and makes no checkable assertion about the documents. |
| SUPPORTED | 07 (answer-level) | Klarna pay-later is available, with two options: pay in 30 days, or pay in 3 interest-free instalments. | The documents list Klarna pay-later with exactly the two options stated: pay in 30 days, or pay in 3 interest-free instalments, subject to Klarna's approval. |
| SUPPORTED | 07 | Both are subject to Klarna's approval, and you can see Klarna's terms at checkout. | The documents state that both Klarna pay-later options (Pay in 30 days and Pay in 3 instalments) are subject to Klarna's approval and that Klarna's terms are available at checkout. |

### Q6-faithful — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| UNSUPPORTED | 26 (answer-level) | Yes, you can likely return it. | The sentence asserts that the unspecified item can likely be returned, but the documents give no basis to confirm eligibility for that item (it may be sale, personalised, or hygiene-sealed, which are non-returnable or excepted). |
| SUPPORTED | 26 | Northbound's policy allows most items to be returned within 30 days of delivery for a refund. | The documents state that most items can be returned within 30 days of delivery for a refund under Northbound's own policy. |
| SUPPORTED | 26 | The item must be unused, in original condition, with tags and original packaging. | The documents state that to qualify for a return, items must be unused, in original condition, with tags and original packaging. |
| SUPPORTED | 26 | You can start a return from Your account → Returns. | The documents state that a return is started from Your account → Returns. |
| SUPPORTED | 26 (answer-level) | A few items are handled differently. | The documents state that some items are handled differently, and list three such categories; "a few" is a mild paraphrase of "some" that the listed exceptions support. |
| SUPPORTED | 26 | Personalised or hygiene-sealed items can't be returned unless they're faulty. | The documents state that personalised or hygiene-sealed items are non-returnable unless faulty, which matches the sentence. |
| SUPPORTED | 26 | Sale and clearance items have their own return exceptions, but I don't have those details here. | The documents state that sale and clearance items have their own return exceptions, and the second clause only says the details aren't in the provided text, which is accurate. |
| NOT_A_CLAIM | 26 (answer-level) | I don't have information on who pays return postage for change-of-mind returns, or on how refunds are issued. | The sentence only says the assistant lacks information on postage and refunds, which is a remark about what the documents don't cover rather than a policy fact. |

### Q1-corrupted — CORRUPTED on purpose: 30 days -> 60 days, still cited to [26] (doc 26 says 30).

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| UNSUPPORTED | 26 | For most items, you have 60 days from delivery to return them for a refund. | The documents state a 30-day return window from delivery, not 60 days, so the sentence contradicts them. |
| SUPPORTED | 26 | The item must be unused, in original condition, with tags and original packaging. | The documents state that to qualify for return, items must be unused, in original condition, with tags and original packaging. |
| SUPPORTED | 26 | You can start a return from Your account → Returns. | The documents state that a return is started from Your account → Returns. |
| SUPPORTED | 26, 32, 27 (answer-level) | Some items have different rules: | The documents state that some items are handled differently (sale and clearance, faulty, personalised or hygiene-sealed items). |
| SUPPORTED | 32 | Regular sale or discounted items: returnable within 14 days of delivery, refunded as store credit only. | The document states regular sale/discounted items are returnable within 14 days of delivery and refunded as store credit only, matching the sentence exactly. |
| SUPPORTED | 32 | Clearance or items marked "Final sale": not returnable. | The documents explicitly state that clearance and items marked "Final sale" are not returnable, so the sentence matches the policy directly. |
| SUPPORTED | 26 | Personalised or hygiene-sealed items: non-returnable unless faulty. | The documents state that personalised or hygiene-sealed items are non-returnable unless faulty, matching the sentence exactly. |
| SUPPORTED | 27 | Separately, you have a 14-day statutory right to withdraw from your order for any reason, which always applies. | The document states a 14-day right of withdrawal for any reason, without needing an explanation, and says this statutory right always applies. |
| SUPPORTED | 27 | Personalised goods and hygiene-sealed items are exceptions to this right. | The documents list personalised goods and hygiene-sealed items as exceptions allowed by law to the 14-day right of withdrawal, though the sentence omits the 'once unsealed' qualifier. |
| UNSUPPORTED | 32, 26 | Faulty, damaged, or wrong items are covered by their own rules, even if they were on sale. | The documents say a faulty sale item is still covered, but they never state that damaged or wrong sale items are covered by their own rules even when on sale. |
| NOT_A_CLAIM | 26, 32, 27 (answer-level) | What type of item are you returning? | The sentence is a question back to the customer and states no policy fact. |
| NOT_A_CLAIM | 26, 32, 27 (answer-level) | I can give you a more specific answer. | The sentence is an offer to help further and states no policy fact. |

### Q2-corrupted — CORRUPTED on purpose: 'Northbound pays return shipping' -> 'customer pays', still cited to [35].

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 35, 22, 33 (answer-level) | Yes, you can likely get a full refund. | The documents allow a full refund for faulty, damaged, or wrong items reported within 30 days, and the sentence's hedge ('likely') avoids claiming eligibility beyond that. |
| SUPPORTED | 35 | Items that arrive faulty, damaged in transit, or not as ordered are covered: report the issue within 30 days for a free replacement or a full refund. | The documents state that faulty, damaged-in-transit, or wrong items are covered, with reporting within 30 days for a free replacement or full refund. |
| UNSUPPORTED | 35, 22, 33 (answer-level) | A ripped seam would generally count as faulty or damaged in transit. | The documents never say a ripped seam counts as faulty or damaged in transit, and a ripped seam could instead be normal wear or misuse, which the policy excludes after 30 days. |
| NOT_A_CLAIM | 35, 22, 33 (answer-level) | To make the claim: | The sentence is a bare lead-in ending with a colon and states no policy fact by itself. |
| UNSUPPORTED | 35 | Report it within 30 days of delivery. | The documents say to report the issue within 30 days but never specify that the period runs from delivery, so "of delivery" adds an unstated fact. |
| SUPPORTED | 35 | Include your order number and a photo of the issue. | The documents explicitly ask customers to include their order number and a photo of the issue when reporting a faulty or wrong item. |
| SUPPORTED | 22 | Also photograph the packaging, and keep it until the issue is resolved. | The documents say to take photos of the item and packaging and to keep the packaging until the issue is resolved, which matches the sentence. |
| UNSUPPORTED | 35 | You pay the return shipping yourself, and Northbound refunds it after inspection. | The documents say Northbound pays the return shipping for faulty, damaged, or wrong items and sends a free label, which contradicts the claim that the customer pays and gets it refunded after inspection. |
| SUPPORTED | 35 | If you're past 30 days, items are still covered for up to 2 years against manufacturing defects, though not damage from normal wear or misuse. | The documents state that beyond 30 days items are covered for up to 2 years against manufacturing defects, not damage from normal wear or misuse. |
| SUPPORTED | 33 | Even if the boots were marked "Final sale," your statutory rights for faulty goods still apply. | The documents state that items marked "Final sale" are not returnable but that statutory rights for faulty goods always still apply, which is exactly what the sentence says. |

### Q4-corrupted — CORRUPTED on purpose: free-shipping threshold €75 -> €40, still cited to [17].

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 16 | Delivery to Germany takes 2–3 business days after dispatch, and orders are dispatched within 1 business day. | The documents state Germany delivery is 2–3 business days counted from dispatch and that orders are dispatched within 1 business day, matching the sentence exactly. |
| SUPPORTED | 16 | Estimates may be longer during sale periods and public holidays. | The documents explicitly state that delivery estimates may be longer during sale periods and public holidays. |
| UNSUPPORTED | 16, 17 (answer-level) | Yes, a €45 order qualifies for free delivery. | The documents set free-shipping thresholds of €50 (Netherlands) and €75 (rest of EU), and the example explicitly says a €45 order pays shipping, so it does not qualify. |
| UNSUPPORTED | 17 | Free standard shipping to the rest of the EU applies on orders over €40. | The documents set the rest-of-EU free-shipping threshold at orders over €75, not €40, so the sentence contradicts them. |

### Q5-corrupted — CORRUPTED on purpose: 3 instalments -> 6, still cited to [07].

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| NOT_A_CLAIM | 07 (answer-level) | Yes. | The sentence is a bare affirmative with no policy fact stated. |
| UNSUPPORTED | 07 (answer-level) | Klarna pay-later is available, with two options: pay in 30 days, or pay in 6 interest-free instalments. | The documents say Klarna offers Pay in 3 interest-free instalments, not 6 instalments. |
| SUPPORTED | 07 | Both are subject to Klarna's approval, and you can see Klarna's terms at checkout. | The documents state that both Klarna options (Pay in 30 days and Pay in 3 instalments) are subject to Klarna's approval and that Klarna's terms are seen at checkout. |

