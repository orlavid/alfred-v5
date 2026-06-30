#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import contextlib

BASE = Path(__file__).parent
PERSIST = str(BASE / "index")

args = sys.argv[1:]
json_mode = False

if args and args[0] == "--json":
    json_mode = True
    args = args[1:]

if not args:
    raise SystemExit('Usage: alfred.py [--json] "question"')

question = " ".join(args)

with contextlib.redirect_stdout(sys.stderr):
    from llama_index.core import StorageContext, load_index_from_storage, Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.llm = None

    storage_context = StorageContext.from_defaults(persist_dir=PERSIST)
    index = load_index_from_storage(storage_context)
    retriever = index.as_retriever(similarity_top_k=12)

    nodes = retriever.retrieve(question)

evidence = []
for i, node in enumerate(nodes, 1):
    meta = getattr(node.node, "metadata", {}) or {}
    path = meta.get("file_path") or meta.get("filename") or meta.get("source") or "unknown"
    text = node.node.get_content()[:2500]
    score = getattr(node, "score", None)
    evidence.append(
        f"### Evidence {i}\n"
        f"Source: {path}\n"
        f"Score: {score}\n\n"
        f"{text}"
    )

answer = f"""You are Alfred's evidence package.

Question:
{question}

Instructions for ChatGPT:
Use only the evidence below. If the evidence is insufficient, say so clearly. Do not use public knowledge or memory.

Evidence:
{chr(10).join(evidence)}
"""

payload = {
    "question": question,
    "answer": answer,
    "quality_gate": "EVIDENCE_PACKAGE_ONLY_CHATGPT_MUST_REASON",
    "source": "alfred.py",
}

print(json.dumps(payload) if json_mode else answer)
