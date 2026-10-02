# Professional Research Project — Kickoff & Decision Log
## Topic #8: RAG Assistant (KLM anchor) · Role: Architect

*Started: 2026-09-17 · Status: **LOCKED** (topic confirmed 2026-09-17) · Domain: **e-commerce** — single online store (locked 2026-09-19) · KB source locked 2026-09-28 — self-authored fictional store + EU text, freeze-then-test (DL-04)*

> **RAG** = Retrieval-Augmented Generation. Instead of asking a language model to answer from memory (where it invents things), you first *retrieve* the relevant documents from your own knowledge base, then hand them to the model and tell it to answer *only* from those. It's how you make an AI answer trustworthy questions with sources.

---

## 1. What I'm building (one paragraph)

An end-to-end question-answering assistant for a single online store's customer service. A user asks a plain-language question ("My order arrived damaged — can I get a refund?"); the system finds the right passages in a curated knowledge base of the store's policy documents, feeds them to a language model, and returns a clear answer **with citations** pointing to the exact source. Critically, when the answer isn't in the knowledge base, it says so instead of guessing.

The pipeline, stage by stage (this is the mental model I defend in the review):

| Stage | Plain meaning | What I decide |
|---|---|---|
| **Understand** | Turn the question into a searchable form | how to embed the query |
| **Retrieve** | Find the most relevant passages | vector DB, top-k, similarity threshold |
| **Augment** | Bundle those passages into the prompt | chunking, how much context |
| **Generate** | Model writes the answer from them | which model, citation format |
| **Verify** | Check the answer is grounded + cited | citation accuracy, "not in KB" handling |

> **Embed / embedding** = turning text into a list of numbers that captures its meaning, so the computer can measure which passages are "closest" to the question. **Vector DB** = a database built to search those number-lists fast. **Chunking** = splitting long documents into bite-sized passages so retrieval returns a paragraph, not a 40-page PDF. **top-k** = how many passages you pull back per question.

---

## 2. The assignment (from the brief) — the bar I'm held to

