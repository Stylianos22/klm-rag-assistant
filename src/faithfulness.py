"""Faithfulness check (Decision Log #16): is every claim backed by the doc it cites?

verify.py only checks that a cited id is real and was retrieved. This checks the
harder thing: does the cited document actually SAY what the sentence claims?

Method (LLM-as-judge, pinned):
1. Split the answer into sentences (one claim each); keep each sentence's own [id]s.
   A sentence with no [id] is judged against all docs the answer cites.
2. One judge call per sentence: the sentence + the full text of its cited doc(s)
   (+ the customer's question from judge v2 on; v1 stays pinned as the baseline).
   Verdict: SUPPORTED, UNSUPPORTED, or NOT_A_CLAIM (a question back, a greeting,
   or a remark that the docs don't cover something: nothing to verify).
3. An answer is grounded only if every claim is SUPPORTED.

The judge reuses generate.complete(): same pinned model, effort and client.
Faithful means "the cited doc states it", not "the answer is correct": a
correctly cited rule that doesn't apply to the customer still passes.
"""
import json
import re

import generate
from generate import KB, MODEL, EFFORT, complete, parse_citations

DEFAULT_JUDGE = "v2"

# v1 — pinned baseline (DL16 run 1 / first validation). Do not edit: its numbers are the baseline.
JUDGE_SYSTEM_V1 = (
    "You check whether one sentence from a customer-service answer is supported by "
    "store policy documents. Use ONLY the documents given; ignore your own knowledge.\n"
    "Verdicts:\n"
    "SUPPORTED: every fact in the sentence (numbers, time limits, conditions, who pays, "
    "what is or isn't allowed) is stated in the documents or follows directly from them.\n"
    "UNSUPPORTED: the sentence states at least one fact the documents do not state, or "
    "contradicts them.\n"
    "NOT_A_CLAIM: the sentence states no policy fact: a question back to the customer, "
    "a greeting, or a remark that the documents don't cover something.\n"
    'Reply with JSON only: {"verdict": "SUPPORTED" | "UNSUPPORTED" | "NOT_A_CLAIM", '
    '"reason": "<one short sentence>"}'
)

# v2 — the judge also sees the customer's question, so it judges the sentence as an answer
# to what was asked. Fixes v1's false flags (question echoes, values applied to the customer's
# case, backed hedges) while a broadened, strengthened or invented rule still fails.
JUDGE_SYSTEM_V2 = (
    "You check whether one sentence from a customer-service answer is supported by store "
    "policy documents. You get the customer's question, the sentence, and the documents it "
    "cites. Use ONLY the documents for policy facts; ignore your own knowledge.\n"
    "Judge the sentence as an answer to the question:\n"
    "- Details the customer gave in the question (the product, destination, order amount, "
    "timing) may be repeated; they are not policy claims.\n"
    "- Applying a document's rule or value to the customer's situation as described is "
    "supported (e.g. stating the shipping rate that the documents give for that destination "
    "and amount).\n"
    "- A hedged lead-in such as \"Yes, you can likely…\" is supported if the documents allow "
    "it in the customer's situation.\n"
    "Verdicts:\n"
    "SUPPORTED: every policy fact in the sentence is stated in the documents or follows "
    "directly from them for the situation in the question.\n"
    "UNSUPPORTED: the sentence states a policy fact the documents do not state, makes a rule "
    "broader or stronger than the documents (e.g. 'may' stated as 'are', a condition added "
    "or dropped, a rule extended to cases the documents don't name), or contradicts them.\n"
    "NOT_A_CLAIM: the sentence states no policy fact: a question back to the customer, a "
    "greeting, or a remark that the documents don't cover something.\n"
    'Reply with JSON only: {"verdict": "SUPPORTED" | "UNSUPPORTED" | "NOT_A_CLAIM", '
    '"reason": "<one short sentence>"}'
)
JUDGES = {
    "v1": {"version": "faithfulness-judge v1", "system": JUDGE_SYSTEM_V1, "uses_question": False},
    "v2": {"version": "faithfulness-judge v2", "system": JUDGE_SYSTEM_V2, "uses_question": True},
}
JUDGE_VERSION = JUDGES[DEFAULT_JUDGE]["version"]
VERDICTS = ("SUPPORTED", "UNSUPPORTED", "NOT_A_CLAIM")

