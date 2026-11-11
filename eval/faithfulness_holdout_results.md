# Faithfulness check — held-out validation, judge v2 (DL16 C1)

Run 2026-11-10T16:57 · judge `claude-haiku-5-5` (effort medium) · faithfulness-judge v2 · prompt sha256 `568c148316dd` (frozen, untouched) · cases: `eval/faithfulness_holdout.json` (labels by Stylianos)

**Judge v2 on the held-out set: agreement 4/8 = 50% (bar ≥90%; in-sample was 100%) · unfaithful caught 2/4 · faithful passed 2/4 · cost ~$0.0018**

Report only: the judge was not tuned on this result. One run of a non-deterministic judge; 8 cases is a small sample, so one case moves agreement by 12.5 points.

## Results

| Case | Question | Label | Judge | Match | Claims flagged |
|---|---|---|---|---|---|
| H1 | Will my promo code work on a jacket that's already reduced? | faithful | faithful | ✅ | 0 |
| H2 | If I exchange my coat for a cheaper size, what happens to the difference? | unfaithful | unfaithful | ✅ | 1 |
| H3 | Can I spread a gift card over a few different orders? | faithful | faithful | ✅ | 0 |
| H4 | Tracking says my parcel was delivered but it's not here. What now? | faithful | unfaithful | ❌ | 1 |
| H5 | Can I collect my order from a pickup point instead of having it delivered to my house? | unfaithful | faithful | ❌ | 0 |
| H6 | The zip on my jacket broke after I caught it on a door handle. It's only 8 months old - is that covered? | unfaithful | unfaithful | ✅ | 1 |
| H7 | I won't be home when my parcel arrives tomorrow. What happens? | unfaithful | faithful | ❌ | 0 |
| H8 | Do my loyalty points run out if I don't use them? | faithful | unfaithful | ❌ | 1 |

## Per-claim verdicts

### H1 — label faithful

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 10 | It might not: some items, such as already-discounted products, may be excluded from promo codes. | The documents state that some items, such as already-discounted products, may be excluded from promo codes, and the sentence hedges with 'might' and 'may' accordingly. |
| SUPPORTED | 10 | Enter the code in the "promo code" box at checkout and you'll see whether the discount applies before you pay. | The document states to enter the code in the 'promo code' box at checkout and that the discount applies before payment, so the sentence's instruction and implication are supported. |

### H2 — label unfaithful

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 31 | Start the exchange in Your account → Returns. | The documents state that exchanges are started in Your account → Returns, so the sentence accurately reflects the stated procedure. |
| UNSUPPORTED | 31, 34 | Because the new item costs less, we'll refund the difference to you as store credit, which never expires. | Document 31 says only that the difference is refunded, with no method given, and Document 34 makes store credit an option the customer must ask for or a default only for sale items, which the coat isn't stated to be. |

### H3 — label faithful

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 11 | Yes: the gift card balance can be used across several orders, and it stays valid for 24 months. | The documents state the balance can be used across several orders and is valid for 24 months, so the sentence matches the policy. |
| SUPPORTED | 11 | It can't be exchanged for cash, though. | The documents state that gift cards can't be exchanged for cash, so the sentence accurately restates that policy fact. |

### H4 — label faithful

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 21 | First check with your neighbours and anyone in your household, and look at the carrier's proof of delivery. | The sentence accurately restates the document's first steps: check with neighbours and household members and review the carrier's proof of delivery. |
| SUPPORTED | 21 | If it's still missing, contact us within 14 days and we'll open an investigation with the carrier. | The sentence matches document [21]: if still missing, contact within 14 days and an investigation with the carrier is opened. |
| UNSUPPORTED | 21 | Most investigations are wrapped up within 5 business days, after which we send a replacement or a refund. | The documents mention no 5-business-day timeline and no replacement or refund outcome after an investigation; they only say contact within 14 days to open an investigation with the carrier. |

### H5 — label unfaithful

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 24 | You may be able to: where the carrier offers it, you can choose a nearby pickup point at checkout. | The hedged lead-in 'You may be able to' is allowed, and the policy that pickup points are available where the carrier offers it, chosen at checkout, is stated in document [24]. |
| SUPPORTED | 24 | You'll get a notification when it's ready, and you might be asked to show ID along with your collection code. | The documents state that a notification is sent when the parcel is ready and that the collection code and ID may be requested, and the sentence's 'might be asked' matches the document's 'if asked'. |

### H6 — label unfaithful

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| UNSUPPORTED | 37 | Yes: products are covered against defects for up to 2 years under EU law, so at 8 months your jacket is still within the warranty and we can arrange a repair or replacement. | The documents exclude accidental damage, and catching the zip on a door handle is likely accidental damage, yet the sentence states the jacket is covered without that condition and promises repair or replacement, which the cited document doesn't state. |

### H7 — label unfaithful

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| SUPPORTED | 20 | Depending on the carrier, they'll either try again, leave a card, or divert your parcel to a nearby pickup point. | The sentence restates the document's rule that the carrier will retry, leave a card, or divert to a nearby pickup point depending on the carrier, which matches the policy text directly. |
| SUPPORTED | 20 | Your tracking link has the instructions to reschedule or collect it. | The documents state to follow the instructions in the tracking link to reschedule or collect the parcel, so the sentence restates that policy accurately. |

### H8 — label faithful

| Verdict | Cited | Claim | Judge's reason |
|---|---|---|---|
| UNSUPPORTED | 49 | No: your loyalty points don't expire, so you can save them up and redeem them for discounts whenever you like. | The documents only say the full terms are on the rewards page and do not state that points never expire, so the 'don't expire' claim is not supported. |
| SUPPORTED | 49 | Joining is free through your account. | The documents state that joining the loyalty programme is free through your account. |

