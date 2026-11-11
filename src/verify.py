"""Citation gate (the brief's 100% citation target).

Automatic: every cited id must be a real KB doc AND one of the docs retrieved for
this query. An answer (not a refusal, not a clarifying question) with no citation
also fails, because a missing citation fails the answer.

NOT automatic: whether the cited doc actually supports the claim. That stays a
human yes/no in eval/generation_results.md.
"""
from generate import KB


def is_clarifying(result: dict) -> bool:
    """No citations, not a refusal, and it asks something (the question may not be the last sentence)."""
    return not result["refused"] and not result["cited_ids"] and "?" in result["answer"]


def verify(result: dict) -> dict:
    problems = []
    for cid in result["cited_ids"]:
        if cid not in KB:
            problems.append(f"[{cid}] is not a KB doc")
        elif cid not in result["retrieved_ids"]:
            problems.append(f"[{cid}] was not retrieved for this query")
    if not result["cited_ids"] and not result["refused"] and not is_clarifying(result):
        problems.append("answer has no citations")
    return {"citation_ok": not problems, "problems": problems}