_MARKER = re.compile(r"\s*\[\d{1,3}(?:\s*,\s*\d{1,3})*\]")
_BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+")


def split_claims(answer: str) -> list[str]:
    """One sentence per claim. Bullets and **bold** are stripped; a citation that
    lands after the full stop ("... refund. [35]") stays with its sentence."""
    claims: list[str] = []
    for line in answer.splitlines():
        line = _BULLET.sub("", line).replace("**", "").strip()
        if not line:
            continue
        for part in re.split(r"(?<=[.!?])\s+", line):
            part = part.strip()
            if not part:
                continue
            if claims and re.fullmatch(r"(\[\d{1,3}(?:\s*,\s*\d{1,3})*\]\s*)+[.]?", part):
                claims[-1] += " " + part      # a stray marker belongs to the sentence before
            else:
                claims.append(part)
    return claims


def _parse_verdict(text: str) -> tuple[str, str]:
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            v = str(d.get("verdict", "")).upper()
            if v in VERDICTS:
                return v, str(d.get("reason", ""))
        except json.JSONDecodeError:
            pass
    for v in VERDICTS:                       # fallback: a bare keyword
        if v in text.upper():
            return v, text.strip()[:200]
    return "UNSUPPORTED", f"unparseable judge reply: {text.strip()[:120]}"   # fail closed


def judge(claim: str, doc_ids: list[str], question: str | None = None, version: str = DEFAULT_JUDGE) -> dict:
    j = JUDGES[version]
    docs = "\n\n".join(f"[{d}] {KB[d][0]}:\n{KB[d][1]}" for d in doc_ids) or "(no documents cited)"
    user = f"Documents:\n\n{docs}\n\nSentence to check:\n{_MARKER.sub('', claim).strip()}"
    if j["uses_question"]:
        if not question:
            raise ValueError(f"judge {version} needs the customer's question")
        user = f"Customer's question:\n{question}\n\n{user}"
    verdict, reason = _parse_verdict(complete(j["system"], user))
    return {"verdict": verdict, "reason": reason, "usage": dict(generate.last_usage)}


def check(result: dict, question: str | None = None, version: str = DEFAULT_JUDGE) -> dict:
    """Judge every claim of one generate.answer() result.

    question: the customer's question (required by v2; falls back to result["question"]).
    Returns {grounded, claims: [{claim, cited_ids, supported, verdict, reason}], usage, judge}.
    supported is True/False for claims, None for NOT_A_CLAIM sentences.
    grounded is None for a refusal (nothing to check).
    """
    question = question or result.get("question")
    usage = {"input_tokens": 0, "output_tokens": 0}
    if result["refused"]:
        return {"grounded": None, "claims": [], "usage": usage, "judge": JUDGES[version]["version"]}
    answer_docs = [d for d in result["cited_ids"] if d in KB]
    claims = []
    for sentence in split_claims(result["answer"]):
        own = [d for d in parse_citations(sentence) if d in KB]
        j = judge(sentence, own or answer_docs, question, version)
        for k in usage:
            usage[k] += j["usage"][k]
        claims.append({
            "claim": _MARKER.sub("", sentence).strip(),
            "cited_ids": own or answer_docs,
            "cited_in_sentence": bool(own),
            "supported": None if j["verdict"] == "NOT_A_CLAIM" else j["verdict"] == "SUPPORTED",
            "verdict": j["verdict"],
            "reason": j["reason"],
        })
    judged = [c for c in claims if c["supported"] is not None]
    return {"grounded": all(c["supported"] for c in judged), "claims": claims, "usage": usage,
            "judge": JUDGES[version]["version"]}


def config(version: str = DEFAULT_JUDGE) -> dict:
    """What a re-run must hold fixed to reproduce a number."""
    return {"judge_model": MODEL, "judge_effort": EFFORT, "judge_version": JUDGES[version]["version"]}


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "Do you do pay-later, like Klarna?"
    r = generate.answer(q)
    print(r["answer"], "\n")
    f = check(r, question=q)
    for c in f["claims"]:
        print(f"  {c['verdict']:<12} {c['cited_ids']}  {c['claim'][:80]}  — {c['reason']}")
    print("grounded:", f["grounded"])
