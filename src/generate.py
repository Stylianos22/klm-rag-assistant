"""Generate an answer grounded ONLY in retrieved chunks, with citations.

Needs an LLM. No paid budget -> use a free/local model (e.g. Ollama) or a
school-licensed API. Keep the client swappable behind one function.
"""
# TODO: build a prompt from the retrieved chunks; instruct the model to answer
# ONLY from them and cite each source by doc_id/title; if nothing retrieved
# (abstain), return the "I don't have that information" response.
