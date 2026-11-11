# Generation eval — grounded, cited answers (DL15)

Run 2026-10-29 · model `claude-haiku-5-5` (effort medium) · top-3 docs from the current retriever (score gate off; the model decides to refuse) · frozen `eval/queries.json` unchanged.

**Auto checks:** `citation_ok` = every cited id is a real KB doc and was retrieved, and an answer has at least one citation. Edge behaviour = Q9/Q10 refuse, Q8 cites the tracking/account doc (18/04), Q7 asks a clarifying question.  
**Human check (fill in):** for each answer — is it correct, does every cited doc actually support its claim, and is nothing invented (Q8: no made-up order status)? Mark yes/no.

## Summary

| Query | Type | Gold in top-3 | Cited | Retrieved | citation_ok | Edge behaviour | Tokens in/out | Cost (USD) | Human-approved (yes/no) |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | answerable | ✅ | 26, 32, 27 | 26, 27, 32 | ✅ | — | 784/713 | 0.00043 | ✅ yes |
| Q2 | answerable | ✅ | 35, 22, 33 | 35, 22, 33 | ✅ | — | 530/493 | 0.00030 | ✅ yes |
| Q3 | answerable-multidoc | ❌ | 30, 34, 26 | 30, 34, 26 | ✅ | — | 702/832 | 0.00049 | ❌ no — sale 14-day doc 32 not retrieved |
| Q4 | answerable-multidoc | ✅ | 16, 17 | 16, 15, 17 | ✅ | — | 611/224 | 0.00017 | ✅ yes |
| Q5 | answerable | ✅ | 07 | 07, 30, 34 | ✅ | — | 633/157 | 0.00014 | ✅ yes |
| Q6 | answerable | ❌ | 26 | 35, 26, 22 | ✅ | — | 684/359 | 0.00025 | ✅ yes — correct via doc 26 |
| Q7 | ambiguous-should-clarify | — | — | 33, 26, 28 | ✅ | ✅ ask one clarifying question | 561/303 | 0.00021 | — clarify |
| Q8 | out-of-kb-live-data | — | 18, 02 | 18, 02, 22 | ✅ | ✅ redirect to tracking/account (18/04) | 388/348 | 0.00021 | — redirect |
| Q9 | out-of-kb-absent | — | — | 31, 12, 32 | ✅ | ✅ refuse | 470/153 | 0.00012 | — refuse |
| Q10 | out-of-kb-domain | — | — | 44, 40, 26 | ✅ | ✅ refuse | 514/9 | 0.00006 | — refuse |

**Citations OK:** 10/10 (target 100%) · **Edge behaviour OK:** 4/4 · **Total cost:** ~$0.0024 for 10 queries (~$0.00024/query; 5877 in / 3591 out tokens)  
**Answer approval:** 5 / 6 answerable = **83%** (target >70%) — only Q3 missed, and for a retrieval reason (sale-exceptions doc 32 not retrieved), not a generation one.

## Answers

### Q1 — How long do I have to return something?

> For most items, you have **30 days from delivery** to return them for a refund [26]. The item must be unused, in original condition, with tags and original packaging [26]. You can start a return from **Your account → Returns** [26].
> 
> Some items have different rules:
> - **Regular sale or discounted items:** returnable within **14 days** of delivery, refunded as **store credit only** [32].
> - **Clearance or items marked "Final sale":** **not returnable** [32].
> - **Personalised or hygiene-sealed items:** non-returnable unless faulty [26].
> 
> Separately, you have a **14-day statutory right to withdraw** from your order for any reason, which always applies [27]. Personalised goods and hygiene-sealed items are exceptions to this right [27].
> 
> Faulty, damaged, or wrong items are covered by their own rules, even if they were on sale [32][26].
> 
> What type of item are you returning? I can give you a more specific answer.

Retrieved: [26] Returns policy & window, [27] EU right of withdrawal (14-day), [32] Sale & clearance items — return exceptions  
Cited: 26, 32, 27 · citation_ok ✅

### Q2 — The boots I ordered turned up with a ripped seam - can I get my money back?

> Yes, you can likely get a full refund. Items that arrive faulty, damaged in transit, or not as ordered are covered: report the issue within 30 days for a free replacement or a full refund [35]. A ripped seam would generally count as faulty or damaged in transit.
> 
> To make the claim:
> - **Report it within 30 days** of delivery [35].
> - **Include your order number and a photo** of the issue [35]. Also photograph the packaging, and keep it until the issue is resolved [22].
> - **Return shipping is free.** Northbound sends a prepaid label [35].
> 
> If you're past 30 days, items are still covered for up to 2 years against manufacturing defects, though not damage from normal wear or misuse [35].
> 
> Even if the boots were marked "Final sale," your statutory rights for faulty goods still apply [33].

