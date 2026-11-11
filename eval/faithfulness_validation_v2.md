# Faithfulness check — validation, judge v2 (DL16 C1)

Run 2026-11-10T15:28 · judge `claude-haiku-5-5` (effort medium) · faithfulness-judge v2 · cases: `eval/faithfulness_cases.json` (labels corrected 2026-11-10)

**Judge v2: agreement 10/10 = 100% (bar ≥90%) · corrupted caught 4/4 = 100% (bar 100%; the injected claim itself must be flagged) · real answers 6/6 · judge cost ~$0.0119 → C1 MET**

**Baseline (v1, not re-run):** 6/10 = 60% against the original labels (`eval/faithfulness_validation.md`); the same recorded v1 verdicts score 9/10 = 90% against the corrected labels.

One run of a non-deterministic judge: re-run before quoting a number as stable.

## Label changes

| Case | From → to | Claim | Cited doc says | Reason |
|---|---|---|---|---|
| Q1-real | faithful → unfaithful | Faulty, damaged, or wrong items are covered by their own rules, even if they were on sale [32][26]. | [32] "Your statutory rights for faulty goods are unaffected by this — a faulty sale item is still covered." · [26] "Faulty, damaged or wrong items — see \"Faulty, defective or wrong item\"." | Scope widened: doc 32 keeps only FAULTY sale items covered; 'damaged or wrong … even if on sale' is not stated (doc 26 backs only the 'own rules' half). |
| Q2-real | faithful → unfaithful | Report it within 30 days of delivery [35]. | [35] "Report it within 30 days for a free replacement or a full refund." | Condition added: doc 35 gives a 30-day window but never anchors it to delivery. |
| Q3-real | faithful → unfaithful | Sale items are refunded as store credit only, not to your original payment method [30]. | [30] "Sale items may be refunded as store credit only — see \"Sale & clearance items\"." | Strengthened 'may' to 'are': the cited doc 30 does not state it flatly (doc 32 does, but was not cited). |

## Results

| Case | Label | Predicted | Match | Claims judged | Unsupported | Injected claim flagged |
|---|---|---|---|---|---|---|
| Q1-real | unfaithful | unfaithful | ✅ | 10 | 1 | — |
| Q2-real | unfaithful | unfaithful | ✅ | 10 | 1 | — |
| Q3-real | unfaithful | unfaithful | ✅ | 6 | 1 | — |
| Q4-real | faithful | faithful | ✅ | 5 | 0 | — |
| Q5-real | faithful | faithful | ✅ | 3 | 0 | — |
| Q6-real | faithful | faithful | ✅ | 7 | 0 | — |
| Q1-corrupted | unfaithful | unfaithful | ✅ | 10 | 2 | ✅ |
| Q2-corrupted | unfaithful | unfaithful | ✅ | 9 | 2 | ✅ |
| Q4-corrupted | unfaithful | unfaithful | ✅ | 4 | 2 | ✅ |
| Q5-corrupted | unfaithful | unfaithful | ✅ | 3 | 1 | ✅ |

## Per-claim verdicts

