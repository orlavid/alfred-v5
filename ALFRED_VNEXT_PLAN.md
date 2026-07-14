# Alfred vNext Plan

Date:
- 2026-07-14

Inputs obeyed:
- [BUILD_CHARTER.md](BUILD_CHARTER.md)
- [PRODUCT_RESET_AUDIT.md](PRODUCT_RESET_AUDIT.md)
- [SIMPLE_VAULT_RETRIEVAL_BAKEOFF.md](SIMPLE_VAULT_RETRIEVAL_BAKEOFF.md)
- [ARCHITECTURE_CONSTITUTION.md](ARCHITECTURE_CONSTITUTION.md)
- existing Definition of Done as supplied by the user

Decision baseline:
- Bake-off conclusion: `D. HYBRID`
- Strategy decision: do not incrementally repair the current Alfred intelligence/product pipeline as the primary route
- Build Alfred vNext alongside the current live product

## 1. Locked Design Decisions

### Decision 1: Parallel vNext

Alfred vNext will be built alongside the current live Alfred product.

Purpose:
- preserve the current live release as:
  - reference
  - rollback
  - comparison baseline
- avoid destabilising the current production path during the reset

Planned boundary:
- current Alfred remains on the existing production application path
- Alfred vNext will sit in a separate product layer and request path

Proposed code boundary:
- `src/vnext/`
- `web/src/vnext/`
- `tests/vnext/`

Proposed environment boundary:
- separate vNext published snapshot namespace
- separate vNext API namespace
- separate vNext persistence store or schema for managed matters

Proposed URL boundary:
- current product remains at the current live root
- vNext served under either:
  - `/#/vnext/...`
  - or a parallel environment such as `vnext` subdomain / port

Preferred planning default:
- separate environment and separate URL

Reason:
- the charter requires user-facing trust, rollback, and comparison clarity

Cutover approach:
- side-by-side comparison against current Alfred using real workflows
- cut over only when vNext materially outperforms current Alfred on the approved stage gates

Rollback approach:
- keep current live Alfred deployable and unchanged
- vNext cutover must be reversible by route/environment switch, not by emergency rebuild

### Decision 2: Hybrid architecture with two lanes

Alfred vNext has two primary lanes.

Lane A: Knowledge and Intelligence
- Obsidian vault
- direct retrieval
- relevant source evidence
- AI synthesis
- answer / insight / recommendation

Use Lane A for:
- Ask Alfred
- people/company context
- meeting preparation
- “what is happening?”
- “what changed?”
- research across the vault
- executive synthesis
- contextual questions

Lane B: Managed Work
- vault evidence
- atomic managed matter
- editable workflow state
- relationships
- optional on-demand enrichment

Use Lane B for:
- Objectives
- Projects
- Follow-ups
- Open Loops
- Decisions
- Risks

Core rule:
- do not force knowledge questions through a universal canonical `ExecutiveState` path
- do not force managed work to duplicate the entire vault

### Decision 3: Common Matter Core

Alfred vNext will use one minimal shared Matter model for managed work.

Minimum shared fields:
- `matter_id`
- `primary_type`
- `title`
- `summary`
- `status`
- `owner`
- `priority`
- `start_date`
- `due_date`
- `target_date`
- `source_evidence_refs`
- `evidence_summary`
- `relationships`
- `management_notes`
- `created_at`
- `updated_at`
- `workflow_history`
- `enrichment_history`

Primary types:
- Objective
- Project
- Follow-up
- Open Loop
- Decision
- Risk

Rules:
- one matter has one primary operational type at a time
- one matter may have many relationships
- views such as Plan Today reference matters rather than mint duplicates
- only add domain-specific extensions when the workflow genuinely requires them

Explicit anti-goal:
- do not build another universal ontology

### Decision 4: Record creation policy

High-confidence explicit structure:
- explicit checkbox action
- explicit structured objective
- explicit project record
- explicit decision statement

Policy:
- may create or update a managed record automatically where rules are deterministic and evidence is strong

Ambiguous prose:
- AI may detect and propose atomic matters
- do not silently create authoritative managed records from ambiguous prose

