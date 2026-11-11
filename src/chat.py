"""Live demo: type a question, get a cited answer. `exit` quits. Not part of the eval.

Usage:  python src/chat.py
"""
from generate import KB, answer
from index import get_collection
from verify import is_clarifying


def main():
    col = get_collection()
    print("Northbound support (type 'exit' to quit)")
    while True:
        try:
            q = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in ("exit", "quit"):
            break
        if not q:
            continue
        r = answer(q, col=col)
        print(f"\nAssistant: {r['answer']}")
        if r["refused"]:
            print("(refused: not in the knowledge base)")
        elif is_clarifying(r):
            print("(clarifying question)")
        else:
            print("Sources: " + ", ".join(f"[{d}] {KB[d][0]}" for d in r["cited_ids"] if d in KB))


if __name__ == "__main__":
    main()