Retrieved: [35] Faulty, defective or wrong item, [22] Damaged in transit, [33] Final-sale & non-returnable items  
Cited: 35, 22, 33 · citation_ok ✅

### Q3 — I'm sending back a sale item I bought about 3 weeks ago - do I get a refund or store credit, and who pays the return postage?

> Sale items are refunded as **store credit only**, not to your original payment method [30]. Store credit is added to your account and does not expire [34].
> 
> For postage, return postage is **not refunded for change-of-mind returns** [30]. Your return is within the 30-day window if it was delivered recently enough, since returns are accepted within 30 days of delivery [26]. The items must be unused, in original condition, with tags and original packaging [26]. You can start the return from **Your account → Returns** [26].
> 
> My documents don't include the full "Return shipping: who pays" article or the "Sale & clearance items: return exceptions" article, so I can't confirm any other conditions that apply to sale items.

Retrieved: [30] Refunds — method & timing, [34] Store credit & return vouchers, [26] Returns policy & window  
Cited: 30, 34, 26 · citation_ok ✅

### Q4 — Shipping to Germany - how long does it take, and do I get free delivery on a 45 euro order?

> Delivery to Germany takes **2–3 business days** after dispatch, and orders are dispatched within 1 business day [16]. Estimates may be longer during sale periods and public holidays [16].
> 
> You won't get free delivery on a €45 order. Free standard shipping to the rest of the EU applies only on orders over €75 [17]. Your order would be charged the standard EU rate of €6.95 [17].

Retrieved: [16] International shipping times, [15] Domestic shipping (Netherlands), [17] Shipping costs & free-shipping threshold  
Cited: 16, 17 · citation_ok ✅

### Q5 — Do you do pay-later, like Klarna?

> Yes. Klarna pay-later is available, with two options: pay in 30 days, or pay in 3 interest-free instalments. Both are subject to Klarna's approval, and you can see Klarna's terms at checkout [07].

Retrieved: [07] Payment methods, [30] Refunds — method & timing, [34] Store credit & return vouchers  
Cited: 07 · citation_ok ✅

### Q6 — Nothing's actually wrong with it, I just changed my mind - can I still send it back?

> Yes, you can likely return it. Northbound's policy allows most items to be returned within **30 days of delivery** for a refund [26]. The item must be unused, in original condition, with tags and original packaging [26]. You can start a return from **Your account → Returns** [26].
> 
> A few items are handled differently. Personalised or hygiene-sealed items can't be returned unless they're faulty [26]. Sale and clearance items have their own return exceptions [26], but I don't have those details here.
> 
> I don't have information on who pays return postage for change-of-mind returns, or on how refunds are issued.

Retrieved: [35] Faulty, defective or wrong item, [26] Returns policy & window, [22] Damaged in transit  
Cited: 26 · citation_ok ✅

### Q7 — Can I return it?

> Which item do you want to return? Let me know what it is and whether it's personalised, from a sale or clearance, or faulty, since those affect whether it can be returned.

Retrieved: [33] Final-sale & non-returnable items, [26] Returns policy & window, [28] How to start a return  
Cited: — · citation_ok ✅

### Q8 — Where's my order #48213? It's been a week.

> I can't look up the status of a specific order over chat. Your shipping confirmation includes a tracking link, and you can also see the status under Your account → Orders [18].
> 
> If you can't find a tracking link or the order isn't showing in your account, contact support by email at support@northbound.example or through live chat. Support hours are Monday–Friday, 09:00–17:00 CET, and replies usually come within one business day. Have your order number ready to speed things up [02].

Retrieved: [18] Tracking your order, [02] Contact us & support hours, [22] Damaged in transit  
Cited: 18, 02 · citation_ok ✅

### Q9 — Do you price-match other shops if I find it cheaper?

> I don't have that information.

Retrieved: [31] Exchanges, [12] Prices, currency & VAT, [32] Sale & clearance items — return exceptions  
Cited: — · citation_ok ✅

### Q10 — Which of your laptops is best for gaming?

> I don't have that information.

Retrieved: [44] Cookie policy, [40] Stock availability & restocks, [26] Returns policy & window  
Cited: — · citation_ok ✅