### Q1-real — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 26 | For most items, you have 30 days from delivery to return them for a refund. | The documents state that most items can be returned within 30 days of delivery for a refund, which the sentence accurately reflects. |
| SUPPORTED | 26 | The item must be unused, in original condition, with tags and original packaging. | The documents state that to qualify for return, items must be unused, in original condition, with tags and original packaging. |
| SUPPORTED | 26 | You can start a return from Your account → Returns. | The documents state that a return is started from Your account → Returns. |
| SUPPORTED | 26, 32, 27 (answer-level) | Some items have different rules: | The documents state that sale/clearance items and faulty/damaged/wrong items are handled differently, and personalised or hygiene-sealed items have exceptions, so the general statement that some items have different rules is accurate. |
| SUPPORTED | 32 | Regular sale or discounted items: returnable within 14 days of delivery, refunded as store credit only. | The documents state that regular sale or discounted items are returnable within 14 days of delivery and refunded as store credit only. |
| SUPPORTED | 32 | Clearance or items marked "Final sale": not returnable. | The documents state that clearance items and items marked 'Final sale' are not returnable, and the sentence repeats this directly without adding conditions or extending the rule beyond the document's wording. |
| SUPPORTED | 26 | Personalised or hygiene-sealed items: non-returnable unless faulty. | The documents state that personalised or hygiene-sealed items are non-returnable unless faulty, matching the sentence exactly. |
| SUPPORTED | 27 | Separately, you have a 14-day statutory right to withdraw from your order for any reason, which always applies. | The documents state a 14-day statutory right to cancel for any reason and say this right always applies, so the sentence matches them. |
| SUPPORTED | 27 | Personalised goods and hygiene-sealed items are exceptions to this right. | The document states that exceptions allowed by law include personalised goods and hygiene-sealed items once unsealed, so the sentence accurately reflects the stated exceptions to the 14-day right. |
| UNSUPPORTED | 32, 26 | Faulty, damaged, or wrong items are covered by their own rules, even if they were on sale. | The documents say only that faulty sale items remain covered, not that damaged or wrong sale items are also exempt from the sale rules, so the sentence extends that rule beyond what is stated. |
| NOT_A_CLAIM | 26, 32, 27 (answer-level) | What type of item are you returning? | The sentence is a question back to the customer and states no policy fact. |
| NOT_A_CLAIM | 26, 32, 27 (answer-level) | I can give you a more specific answer. | The sentence is a remark about answering further, stating no policy fact from the documents. |

### Q2-real — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 35, 22, 33 (answer-level) | Yes, you can likely get a full refund. | A faulty item reported within 30 days qualifies for a full refund or free replacement, and the hedged "likely" fits a ripped seam that the customer reports on arrival. |
| SUPPORTED | 35 | Items that arrive faulty, damaged in transit, or not as ordered are covered: report the issue within 30 days for a free replacement or a full refund. | The documents state that faulty, damaged, or wrong items are covered, with reporting within 30 days for a free replacement or full refund, which the sentence accurately restates. |
| SUPPORTED | 35, 22, 33 (answer-level) | A ripped seam would generally count as faulty or damaged in transit. | The documents cover items that arrive faulty, damaged in transit, or not as ordered, and a seam that is ripped on arrival follows directly from that, with the hedge 'generally' keeping the claim modest. |
| NOT_A_CLAIM | 35, 22, 33 (answer-level) | To make the claim: | The sentence is only a lead-in phrase ('To make the claim:') that states no policy fact by itself. |
| UNSUPPORTED | 35 | Report it within 30 days of delivery. | The documents say to report within 30 days but never specify that the period runs from delivery, so 'of delivery' adds a condition the policy doesn't state. |
| SUPPORTED | 35 | Include your order number and a photo of the issue. | The documents say to include the order number and a photo of the issue to speed things up, so the sentence states a documented request accurately. |
| SUPPORTED | 22 | Also photograph the packaging, and keep it until the issue is resolved. | Document 22 says to take photos of the item and packaging and to keep the packaging until the issue is resolved, so the sentence matches it. |
| SUPPORTED | 35, 22, 33 (answer-level) | Return shipping is free. | The boots arrived faulty, and the faulty-item section states that Northbound pays return shipping and sends a free label, so free return shipping applies to this situation. |
| SUPPORTED | 35 | Northbound sends a prepaid label. | The documents state that Northbound pays return shipping and sends a free label, which is equivalent to a prepaid label for a faulty item reported within 30 days. |
| SUPPORTED | 35 | If you're past 30 days, items are still covered for up to 2 years against manufacturing defects, though not damage from normal wear or misuse. | The documents state that beyond 30 days items are covered for up to 2 years against manufacturing defects, not damage from normal wear or misuse, which matches the sentence. |
| SUPPORTED | 33 | Even if the boots were marked "Final sale," your statutory rights for faulty goods still apply. | The documents state that items marked "Final sale" are not returnable but that statutory rights for faulty goods always still apply, which is exactly what the sentence says. |

