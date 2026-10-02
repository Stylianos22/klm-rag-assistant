"""
KLM RAG — retrieval spike (reference).
Proved the stack on the 9 gold docs: embed TITLE + body, cosine, top-3.
Body-only = 67% retrieval; title+body = 100%. Out-of-KB abstains (<0.35).
Run: pip install sentence-transformers numpy ; python spike.py
This is a throwaway probe. The real pipeline goes in ../src/ (see ../CLAUDE.md).
"""
import numpy as np
from sentence_transformers import SentenceTransformer

# For the real build, load these from ../KB/*.md instead of inlining.
DOCS = {
 "07 Payment methods": "Visa, Mastercard, Amex; PayPal; Apple/Google Pay; Klarna pay later (Pay in 30 days or 3 instalments). 3-D Secure. EUR.",
 "16 International shipping times": "Dispatch within 1 business day. NL 1-2 days; BE/DE/LU 2-3; rest of EU 3-7; non-EU Europe 5-10. Tracking emailed.",
 "17 Shipping costs & free shipping": "NL standard 4.95 euro, free over 50. EU standard 6.95 euro, free over 75. No EU customs; outside EU may pay duties.",
 "26 Returns policy & window": "Change-of-mind returns within 30 days of delivery, unused with tags. More generous than the 14-day legal minimum.",
 "27 EU right of withdrawal 14-day": "EU 14-day right of withdrawal: cancel for any reason within 14 days of receiving goods. Refund incl. standard outbound shipping.",
 "29 Return shipping who pays": "Change of mind: customer pays return postage (4.95 label or own courier). Faulty/wrong: Northbound pays.",
 "30 Refunds method & timing": "Refund to original payment method within 14 days of receiving the return. Store credit on request. Sale items store-credit only.",
 "32 Sale & clearance items return exceptions": "Sale items returnable within 14 days, store credit only. Clearance/Final sale not returnable. Faulty rights unaffected.",
 "35 Faulty, defective or wrong item": "Faulty/damaged/wrong item: report within 30 days for free replacement or refund; Northbound pays return. 2-year defect cover.",
}
QUERIES = [
 ("Q1","How long do I have to return something?", ["26 Returns policy & window"]),
 ("Q2","The boots I ordered turned up with a ripped seam - can I get my money back?", ["35 Faulty, defective or wrong item"]),
 ("Q3","Sending back a sale item I bought 3 weeks ago - refund or store credit, and who pays return postage?", ["32 Sale & clearance items return exceptions","30 Refunds method & timing","29 Return shipping who pays"]),
 ("Q4","Shipping to Germany - how long, and free delivery on a 45 euro order?", ["16 International shipping times","17 Shipping costs & free shipping"]),
 ("Q5","Do you do pay-later, like Klarna?", ["07 Payment methods"]),
 ("Q6","Nothing's wrong, I just changed my mind - can I still send it back?", ["27 EU right of withdrawal 14-day"]),
 ("Q9","Do you price-match other shops?", None),
 ("Q10","Which laptop is best for gaming?", None),
]
K, ABSTAIN = 3, 0.35
m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
names = list(DOCS)
# KEY LESSON: embed title + body, not body alone.
emb = m.encode([n + ". " + DOCS[n] for n in names], normalize_embeddings=True)
hits = tot = 0
for qid, q, gold in QUERIES:
    qe = m.encode([q], normalize_embeddings=True)[0]
    order = np.argsort(-(emb @ qe))[:K]
    top = [(names[i], float((emb @ qe)[i])) for i in order]
    tn = [t[0] for t in top]
    if gold is None:
        print(qid, "OUT-OF-KB -> abstain" if top[0][1] < ABSTAIN else "OUT-OF-KB -> RISK answer", round(top[0][1],2))
    else:
        tot += 1; ok = all(g in tn for g in gold); hits += ok
        print(qid, "HIT" if ok else "MISS", [n.split()[0] for n in tn])
print(f"retrieval {hits}/{tot} = {round(100*hits/tot)}%")
