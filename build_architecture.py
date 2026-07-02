#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(__file__).parent
ARCH = ROOT / "architecture"
ARCH.mkdir(exist_ok=True)

DOCS = {
    "00 Vision.md": """# Vision

Alfred is an Executive Operating System.

It exists to improve executive decision-making by combining Obsidian memory, deterministic workflows, semantic retrieval, evidence-bound AI reasoning, and executive presentation.

Obsidian is the source of truth. Generated reports, indexes, architecture documents, and executive reviews are derived artefacts.
""",
    "01 Principles.md": """# Principles

## Obsidian is the source of truth

The Obsidian vault is authoritative. Everything else is derived.

## Evidence before inference

Alfred must retrieve evidence before forming conclusions.

## Derived knowledge is disposable

Indexes, briefings, reports, and generated architecture must be rebuildable.

## Preserve proven components

Do not replace working components unless there is a clear architectural reason.

## Smallest safe change

Repair or extend Alfred with the smallest change that restores or advances intended behaviour.

## Fail clearly

If evidence is missing or insufficient, Alfred must say so.

## No drift

New ideas belong either to the current phase or the backlog.
""",
    "02 System Architecture.md": """# System Architecture

## Baseline

Recovery Point Alpha is the implementation baseline.

## Logical Flow

User -> Telegram / ChatGPT Action / Future UI -> Alfred Router or API boundary -> deterministic strategy or semantic retrieval -> evidence package -> reasoning layer -> executive response.

## Core Components

- Obsidian vault
- Hermes / Second Brain scripts
- Alfred Router
- Telegram bot
- LlamaIndex evidence engine
- ChatGPT Action
- OpenRouter compatibility path
- Cloudflare routing
- Handbook generator
- Architecture generator
- Executive Review generator
""",
    "03 Component Specifications.md": """# Component Specifications

## Obsidian

Source of truth and durable knowledge store.

## Alfred Router

Orchestration, strategy selection, and quality gates.

## LlamaIndex

Semantic retrieval and evidence packaging.

## Telegram

Mobile executive interface.

## Hermes Batch

Background enrichment and deterministic processing.

## ChatGPT

Executive reasoning over evidence.

## OpenRouter

Legacy model access and compatibility path.

## Cloudflare

Public HTTPS routing to local services.
""",
    "04 Capability Model.md": """# Capability Model

## Executive Review

Summarise current executive position, risks, actions, and recommended next steps.

## Meeting Preparation

Prepare evidence-led briefs for upcoming meetings.

## Follow-ups

Extract, track, and escalate commitments.

## Open Loops

Identify incomplete work and recommend closure.

## Projects

Track project health, ownership, evidence, and dependencies.

## Objectives

Link work to strategic objectives and detect drift.
""",
    "05 Agent Organisation.md": """# Agent Organisation

## Alfred

Executive oracle and orchestration identity.

## Nigel

Chief of Staff role supporting prioritisation and coordination.

## Specialist Domains

- Procurement
- Risk
- Governance
- Investment
- Operations
- Architecture

Agents may advise, enrich, and recommend. They must not replace source evidence or bypass governance.
""",
    "06 Information Model.md": """# Information Model

## Source Objects

- Notes
- Daily logs
- People
- Companies
- Projects
- Objectives
- Decisions
- Meetings
- Follow-ups
- Open loops

## Derived Objects

- Evidence packages
- Executive reviews
- Briefings
- Indexes
- Knowledge graph outputs

Derived objects must be traceable back to source evidence.
""",
    "07 Security & Governance.md": """# Security and Governance

## Secrets

Secrets must be held outside source code.

## Evidence

Responses must be evidence-bound where factual claims are made.

## Audit

Material recommendations should be traceable to source evidence.

## Recovery

Recovery work must restore the smallest broken component before redesign.

## Change Control

Significant changes require regeneration of handbook, architecture, and executive review outputs.
""",
    "08 Build Roadmap.md": """# Build Roadmap

## Phase 1 — Recovery

Complete.

## Phase 2 — Foundation

Recovery Point Alpha, engineering handbook, architecture generator, and executive review prototype.

## Phase 3 — Architecture Reconciliation

Compare Recovery Point Alpha to Alfred V2 intent.

## Phase 4 — Executive Capabilities

1. Executive Review
2. Meeting Preparation
3. Follow-ups
4. Open Loops
5. Projects
6. Objectives

## Backlog

- Executive Critic
- Negotiation Intelligence
- Multi-agent debate
- Autonomous governance workflows
""",
    "09 Decision Log.md": """# Decision Log

## Current Decisions

- Recovery Point Alpha is the implementation baseline.
- Obsidian is the source of truth.
- Alfred Router remains the orchestration layer.
- V2 reference platform is architectural intent, not implementation authority.
- LLMs reason over evidence but do not own memory.
""",
    "10 Architectural Decision Records.md": """# Architectural Decision Records

## ADR-001: Recovery Point Alpha is the implementation baseline

Accepted.

## ADR-002: Obsidian is the source of truth

Accepted.

## ADR-003: Alfred Router remains the orchestration layer

Accepted.

## ADR-004: V2 reference platform is architectural intent, not implementation authority

Accepted.

## ADR-005: LLMs reason over evidence but do not own memory

Accepted.
""",
}

for filename, content in DOCS.items():
    (ARCH / filename).write_text(content.strip() + "\n")

blueprint = ARCH / "Alfred Architecture Blueprint.md"
with blueprint.open("w") as out:
    out.write("# Alfred Architecture Blueprint\n\n")
    for filename in sorted(DOCS):
        out.write("\n---\n\n")
        out.write((ARCH / filename).read_text())

print("Architecture generated:")
print(blueprint)