Proposed risks:
- remain proposed until accepted

Inferred decisions:
- remain proposed until confirmed unless explicit decision evidence exists

User-created records:
- are authoritative managed state

Confidence policy:
- use only simple confidence states:
  - explicit
  - proposed
  - accepted
- avoid an elaborate confidence framework

### Decision 5: Interaction model

Cards:
- reserved for:
  - small executive summaries
  - top-level exceptions
  - limited KPI views

Lists / tables:
- default for:
  - Follow-ups
  - Open Loops
  - Decisions
  - Risks
  - Actions
  - other high-volume managed work

Required list behaviour:
- search
- filter
- sort
- inline editing
- row selection
- multi-select
- batch actions
- direct drill-through

Detail views:
- used for:
  - understanding
  - context
  - evidence
  - relationships
  - AI interrogation
  - enrichment
  - management workflow
  - history

### Decision 6: AI operating model

Mode A: Retrieval Synthesis
- automatic when the user asks a question
- process:
  - query
  - direct vault retrieval
  - evidence selection
  - synthesis
  - answer with readable evidence and provenance

Mode B: On-Demand Enrichment
- explicitly invoked by the user for one or more managed matters
- may propose:
  - improved title
  - context
  - why it matters
  - relationships
  - owner
  - dates
  - milestones
  - dependencies
  - risks
  - next actions
  - missing information
  - completion criteria

Rules:
- reviewable
- editable
- partially acceptable
- rejectable
- never silently authoritative

Mode C: Background Discovery
- scheduled process may identify:
  - candidate actions
  - candidate decisions
  - candidate risks
  - candidate relationships
  - potentially stale or completed work

Authority policy:
- automatic discovery
- human-controlled authority

### Decision 7: Source-of-truth boundary

Obsidian remains the source of truth for:
- source evidence
- notes
- meetings
- documents
- knowledge
- long-form thinking

Alfred manages:
- workflow state
- assignments
- status
- priorities
- dates
- accepted relationships
- accepted enrichment
- audit history

Boundary rule:
- Alfred does not continuously rewrite the vault
- any future export/sync is explicit and separately governed

## 2. Reused Components to Keep

### VPS infrastructure

Retain:
- existing VPS hosting and service model

Why:
- proven operationally
- already supports published snapshots, restart behaviour, and deployment validation

Reuse mode:
- reused with adaptation for parallel vNext environment isolation

### Git / GitHub deployment process

Retain:
- current repo, branch, and deployment discipline

Why:
- already supports repeatable deploy, rollback reference points, and production gating

Reuse mode:
- reused unchanged unless vNext needs environment-specific deploy steps

### Published snapshot / last-known-good mechanism

Retain:
- published snapshot model
- atomic promotion
- failed-refresh preservation

Why:
- already fixes the blank-start / monolithic payload problem
- aligns with the charter’s currentness and resilience requirements

Reuse mode:
- adapted to vNext payloads and endpoints

### Vault access

Retain:
- live Obsidian vault access path and note-reading infrastructure

Why:
- essential for both retrieval synthesis and evidence-backed managed work

Reuse mode:
- reused unchanged

### Direct vault retrieval capability proven in the bake-off

Retain:
- exact search
- note reading
- heading/list parsing
- folder/date context

Why:
- bake-off proved this is currently the best-performing path for executive Q&A

Reuse mode:
- reused as the default vNext intelligence path

### Semantic search where it materially improves retrieval

Retain selectively:
- only where it materially improves recall on a query

Why:
- helpful in targeted retrieval
- not trustworthy as a universal first-pass abstraction

Reuse mode:
- adapted, optional, query-dependent

### Stable IDs where reusable

Retain:
- existing stable IDs for validated entities or records where they are already trustworthy

Why:
- avoids unnecessary identity churn across product reset

Reuse mode:
- adapted only where current IDs are noisy or derived from degraded intermediate artefacts

### Persistence / audit components where genuinely fit

Retain:
- persistence and audit patterns that already support state changes and history

Why:
- charter requires auditability by design

Reuse mode:
- adapted into the simpler Matter store