### Q3-real — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| UNSUPPORTED | 30 | Sale items are refunded as store credit only, not to your original payment method. | The document says sale items *may* be refunded as store credit only, and points to a section not provided, whereas the sentence states flatly that they are refunded as store credit and never to the original payment method. |
| SUPPORTED | 34 | Store credit is added to your account and does not expire. | Document [34] states that store credit is added to the customer's account and does not expire. |
| SUPPORTED | 30 | For postage, return postage is not refunded for change-of-mind returns. | The documents state that return postage is not refunded for change-of-mind returns, and the sentence states that rule accurately without broadening it. |
| SUPPORTED | 26 | Your return is within the 30-day window if it was delivered recently enough, since returns are accepted within 30 days of delivery. | The documents state the 30-day window runs from delivery, and a purchase about 3 weeks ago falls within it; the sentence makes no claim about the sale-item exceptions. |
| SUPPORTED | 26 | The items must be unused, in original condition, with tags and original packaging. | {"verdict": "SUPPORTED", "reason": "The returns policy document states that to qualify, items must be unused, in original condition, with tags and original packaging.", "}"} |
| SUPPORTED | 26 | You can start the return from Your account → Returns. | The documents state that a return is started from Your account → Returns, which the sentence correctly repeats as a general instruction without adding conditions. |
| NOT_A_CLAIM | 30, 34, 26 (answer-level) | My documents don't include the full "Return shipping: who pays" article or the "Sale & clearance items: return exceptions" article, so I can't confirm any other conditions that apply to sale items. | The sentence only states that the provided documents lack certain articles and that other sale-item conditions cannot be confirmed, which is a remark about document coverage rather than a policy fact. |

### Q4-real — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 16 | Delivery to Germany takes 2–3 business days after dispatch, and orders are dispatched within 1 business day. | The documents state Germany delivery is 2–3 business days counted from dispatch and that orders are dispatched within 1 business day, matching the sentence. |
| SUPPORTED | 16 | Estimates may be longer during sale periods and public holidays. | The documents state that estimates may be longer during sale periods and public holidays, matching the sentence's hedged wording. |
| SUPPORTED | 16, 17 (answer-level) | You won't get free delivery on a €45 order. | The documents state Germany falls under 'Rest of the EU' with free shipping only on orders over €75, and the example explicitly says a €45 order to Germany pays €6.95 shipping, so no free delivery applies. |
| SUPPORTED | 17 | Free standard shipping to the rest of the EU applies only on orders over €75. | Document 17 states free shipping to the rest of the EU applies on orders over €75, and the sentence accurately reflects that threshold. |
| SUPPORTED | 17 | Your order would be charged the standard EU rate of €6.95. | Document 17 states that a €45 order to Germany (within the EU, below the €75 threshold) incurs standard EU shipping of €6.95. |

### Q5-real — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 07 (answer-level) | Yes. | The documents list Klarna pay-later options (pay in 30 days or 3 interest-free instalments), so the answer "Yes" to the question is supported. |
| SUPPORTED | 07 (answer-level) | Klarna pay-later is available, with two options: pay in 30 days, or pay in 3 interest-free instalments. | The documents list Klarna pay-later with exactly the two options stated (pay in 30 days, or pay in 3 interest-free instalments), and the sentence omits only the approval condition rather than adding a stronger claim. |
| SUPPORTED | 07 | Both are subject to Klarna's approval, and you can see Klarna's terms at checkout. | The documents state Klarna pay-later options (Pay in 30 days or Pay in 3 interest-free instalments) are subject to Klarna's approval and that Klarna's terms are seen at checkout, so the sentence matches. |

### Q6-real — Real answer from eval/generation_results.md (run 2026-10-29). Label = faithful per Stylianos's brief; human approval column not yet filled.

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 26 (answer-level) | Yes, you can likely return it. | The documents allow returning most items for a change of mind within 30 days of delivery, and the hedged "likely" fits the unknown item type and timing. |
| SUPPORTED | 26 | Northbound's policy allows most items to be returned within 30 days of delivery for a refund. | The documents state that most items can be returned within 30 days of delivery for a refund under Northbound's own policy, and the sentence says exactly that. |
| SUPPORTED | 26 | The item must be unused, in original condition, with tags and original packaging. | The documents state that to qualify for return, items must be unused, in original condition, with tags and original packaging. |
| SUPPORTED | 26 | You can start a return from Your account → Returns. | {"verdict": "SUPPORTED", "reason": "The documents state that returns are started from Your account → Returns, so the sentence accurately reflects the policy.", "" : ""}