- **Knowledge base:** ≥ 50 documents.
- **Test set:** 10 test queries, **including out-of-knowledge-base edge cases** (questions the KB can't answer).
- **Targets:**
  - Retrieval accuracy **> 80%** (right passage found for the question)
  - Answers **> 70% human-approved** (a person judges the answer correct + useful)
  - Citations **100% accurate** (every citation actually supports the claim)
- **Required throughout:** a Decision Log (this file) capturing *why* each choice was made.

---

## 3. Domain & knowledge base plan

**Domain: e-commerce customer service — ONE online store** (a single store, so the KB never contradicts itself; mirrors the KLM support use case).

Target ~50–60 documents, grouped so retrieval has clean topics to hit:

- Consumer rights (**EU right of withdrawal** — the 14-day return right for online purchases; public legal text, the authoritative anchor)
- Shipping & delivery: options, times, costs, international
- Returns, refunds, exchanges, store credit
- Order changes, cancellation, tracking
- Payment methods, security, failed payments
- Warranty, faulty/defective items, missing parts
- Sizing / product info / care
- Accounts, promo codes, gift cards

**Sourcing + ethics note (log this):** pin ONE store. Either (a) a real store's publicly published help-centre articles + the official EU right-of-withdrawal text — cite them, note it's an academic recreation, not affiliated, and don't scrape logged-in areas; or (b) a self-authored fictional store's policy set + the EU legal text — no copyright question. **DECIDED 2026-09-28: option (b), self-authored fictional store, with freeze-then-test (write all docs before the test queries). Full entry: 2026-09-28 — KB source — self-authored fictional store.**

---

## 4. Architecture — options & trade-offs (this is my LO1 evidence)

The rule for every choice below: pick what I can *run cheaply* and *explain fully*. Flashy loses to defensible.

**Orchestration (the framework that wires the stages together)**

| Option | Pro | Con | Lean |
|---|---|---|---|
| LlamaIndex | RAG-first, least boilerplate for exactly this | one more abstraction to learn | ✅ likely |
| LangChain | flexible, huge ecosystem | heavier, easy to cargo-cult code you can't defend | maybe |
| n8n (no-code) | fast to wire visually | hides the mechanics — *this is the dashboard trap again* | ❌ avoid |

**Embedding model (turns text → number-lists)**

| Option | Pro | Con |
|---|---|---|
| Open-source (e.g. `bge-small`, `all-MiniLM`) | free, runs locally, no data leaves my machine, defensible | slightly lower quality |
| OpenAI `text-embedding-3-small` | strong quality, trivial to use | costs per call, data goes to a vendor |

*Lean: open-source local — cheaper and a stronger privacy story for the ethics section.*

**Vector database (fast similarity search)**

| Option | Pro | Con |
|---|---|---|
| Chroma (local) | free, zero setup, perfect for ~50 docs | not built for millions of docs (irrelevant here) |
| Pinecone / Weaviate (managed) | scales huge, production-grade | overkill, account + cost, more to defend |

*Lean: Chroma. Matching the tool to the problem size is itself a defensible Architect decision — log it.*

**Chunking (how I split documents)**

- Naive fixed-size (every N characters) — simple but slices sentences in half.
- **Structure-aware (split by policy section/heading)** — passages stay whole and on-topic. ✅ Better for policy docs.

**Generation model + citations**

- Model: a current Claude or GPT-4o-class model via API.
- Citation method: tag every chunk with its source doc + section; require the model to cite the chunk IDs it used; then **programmatically verify** the cited chunk actually contains the claim. That verify step is what turns "citations look nice" into "citations 100% accurate."

---

## 5. Where "proficient" actually comes from (the defensibility edge)

RAG is a common choice, so "it works" won't earn a top mark — everyone's will kind of work. Proficiency comes from the **failure modes**. Design the test set to include the hard ones from day one:

- **Out-of-KB** ("Do you fly to Mars?") → must answer *"I don't have that information,"* never invent.
- **Ambiguous** ("Can I bring it?") → should ask a clarifying question, not guess.
- **Multi-document** (answer needs two policies combined) → tests whether retrieval + synthesis actually work.
- **Outdated-info** trap → what happens when a policy changed; how citations expose it.
- **Wrong-citation** → the sneakiest failure: right-sounding answer, citation that doesn't support it. My verify step targets exactly this.

Logging retrieval hits/misses per query, and showing a failure I caught and fixed, is the difference between a demo and portfolio evidence.

---

## 6. Decision Log (the graded reasoning trail — append as I go)

**DL-01 · Topic chosen: RAG assistant (#8) over #2 (video) and #3 (multi-agent).**
Why: as an Architect I'm graded on designing systems I can defend end-to-end. #2's core is a black-box video model I'd only be calling — undefendable in a technical review (the same gap that sank the week-1 dashboard). #3 was the strongest interest/defensibility overlap but I chose lower defense risk. RAG's whole pipeline is glass-box and reused later in the Industry Project, so the learning compounds. *Trade-off accepted: less day-to-day excitement than #2/#3.*

**DL-02 · Role framing: Architect.**
Focus of my evidence is the design decisions (retrieval strategy, chunking, citation verification), not raw coding volume.

**DL-03 · Success criteria locked to the brief:** retrieval > 80%, answers > 70% approved, citations 100%. Measured on a 10-query test set built *before* the system, including ≥ 3 out-of-KB edge cases. *(Test-first so I'm not grading myself on questions I designed the system to pass.)*

**DL-04 · Domain = e-commerce (single online store), locked 2026-09-19** over airline/travel and healthcare/education — best domain familiarity (retail/Plainwear background), easiest doc sourcing, and natural out-of-KB edge cases (order status, product advice). **KB source DECIDED 2026-09-28 (log #9):** self-authored fictional single store + EU right-of-withdrawal text (option b) — chosen for full content control and no copyright question over real-world realism; evaluation honesty protected by **freeze-then-test** (KB written before the 10 test queries). Full entry: 2026-09-28 — KB source — self-authored fictional store.

**DL-05 · Stack: PROVISIONAL** — LlamaIndex + local open-source embeddings + Chroma + structure-aware chunking + API generation model with verified citations. Confirm after a 5-document spike (small throwaway test) proves the pipeline runs.

---

## 7. Immediate next steps

1. ~~Decide KB source (DL-04)~~ ✅ done 2026-09-28 — self-authored fictional store, freeze-then-test.
2. **Write the 10 test queries first** — including the edge cases. This is the ruler I measure against.
3. **5-document spike** — tiny end-to-end run on 5 docs to prove the stack before scaling to 50.
4. **Build the full KB** (~50 docs), then run + measure against §2 targets.
5. **Log every non-obvious choice** here as it happens — memory fades, the Decision Log doesn't.

---
*Note: "proficient"-level interpretations here are mine — verify against the Fontys learning-outcome clarification and your assessor's rubric before relying on them.*

**DL-06 · Topic LOCKED (Sep 17, 2026).** KLM/RAG confirmed as a Professional Research Project. No further reconsideration — remaining open item: stack confirmation after the spike (DL-05). KB source resolved 2026-09-28 (DL-04 / log #9).