### Six validated objective definitions

Retain:
- current six canonical objective definitions

Why:
- already validated against live evidence and legacy behaviour

Reuse mode:
- reused unchanged as seed managed Objective matters

### Useful canonical project source knowledge

Retain:
- the validated live project source set

Why:
- project extraction/parity work has already recovered a useful baseline source set

Reuse mode:
- adapted into vNext managed Project matters

### Authentication, networking, and routing infrastructure

Retain:
- current app-server, routing, service, and network structure

Why:
- infrastructural foundation is already working

Reuse mode:
- adapted to parallel vNext request paths

### Existing tests that protect valid behaviour

Retain:
- tests covering:
  - snapshot resilience
  - validated objective/project/follow-up/open-loop counts
  - direct route behaviour
  - deployment/runtime gates

Why:
- protects live behaviours that should not regress during vNext build-out

Reuse mode:
- reused and supplemented with stage-specific vNext tests

## 3. Components to Replace / Deprecate / Remove from vNext Request Path

### Replace

- universal multi-stage intelligence transformations that degrade source quality
- `daily_governance_index.py` behaviour that concatenates separate matters
- presentation layers that merge unrelated work into one item
- landing-page manufacturing of duplicate matters across categories
- current non-actionable “Next Best Action” behaviour
- static drill-through pages with no user loop
- card-grid treatment of high-volume work domains

### Deprecate

- routing all executive Q&A through universal canonical state first
- daily-brief subsets being reused as if they were full domain collections
- internal data-quality warnings surfaced as executive risks
- broad canonicalisation where direct retrieval is better and simpler

### Remove from vNext request path

- raw markdown filenames as primary executive evidence
- top-N subsets masquerading as complete collections
- duplicate matter generation across Risks, Open Loops, and Plan Today
- universal request handling through the current Alfred product-layer transformations
- current merged-record dependence where upstream atomicity is already broken

Planning note:
- none of these are deleted in this plan
- they are simply not carried into the vNext primary request path

## 4. Build Sequence

### Stage 0: Freeze and Baseline

Scope:
- preserve the current production release
- record rollback point
- preserve current live URL
- define vNext isolation
- establish benchmark test set

Dependencies:
- none

User outcome:
- safe comparison baseline and rollback assurance

Build Charter acceptance:
- current live product preserved
- vNext isolated
- benchmark questions fixed

Test cases:
- the 12 bake-off questions
- baseline route/load checks
- rollback reference validation

Live acceptance:
- current product still available
- vNext route/environment defined but not yet active

Stop/go:
- stop if rollback or comparison baseline is not explicit

Complexity:
- Small

Principal technical risks:
- environment confusion
- accidental baseline drift

Principal product risks:
- false comparison if baseline changes during build

Reuse opportunities:
- current deployment and snapshot infrastructure

Clear stop condition:
- baseline frozen and benchmark set recorded

### Stage 1: Minimum vNext Foundation

Scope:
- direct vault retrieval
- AI synthesis
- simple Matter persistence
- basic vNext UI
- evidence presentation

Dependencies:
- Stage 0

User outcome:
- vNext can answer the 12 bake-off questions at least as well as the winning simple-retrieval path

Build Charter acceptance:
- answers are understandable
- evidence-backed
- explained in human language
- AI adds value beyond retrieval
- provenance preserved without burdening the user

Test cases:
- all 12 bake-off questions
- direct retrieval for named people/companies/projects
- restart persistence for baseline Matter store

Live acceptance:
- vNext question-answering performs at least as well as the bake-off winner
- answers do not collapse into generic pipeline text

Stop/go:
- go only if retrieval synthesis clearly works live

Complexity:
- Medium

Principal technical risks:
- retrieval quality drift
- evidence-selection inconsistency

Principal product risks:
- answers may still read like search results rather than executive help

Reuse opportunities:
- vault access
- snapshot mechanism
- optional semantic recall helper

Clear stop condition:
- the 12 benchmark questions pass side-by-side quality review

### Stage 2: Reference Workflow — Follow-ups

Scope:
- build Follow-ups as the complete reference managed-work pattern