Correction to the format: the  |
| SUPPORTED | 26 (answer-level) | A few items are handled differently. | The documents state that some items are handled differently, and "a few" is a close paraphrase of "some" that doesn't change the substance. |
| SUPPORTED | 26 | Personalised or hygiene-sealed items can't be returned unless they're faulty. | The documents state that personalised or hygiene-sealed items are non-returnable unless faulty, which the sentence restates accurately. |
| SUPPORTED | 26 | Sale and clearance items have their own return exceptions, but I don't have those details here. | The documents state that sale and clearance items are handled differently and point to a separate return-exceptions article, and the sentence's admission that those details aren't included here is accurate. |
| NOT_A_CLAIM | 26 (answer-level) | I don't have information on who pays return postage for change-of-mind returns, or on how refunds are issued. | The sentence only says the assistant lacks information on postage and refunds, which the documents explicitly leave to separate articles, so it states no policy fact. |

### Q1-corrupted — CORRUPTED on purpose: 30 days -> 60 days, still cited to [26] (doc 26 says 30).

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| UNSUPPORTED | 26 | For most items, you have 60 days from delivery to return them for a refund. | The documents state a 30-day window from delivery for most items, not 60 days. |
| SUPPORTED | 26 | The item must be unused, in original condition, with tags and original packaging. | The documents state that to qualify for return, items must be unused, in original condition, with tags and original packaging. |
| SUPPORTED | 26 | You can start a return from Your account → Returns. | The documents state that returns are started from Your account → Returns. |
| SUPPORTED | 26, 32, 27 (answer-level) | Some items have different rules: | The documents state that sale/clearance items and faulty/damaged/wrong items are handled differently, and personalised or hygiene-sealed items are also exceptions, so the general statement that some items have different rules is accurate. |
| SUPPORTED | 32 | Regular sale or discounted items: returnable within 14 days of delivery, refunded as store credit only. | The documents state that regular sale/discounted items are returnable within 14 days of delivery and refunded as store credit only, matching the sentence exactly. |
| SUPPORTED | 32 | Clearance or items marked "Final sale": not returnable. | {"verdict": "SUPPORTED", "reason": "The documents state that clearance items and items marked \"Final sale\" are not returnable, and the sentence repeats that rule without broadening it (though it omi |
| SUPPORTED | 26 | Personalised or hygiene-sealed items: non-returnable unless faulty. | The documents state that personalised or hygiene-sealed items are non-returnable unless faulty, matching the sentence exactly. |
| SUPPORTED | 27 | Separately, you have a 14-day statutory right to withdraw from your order for any reason, which always applies. | The documents state the 14-day statutory right to cancel for any reason and say it always applies, which the sentence repeats. |
| SUPPORTED | 27 | Personalised goods and hygiene-sealed items are exceptions to this right. | The document states that exceptions allowed by law include personalised goods and hygiene-sealed items once unsealed, which matches the sentence's claim that they are exceptions to the withdrawal right. |
| UNSUPPORTED | 32, 26 | Faulty, damaged, or wrong items are covered by their own rules, even if they were on sale. | The documents explicitly say only faulty sale items remain covered, while damaged or wrong sale items are not stated to be covered 'even if on sale', so the sentence extends that rule beyond what is written. |
| NOT_A_CLAIM | 26, 32, 27 (answer-level) | What type of item are you returning? | The sentence is a question back to the customer and states no policy fact. |
| NOT_A_CLAIM | 26, 32, 27 (answer-level) | I can give you a more specific answer. | The sentence is a remark about the answer's own specificity and states no policy fact about the return window. |

### Q2-corrupted — CORRUPTED on purpose: 'Northbound pays return shipping' -> 'customer pays', still cited to [35].

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 35, 22, 33 (answer-level) | Yes, you can likely get a full refund. | The documents say a faulty or damaged item reported within 30 days gets a free replacement or a full refund, and the hedged "likely" fits a ripped seam reported as damage on arrival. |
| SUPPORTED | 35 | Items that arrive faulty, damaged in transit, or not as ordered are covered: report the issue within 30 days for a free replacement or a full refund. | The documents state that faulty, damaged, or wrong items are covered, with reporting within 30 days for a free replacement or full refund, which matches the sentence. |
| SUPPORTED | 35, 22, 33 (answer-level) | A ripped seam would generally count as faulty or damaged in transit. | A boot arriving with a ripped seam is an item that arrived faulty or damaged, which the policy covers, so the hedged classification follows from the documents' rule. |
| NOT_A_CLAIM | 35, 22, 33 (answer-level) | To make the claim: | The sentence is only a lead-in phrase ('To make the claim:') that states no policy fact by itself. |
| UNSUPPORTED | 35 | Report it within 30 days of delivery. | The documents say to report within 30 days but never state that the period runs from delivery, so 'of delivery' adds a condition the policy does not specify. |
| SUPPORTED | 35 | Include your order number and a photo of the issue. | The documents say to include the order number and a photo of the issue to speed things up, so the sentence accurately states this request. |
| SUPPORTED | 22 | Also photograph the packaging, and keep it until the issue is resolved. | Document [22] says to take photos of the item and packaging and to keep the packaging until the issue is resolved, so the sentence matches. |
| UNSUPPORTED | 35 | You pay the return shipping yourself, and Northbound refunds it after inspection. | The documents say Northbound pays return shipping and sends a free label for faulty items, contradicting the claim that the customer pays return shipping; the 'refunds it after inspection' part is also not stated. |
| SUPPORTED | 35 | If you're past 30 days, items are still covered for up to 2 years against manufacturing defects, though not damage from normal wear or misuse. | The documents state that beyond 30 days items are covered for up to 2 years against manufacturing defects, not damage from normal wear or misuse, which the sentence accurately restates for a customer past 30 days. |
| SUPPORTED | 33 | Even if the boots were marked "Final sale," your statutory rights for faulty goods still apply. | The documents say final-sale items are not returnable but that statutory rights for faulty goods always still apply, which is what the sentence states. |

### Q4-corrupted — CORRUPTED on purpose: free-shipping threshold €75 -> €40, still cited to [17].

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 16 | Delivery to Germany takes 2–3 business days after dispatch, and orders are dispatched within 1 business day. | The documents state that Germany delivery is 2–3 business days counted from dispatch and that orders are dispatched within 1 business day, matching the sentence. |
| SUPPORTED | 16 | Estimates may be longer during sale periods and public holidays. | The documents explicitly state that estimates may be longer during sale periods and public holidays. |
| UNSUPPORTED | 16, 17 (answer-level) | Yes, a €45 order qualifies for free delivery. | The documents state that a €45 order to Germany is below the €75 EU free-shipping threshold and incurs €6.95 shipping, so claiming free delivery contradicts them. |
| UNSUPPORTED | 17 | Free standard shipping to the rest of the EU applies on orders over €40. | The documents set the rest-of-EU free-shipping threshold at orders over €75, not €40, and a €45 order to Germany pays €6.95 shipping. |

### Q5-corrupted — CORRUPTED on purpose: 3 instalments -> 6, still cited to [07].

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 07 (answer-level) | Yes. | The documents list Klarna as a pay-later option (pay in 30 days or in 3 interest-free instalments), so answering "Yes" to whether they offer pay-later is supported. |
| UNSUPPORTED | 07 (answer-level) | Klarna pay-later is available, with two options: pay in 30 days, or pay in 6 interest-free instalments. | The documents say Klarna offers pay in 3 interest-free instalments, not 6 instalments. |
| SUPPORTED | 07 | Both are subject to Klarna's approval, and you can see Klarna's terms at checkout. | The documents state that both Klarna options (pay in 30 days and pay in 3 instalments) are subject to Klarna's approval and direct customers to Klarna's terms at checkout. |

