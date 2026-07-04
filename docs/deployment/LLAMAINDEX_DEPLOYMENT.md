# LlamaIndex Deployment

Purpose

Prepare Alfred for optional document indexing and retrieval workflows.

When To Use

- When executive knowledge volume requires structured retrieval support.
- When canonical evidence and entity resolution are already stable.

Prerequisites

- Alfred local environment is healthy.
- Vault or evidence paths are known.
- Optional dependency installation is approved.

Install Steps

1. Review retrieval scope and expected outputs.
2. Isolate optional dependencies from the core Alfred runtime.
3. Prepare templates or bundles under `downloads/deployment/`.

Configuration Steps

1. Define the indexed evidence set.
2. Define which entity types will be indexed.
3. Keep configuration in versioned files, not frontend state.

Validation Commands

- `python build_executive_knowledge.py`
- `python build_knowledge_graph.py`
- `pytest`

Troubleshooting

- Check canonical entity quality before expanding indexing scope.
- Reduce scope if retrieval latency becomes excessive.

Status

Not installed