Must prove:
- atomic work items
- editable dense list
- batch editing
- persistent state
- detail view
- readable evidence summary
- Ask Alfred
- on-demand enrichment
- relationships
- close / hold / assign / link
- audit history

Exact acceptance case:
- the compound Joe Bosberry / HPE Storage / FireAnt / GreenLake / ConnectWise content becomes separate independently manageable matters

Dependencies:
- Stage 1

User outcome:
- the user can fully manage follow-up work through a complete loop

Build Charter acceptance:
- understand
- investigate
- decide
- act
- track
- resolve
- no duplicate matter creation
- action persists
- audit exists

Test cases:
- create atomic follow-ups from explicit structured evidence
- propose atomic follow-ups from ambiguous prose without silent authority
- edit one follow-up and persist
- batch action multiple follow-ups
- open detail, inspect evidence, ask Alfred, enrich, accept/reject proposal
- hold/close and verify persistence after refresh/restart

Live acceptance:
- follow-up workflow materially better than current Alfred
- no compound-matter collapse
- no duplicate record manufactured elsewhere

Stop/go:
- this is the key economic checkpoint
- if this stage cannot produce a materially better system of engagement, stop the broader vNext build

Complexity:
- Medium

Principal technical risks:
- atomicity extraction rules
- persistence model too weak or too broad

Principal product risks:
- enrichment may create noise instead of reducing work

Reuse opportunities:
- current follow-up evidence sources
- persistence/audit foundations
- direct retrieval path

Clear stop condition:
- complete usable follow-up loop live in vNext

### Stage 3: Extend the Pattern

Scope:
- Open Loops
- Decisions
- Risks

Dependencies:
- Stage 2 pattern proved

User outcome:
- the remaining volatile work domains use the same managed-work interaction model

Build Charter acceptance:
- no duplicate matters
- business language over system language
- evidence explained
- user can act

Test cases:
- atomic open loops
- proposed vs accepted risks
- explicit vs inferred decisions
- no duplicate representation across work views

Live acceptance:
- each domain works as a real workflow, not a record display

Stop/go:
- stop if pattern forks into domain-specific mini-architectures

Complexity:
- Large

Principal technical risks:
- edge-case domain differences
- identity and relationship leakage between types

Principal product risks:
- reintroducing separate architectures through domain exceptions

Reuse opportunities:
- Stage 2 list/detail/enrichment/action pattern

Clear stop condition:
- these three domains all run on the same reference workflow model

### Stage 4: Rich Managed Entities

Scope:
- Objectives
- Projects

Additional fields only where genuinely required:
- ownership
- dates
- progress
- RAG
- milestones
- measures
- dependencies
- relationships
- on-demand enrichment
- SMART assessment for Objectives

Dependencies:
- Stage 3

User outcome:
- objectives and projects become true management workspaces, not summary cards

Build Charter acceptance:
- actionability by default
- evidence informs without burden
- current reality over historical noise

Test cases:
- editable objective and project lists
- drill-through workspaces
- SMART assessment proposals
- measure / milestone updates
- no payload bloat on list views

Live acceptance:
- all six objectives and all validated projects support full management use

Stop/go:
- stop if project/objective richness forces a second data model instead of an extension of Matter

Complexity:
- Large

Principal technical risks:
- payload growth
- over-modeling

Principal product risks:
- turning detail views into forms without useful executive help

Reuse opportunities:
- existing validated objective/project source sets
- published per-domain payload pattern

Clear stop condition:
- Objectives and Projects operate as full managed workspaces

### Stage 5: Executive Intelligence

Scope:
- Requires Your Attention
- Plan Today
- Decisions Required
- Meeting Preparation
- What Changed?
- Emerging Risk Detection

Dependencies:
- trustworthy underlying managed work from Stages 2 through 4

User outcome:
- executive overview views reference real underlying matters instead of manufacturing duplicates

Build Charter acceptance:
- executive attention is scarce
- AI adds value beyond retrieval
- complete user loop exists

Test cases:
- one matter one primary state
- no duplicate surfacing across overview views
- each surfaced item has drill-through and action

