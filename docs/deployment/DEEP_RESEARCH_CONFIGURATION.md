# Deep Research Configuration

Purpose

Define the control model for optional high-cost research workflows.

When To Use

- Only when lightweight enrichment is insufficient.
- Only when the executive question justifies deeper retrieval and cost.

Prerequisites

- Model/API configuration exists.
- Budget and token controls exist.
- Review checkpoints are defined.

Install Steps

1. Document controls before implementation.
2. Prepare placeholder bundles or templates in `downloads/deployment/`.
3. Keep the capability disabled until governance is approved.

Configuration Steps

1. Define token budgets and concurrency limits.
2. Separate research outputs from canonical evidence until reviewed.
3. Capture monitoring and cost-reporting expectations.

Validation Commands

- `python build_everything.py`
- `pytest`

Troubleshooting

- Do not enable the workflow if cost or latency is unclear.
- Keep the mode disabled if outputs cannot be audited back to sources.

Status

Not installed
