---
type: note
author: claude
project: KLM RAG (Research Project)
entry: 7
lo_stage: Designing
lo: [LO3, LO1]
date: 2026-09-17
---

# Decision Log Entry 7 — Provisional RAG stack (LlamaIndex + Chroma + local embeddings + structure-aware chunking + verified citations)

**Portfolio name (PortFlow):** `[DL] Which stack should the RAG pipeline use? (LO3)`

*Related: KLM RAG — Start Here · KLM RAG — Project Kickoff & Decision Log · Decision Logs — Index*

## 0. Context — why does this question exist?
- **Project:** KLM RAG. Need a toolchain for the five pipeline stages (Understand → Retrieve → Augment → Generate → Verify) that I can run cheaply and explain fully.
- **Why now:** it anchors the spike and the full build.
- 🔗 **Where it fits:** kickoff §4 (option/trade-off tables) · DL-05.

## 1. My research question
Which orchestration / embeddings / vector DB / chunking / generation choices fit a ~50-doc, free-budget, fully-defensible RAG?

## 2. Current LO stage
Designing.

## 3. What makes a good decision here?
- Cheap / local to run (no budget).
- Fully explainable in a review — no black boxes (avoid "the dashboard trap").
- Right-sized for ~50 documents.
- Strong privacy / ethics story.

## 4. What I decided
**PROVISIONAL (confirm after a 5-document spike):** LlamaIndex (orchestration) + local open-source embeddings (e.g. `bge-small` / `all-MiniLM`) + Chroma (vector DB) + structure-aware chunking (split by policy section) + a current Claude/GPT-4o-class API model with **programmatically verified citations**.

## 5. Why this decision
- **Method:** an option/trade-off table per component.
- **What I found:** LlamaIndex is RAG-first with the least boilerplate (n8n hides the mechanics — the dashboard trap — rejected; LangChain heavier/easy to cargo-cult); local embeddings are free and keep data on-device (better ethics story) vs OpenAI's paid/vendor route; Chroma fits ~50 docs with zero setup (Pinecone/Weaviate = overkill); structure-aware chunking keeps policy passages whole; verifying that each cited chunk actually contains the claim is what turns "citations look nice" into "citations 100% accurate".
- 🔗 **Evidence:** KLM RAG — Project Kickoff & Decision Log (§4, DL-05) · *(add the chat where this was decided)*.
- **So I decided:** match the tools to the problem size and to defensibility.

## 6. Does this hold up?
- **Assumptions:** local embeddings are good enough to reach >80% retrieval; LlamaIndex stays explainable rather than a black box.
- **What would change it:** the 5-doc spike shows retrieval below target, or a tool I can't defend.
- *Result: PROVISIONAL — confirm after the spike.*

## 7. What this unlocks
- A concrete pipeline to spike.
- **Next LO stage:** Realizing — the 5-document spike.
- **How I'll know it worked:** the spike runs end-to-end and hits retrieval on a handful of queries.
