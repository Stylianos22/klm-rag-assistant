# KLM RAG Assistant — Northbound customer service

A retrieval-augmented generation (RAG) customer-service assistant for **Northbound**, a fictional EU online store. A customer asks a question; the system retrieves the right policy documents, answers **with citations**, and **refuses** when the answer isn't in the knowledge base.

> **Fontys MA-AAI (Applied GenAI), Semester 4 — portfolio evidence bundle.** Professional Research Project by Stylianos Pharmakas (GenAI Architect track). The decision logs and measured results are the evidence; the code is what produced them.

## Status

| Stage | State |
|---|---|
| Knowledge base (51 docs) + 10 frozen test queries | ✅ done |
| Ingest → embed → Chroma index → top-3 retrieval | ✅ built and measured (full-KB retrieval 4/6 = 67%; see [results](docs/eval-results.md)) |
| Abstention | ✅ moved from a similarity threshold into generation (the model refuses when the docs don't answer) |
| Answer generation with citations + citation gate (`generate.py`, `verify.py`) | ✅ built: citations valid 10/10, edge cases 4/4 ([eval/generation_results.md](eval/generation_results.md)) |
| Local web chat + `/monitor` answer-quality dashboard (`webapp/`) | ✅ built |
| Faithfulness check (LLM-as-judge, `faithfulness.py`) + grounding monitor (`monitor.py`) | 🟡 built; judge v2 scores 100% in-sample but **4/8 = 50% on a held-out set** ([results](eval/faithfulness_holdout_results.md)) — not yet a trustworthy gate |

The project reports its failures as measured, not hidden: retrieval on the real 51-doc KB fell short of target, and the faithfulness judge that looked perfect on its tuning cases agreed with hand labels only half the time on unseen ones.

## Run it

Requires Python 3.10–3.12 (3.14 is too new for the torch/chromadb wheels).

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/run_eval.py --reindex          # build the index from kb/ and score retrieval on the 10 frozen queries
python src/retrieve.py "Do you do pay-later, like Klarna?"   # retrieval only, no API key needed
```

Generation, the faithfulness judge and the monitor call the Claude API. Put your key in a `.env` file in the repo root (gitignored, never committed):

```bash
echo "ANTHROPIC_API_KEY=your-key-here" > .env
python src/chat.py                        # terminal chat
python src/run_generation_eval.py         # answers + citation gate on the 10 frozen queries
python src/monitor.py                     # one monitor run (about $0.01): grounding score over the 10 queries
PORT=5001 python webapp/app.py            # web chat at /  and the dashboard at /monitor (with a Run monitor button)
```

The first run downloads the `all-MiniLM-L6-v2` embedding model (~90 MB); retrieval runs locally.

## Learning outcomes → evidence

| Part | LO | What it proves |
|---|---|---|
| [KB sourcing & authorship note](docs/kb-sourcing-and-authorship-note.md) + [DL09](docs/decision-logs/DL09-kb-source-self-authored-store.md) | LO6 | Ethics / evaluation honesty: freeze-then-test, AI authorship disclosed, deliberate gaps preserved |
| [KB structure](docs/kb-structure.md) + [kb/](kb/) | LO1 | Analysing: the KB is real, structured and internally consistent |
| [Kickoff stack trade-off tables](docs/project-kickoff-and-decision-log.md) + [DL07](docs/decision-logs/DL07-provisional-rag-stack.md) | LO3 | Designing: a justified RAG stack |
| [Test queries (frozen)](eval/test-queries-frozen.md) + [DL11](docs/decision-logs/DL11-evaluation-method.md) | LO3 | Designing: measurable, un-gameable evaluation |
| [src/](src/) + `run_eval.py` + [results](docs/eval-results.md) + [DL13](docs/decision-logs/DL13-full-kb-broke-abstain-threshold.md) | LO4 | Realising: a running pipeline, a measured failure and its diagnosis |
| `faithfulness.py`, `monitor.py`, [webapp/](webapp/) `/monitor`, [held-out validation](eval/faithfulness_holdout_results.md) | LO5 | Managing: answer quality monitored over runs, with the judge itself validated on unseen cases |

## Repository layout

```
src/        pipeline: ingest, index, retrieve, generate, verify, faithfulness judge, monitor, evals, chat
webapp/     Flask web chat + /monitor answer-quality dashboard
kb/         51 Northbound policy documents; doc id = leading number in the filename
eval/       queries.json (10 frozen queries, never edited), generation + faithfulness results, monitor run history
spike/      spike.py: the early 9-doc retrieval probe
docs/       decision logs, KB notes, kickoff log, spike note, eval results; screenshots in docs/images/
```

## Rules the project holds itself to

- The 10 test queries were **frozen before the KB was written** and are never edited to make the system pass.
- **No price-match document** exists, so Q9 must be refused; **no order status is ever invented** (Q8).
- Every claim in an answer must cite a document that supports it; a wrong or missing citation fails the answer.

## AI use (disclosure)

AI is part of the method, and is disclosed as such. The 51 KB documents were written by Claude, and the author knew the test queries; the mitigations are in the [sourcing note](docs/kb-sourcing-and-authorship-note.md). The pipeline code was written with Claude Code. The decisions, criteria and judgement calls are recorded in the decision logs, and the AI conversations behind them are part of the evidence (screenshots in `docs/images/`).

Northbound is fictional; any resemblance to a real store is coincidental.
