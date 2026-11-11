# Held-out faithfulness set — design notes (read AFTER labelling)

What each case in `faithfulness_holdout.json` was written to test. These are my intentions as author,
**not labels**: the labels are Stylianos's, set against the cited doc text. If a label disagrees
with the intent below, the label wins (and that disagreement is itself worth noting in DL16).

The over-claim patterns are deliberately **different** from the three v2 was tuned on
(Q1 scope-widening, Q2 an added condition "of delivery", Q3 "may → are").

| Case | Built as | Pattern tested | Doc text it hinges on |
|---|---|---|---|
| H1 | reasonable hedge | "It might not" — hedge backed by "may be excluded" | [10] "some items (for example, already-discounted products) may be excluded" |
| H2 | over-claim | **cross-doc blend**: a rule neither doc states (exchange difference → store credit) | [31] "we refund or charge the difference"; [34] store credit only "on request" / sale items |
| H3 | grounded | plain paraphrase | [11] |
| H4 | over-claim | **invented promise / SLA**: "5 business days", "replacement or refund" | [21] says only "we'll open an investigation with the carrier" |
| H5 | reasonable hedge | "You may be able to" — backed by "where the carrier offers it" | [24] |
| H6 | over-claim | **misapplying a rule to an excluded situation** (accidental damage), which v2's "apply the rule to the customer's case" instruction could wrongly wave through | [37] "does not cover … accidental damage" |
| H7 | grounded | plain paraphrase | [20] |
| H8 | over-claim | **answering from silence**: "points don't expire" when the doc says nothing about expiry | [49] "full points terms are on the rewards page" |

Mix: 2 grounded · 2 hedges that should pass · 4 over-claims (new patterns).
