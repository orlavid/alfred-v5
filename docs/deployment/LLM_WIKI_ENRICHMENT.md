# LLM Wiki Enrichment

Purpose

Define the optional enrichment pattern for wiki-style executive context.

When To Use

- When concise background context improves decision quality.
- When enrichment remains clearly separate from canonical evidence.

Prerequisites

- Canonical executive entities exist.
- Evidence-backed knowledge and generated enrichment are clearly separated.
- Output locations are defined.

Install Steps

1. Define enrichment targets and guardrails.
2. Prepare placeholder templates in `downloads/deployment/`.
3. Keep enrichment outside the core runtime path.

Configuration Steps

1. Select eligible entity classes.
2. Define review thresholds and budgets.
3. Link outputs back to evidence without replacing the source of truth.

Validation Commands

- `python build_executive_knowledge.py`
- `python build_knowledge_graph.py`
- `pytest`

Troubleshooting

- Reduce scope if generated context drifts from evidence.
- Improve canonical naming if duplication appears.

Status

Not installed
