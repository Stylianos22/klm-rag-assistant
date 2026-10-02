# KLM RAG Assistant — Northbound customer service

A retrieval-augmented generation (RAG) customer-service assistant for **Northbound**, a fictional EU online store. A customer asks a question; the system retrieves the right policy documents, answers **with citations**, and **refuses** when the answer isn't in the knowledge base.

> **Fontys MA-AAI (Applied GenAI), Semester 4 — portfolio evidence bundle.** Professional Research Project by Stylianos Pharmakas (GenAI Architect track). The decision logs and measured results are the evidence; the code is what produced them.

## Status

| Stage | State |
|---|---|
| Knowledge base (51 docs) + 10 frozen test queries | ✅ done |
| Ingest → embed → Chroma index → top-3 retrieval + abstain | ✅ built and measured |
| Retrieval eval on the full KB | ❌ **4/6 = 67%** (target >80%); Q9 not refused — see [results](docs/eval-results.md) |
| Fix (reranker / LLM grounding check) | ⏳ being decided — [DL13](docs/decision-logs/DL13-full-kb-broke-abstain-threshold.md) |
| Answer generation + citation verification (`generate.py`, `verify.py`) | ⏳ stubs, not built yet |

The current result is a measured failure, documented with its cause, not hidden: a spike on 9 docs scored 100%, but only on hand-written summaries; on the real 51-doc KB, retrieval drops to 67% and no single similarity threshold separates answerable from unanswerable questions.

## Run the eval

Requires Python 3.10–3.12 (3.14 is too new for the torch/chromadb wheels).

```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/run_eval.py --reindex          # build the index from kb/ and score the 10 frozen queries
python src/run_eval.py --sweep            # threshold margins: lowest answerable vs highest out-of-KB score
python src/retrieve.py "Do you do pay-later, like Klarna?"   # try a single question
```

The first run downloads the `all-MiniLM-L6-v2` embedding model (~90 MB). Everything runs locally and free; no API key is needed for retrieval.

## Learning outcomes → evidence

| Part | LO | What it proves |
|---|---|---|
| [KB sourcing & authorship note](docs/kb-sourcing-and-authorship-note.md) + [DL09](docs/decision-logs/DL09-kb-source-self-authored-store.md) | LO6 | Ethics / evaluation honesty: freeze-then-test, AI authorship disclosed, deliberate gaps preserved |
| [KB structure](docs/kb-structure.md) + [kb/](kb/) | LO1 | Analysing: the KB is real, structured and internally consistent |
| [Kickoff stack trade-off tables](docs/project-kickoff-and-decision-log.md) + [DL07](docs/decision-logs/DL07-provisional-rag-stack.md) | LO3 | Designing: a justified RAG stack |
| [Test queries (frozen)](eval/test-queries-frozen.md) + [DL11](docs/decision-logs/DL11-evaluation-method.md) | LO3 | Designing: measurable, un-gameable evaluation |
| [src/](src/) + `run_eval.py` + [results](docs/eval-results.md) + [DL13](docs/decision-logs/DL13-full-kb-broke-abstain-threshold.md) | LO4 | Realising: a running pipeline, a measured failure and its diagnosis (fix in progress) |

## Repository layout

```
src/        pipeline: ingest.py, index.py, retrieve.py, run_eval.py (generate.py, verify.py = stubs)
kb/         51 Northbound policy documents; doc id = leading number in the filename
eval/       queries.json (10 frozen queries + gold docs + scoring) and the frozen query write-up
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