Live acceptance:
- overview surfaces are command surfaces, not posters

Stop/go:
- stop if intelligence views start manufacturing parallel records again

Complexity:
- Medium

Principal technical risks:
- duplicate surfacing logic
- poor triage thresholds

Principal product risks:
- overview pages drifting back into presentation-only summaries

Reuse opportunities:
- vNext Matter store
- retrieval synthesis
- proven list/detail workflows

Clear stop condition:
- executive home references underlying matters cleanly and actionably

### Stage 6: Side-by-Side Acceptance and Cutover

Scope:
- compare current Alfred and vNext using real workflows
- cut over only when vNext materially outperforms current Alfred
- retain rollback

Dependencies:
- Stages 1 through 5

User outcome:
- safe production adoption of the better product

Build Charter acceptance:
- full applicable acceptance gate satisfied on real workflows

Test cases:
- side-by-side benchmark set
- live user-loop verification
- restart / refresh / rollback checks

Live acceptance:
- vNext demonstrably better on executive outcomes, not only cleaner architecture

Stop/go:
- no cutover if side-by-side comparison is mixed or trust is lower

Complexity:
- Medium

Principal technical risks:
- route/environment switching errors

Principal product risks:
- premature cutover due to sunk-cost pressure

Reuse opportunities:
- current live product as baseline and rollback

Clear stop condition:
- explicit cutover decision or explicit stop decision

## 5. Stage Gates

Every stage must define and satisfy:
- scope
- dependencies
- user outcome
- Build Charter acceptance criteria
- test cases
- live acceptance criteria
- stop/go decision

Universal rule:
- no stage passes merely because:
  - code compiles
  - tests pass
  - data renders

Each stage must prove a complete useful user loop for the scope it claims to deliver.

## 6. Economic Control

Economic guardrails:
- keep stage scope bounded
- reuse existing foundations wherever they are genuinely fit
- avoid domain-specific one-off architectures
- stop at the first failed economic checkpoint rather than continuing by momentum

Key economic checkpoint:
- after Stage 2

Mandatory rule:
- if the Follow-up reference workflow does not demonstrate a materially better system of engagement using the simpler architecture, stop and reassess before building the remaining domains

## 7. First Implementation Proof After Approval

The first end-to-end proof to build after this plan is approved is:

1. Search the live vault directly.
2. Find the exact source evidence behind the known compound Joe Bosberry example.
3. Preserve separate source matters.
4. Create clean atomic managed Follow-ups.
5. Display them in an editable list.
6. Edit one item and persist the change.
7. Select multiple items and perform a batch action.
8. Open one item.
9. Show readable evidence/context.
10. Ask Alfred about it using direct vault retrieval.
11. Invoke enrichment.
12. Review and accept/reject the enrichment proposal.
13. Close or hold the item.
14. Confirm the state persists after refresh/restart.
15. Confirm no duplicate matter is manufactured elsewhere.

This proof is the first real stop/go demonstration for Alfred vNext.

## 8. Genuine Contradictions to Note

There is one genuine contradiction between the current governing documents and the proposed vNext design.

Contradiction:
- [ARCHITECTURE_CONSTITUTION.md](ARCHITECTURE_CONSTITUTION.md) says user-facing experiences must ultimately derive from `ExecutiveState`, and contributors must not introduce new user-facing direct vault reads when `ExecutiveState` already contains the relevant concept.
- The approved vNext bake-off decision and this vNext design deliberately use direct vault retrieval as the primary path for knowledge/intelligence questions.

Interpretation:
- This is a real design contradiction, not a wording nuance.

Proposed handling:
- keep the contradiction explicit during planning
- treat Alfred vNext as a deliberate bounded exception to Platform v1 runtime rules
- if vNext is adopted as the primary product, the constitution will need formal revision at cutover rather than silent reinterpretation

No contradiction found with:
- `BUILD_CHARTER.md`
- `PRODUCT_RESET_AUDIT.md`
- the supplied Definition of Done

Those documents support the vNext hybrid approach because they prioritise:
- engagement over presentation
- actionability
- evidence quality
- currentness
- executive usefulness
- economic honesty
