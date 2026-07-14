# Product Reset Audit

Audit date:
- 2026-07-14

Live product audited:
- VPS Alfred UI and API on `127.0.0.1:4173`
- deployed commit observed in live refresh status: `3c636c8`

Evidence sources used for this audit:
- live `dashboard-home.json`
- live domain payloads:
  - `objectives.json`
  - `projects.json`
  - `decisions.json`
  - `followups.json`
  - `open-loops.json`
  - `risks.json`
  - `meetings.json`
  - `governance.json`
  - `refresh-status.json`
- live browser verification of:
  - landing page
  - objectives register
  - objective detail
  - projects register
- current route definitions in [web/src/App.tsx](web/src/App.tsx)
- current page implementations under [web/src/pages](web/src/pages)

This audit applies the Build Charter, not implementation sympathy.

## Executive Summary

Current conclusion:
- The platform has real reusable foundations.
- The live product does not meet the Build Charter.
- The most serious failure is that many capabilities stop at presentation rather than engagement.
- Several core executive surfaces surface technical/data-quality conditions as executive insight.
- Several routes are still placeholders but appear inside the product as if they belong to the operating model.
- Matter atomicity is not reliable enough: multiple live open matters are collapsed into single paragraphs and duplicated across views.

Overall classification:
- Reusable foundation exists.
- Product reset is justified.
- Recovery is economically sensible only if the next phase is governed by the Build Charter and stops shipping presentation-only features.

## Audit Method

For each capability the audit records:
- current live behaviour
- user job to be done
- intended outcome
- charter principles passed
- charter principles failed
- specific live evidence
- classification
- recommended product behaviour
- required user loop
- AI value required
- data/evidence dependencies
- reusable existing components
- estimated implementation complexity
- dependencies
- risks

## Capability Audit

### 1. Main Landing Page

- Capability: Main landing page
- Current live behaviour:
  - Immediate snapshot boot works.
  - The page shows `What do I need to focus on next?`, Burning Fires, Next Best Action, Plan Today, Operating Picture, and Quick Navigation.
  - Much of the page is static readout rather than engagement.
- User job to be done:
  - Rapidly understand what materially changed and what requires action now.
- Intended outcome:
  - The executive knows what matters, why now, and can immediately progress the work.
- Charter principles passed:
  - 1 Simplicity Over Complexity
  - 3 Explainability by Default in limited form
  - 6 Observability by Design for refresh status
  - 7 Evidence Retention by Default indirectly through published snapshot
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 19 Current Reality Over Historical Noise
  - 20 Executive Attention Is Scarce
  - 21 AI Must Add Value Beyond Retrieval
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - live dashboard still elevates non-executive phrasing through its subordinate sections
  - route cards click through, but many drill-through destinations remain placeholder or static
  - the main page does not let the user progress the surfaced matters directly
- Classification: REPAIR
- Reason:
  - Snapshot loading is good and worth keeping, but the core executive home experience is still largely display-first.
- Recommended product behaviour:
  - Home should act as a command surface, not a poster.
  - Every surfaced matter should support at least one direct next action or clear drill-through into the governing workflow.
- Required user engagement loop:
  - Understand -> Investigate -> Decide -> Act
- AI value required:
  - prioritisation and current-state reduction, not merely aggregation
- Data/evidence dependencies:
  - canonical matters
  - current-state assessment
  - routeable workflows
- Reusable existing components:
  - published snapshot model
  - card layout
  - route shell
- Estimated implementation complexity: Medium
- Dependencies:
  - fix downstream domain workflows first
- Risks:
  - continuing to treat the landing page as a summary page will keep surfacing low-quality or non-actionable content

### 2. Burning Fires

- Capability: Burning Fires
- Current live behaviour:
  - shows short cards with only a type pill and summary text
  - no drill-through, no action, no explicit “why now”, no executable workflow
- User job to be done:
  - identify urgent matters that deserve immediate executive intervention
- Intended outcome:
  - the executive can open the matter, understand why it is urgent, and take action
- Charter principles passed:
  - 3 Explainability by Default only partially through text
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 17 Business Language Over System Language
  - 18 Evidence Must Inform, Not Burden
  - 20 Executive Attention Is Scarce
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - live `daily-brief.json` and `risks.json` include:
    - `AT RISK. Project has no graph linkage; review whether it is current, duplicated, or missing relationships.`
  - that is an internal modelling condition, not an executive risk
  - current dashboard implementation renders Burning Fires as non-clickable cards in [DashboardPage.tsx](web/src/pages/DashboardPage.tsx)
- Classification: REPLACE
- Reason:
  - the current concept is wrong at both content and workflow level
- Recommended product behaviour:
  - Burning Fires should contain only matters that pass the executive-attention threshold
  - each item should explain:
    - what happened
    - why it matters
    - why now
    - what evidence supports it
    - what should happen next
  - each card should drill through and expose direct actions
- Required user engagement loop:
  - Understand -> Investigate -> Decide -> Act -> Track
- AI value required:
  - triage, implication detection, urgency reasoning, executive framing
- Data/evidence dependencies:
  - canonical matter state
  - recency and closure logic
  - evidence summarisation
- Reusable existing components:
  - card styling
  - snapshot publication
- Estimated implementation complexity: Large
- Dependencies:
  - canonical matter state discipline
  - risk/open-loop cleanup
- Risks:
  - executive trust loss if internal defects continue surfacing as Burning Fires

### 3. Next Best Action

- Capability: Next Best Action
- Current live behaviour:
  - displays one action, one explanation and confidence
  - no executable action
  - no direct workflow progression
- User job to be done:
  - progress the single most important action immediately
- Intended outcome:
  - the user can take the recommended action without reconstructing the workflow manually
- Charter principles passed:
  - 3 Explainability by Default partially
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 21 AI Must Add Value Beyond Retrieval
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - [DashboardPage.tsx](web/src/pages/DashboardPage.tsx) renders the item as static text
  - no direct action is available from the card
- Classification: REPAIR
- Reason:
  - the concept is useful, but the product stops at recommendation
- Recommended product behaviour:
  - pair the recommendation with the executable next step or the authoritative drill-through
- Required user engagement loop:
  - Understand -> Act -> Track
- AI value required:
  - action selection and explanation
- Data/evidence dependencies:
  - canonical matter and relationship routing
- Reusable existing components:
  - intent/recommendation generation
- Estimated implementation complexity: Medium
- Dependencies:
  - downstream workflows
- Risks:
  - recommendation fatigue without a way to progress it

### 4. Plan Today / Execution

- Capability: Plan Today
- Current live behaviour:
  - ordered list of strings
  - no matter identity
  - no action
  - no state transition
- User job to be done:
  - translate today’s priorities into executable work
- Intended outcome:
  - the user can progress each priority and see status change
- Charter principles passed:
  - 1 Simplicity Over Complexity
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 14 One Matter, One Primary Operational State
  - 16 Actionability by Default
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - live `daily-brief.json` `recommended_agenda` duplicates matters already appearing in risks and open loops
  - [DashboardPage.tsx](web/src/pages/DashboardPage.tsx) renders Plan Today as text only
- Classification: REPLACE
- Reason:
  - it is a duplicate planning view with no operational state or actions
- Recommended product behaviour:
  - Plan Today should reference canonical matters, not create a second pseudo-record layer
  - each line should let the user open, defer, assign, mark in progress, or dismiss
- Required user engagement loop:
  - Understand -> Decide -> Act -> Track
- AI value required:
  - sequencing and workload reduction
- Data/evidence dependencies:
  - canonical matter identity and lifecycle
- Reusable existing components:
  - prioritisation logic only where output quality is acceptable
- Estimated implementation complexity: Large
- Dependencies:
  - deduped matter model
- Risks:
  - duplicate work and fragmented state

### 5. Routes / Priorities / Quick Navigation

- Capability: Quick Navigation
- Current live behaviour:
  - cards appear interactive
  - some routes land on real pages
  - several destination pages remain placeholder or static
- User job to be done:
  - jump directly into the relevant operational workspace
- Intended outcome:
  - the route takes the user to a complete, useful workflow
- Charter principles passed:
  - 1 Simplicity Over Complexity
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - [DashboardPage.tsx](web/src/pages/DashboardPage.tsx) maps route cards to pages
  - [App.tsx](web/src/App.tsx) still routes many product areas to `PlaceholderPage`
- Classification: REPAIR
- Reason:
  - navigation itself is useful, but the product misrepresents maturity by exposing incomplete destinations as normal routes
- Recommended product behaviour:
  - only expose routes that support meaningful engagement
  - demote future routes into admin/roadmap state or hide them until real
- Required user engagement loop:
  - Understand -> Investigate
- AI value required:
  - none in the navigation layer itself
- Data/evidence dependencies:
  - route readiness
- Reusable existing components:
  - route shell
  - link cards
- Estimated implementation complexity: Small
- Dependencies:
  - destination readiness
- Risks:
  - trust erosion from dead-end interactions

### 6. Meetings

- Capability: Meetings / Meeting drill-through
- Current live behaviour:
  - live meeting subject is `100 BACK WORKOUT`
  - summary is static
  - page shows plain related context and discussion bullets only
  - no meeting-specific workflow actions
- User job to be done:
  - prepare for an actual executive meeting
- Intended outcome:
  - the user gets a concise, relevant, actionable briefing
- Charter principles passed:
  - 3 Explainability by Default partially
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 17 Business Language Over System Language
  - 19 Current Reality Over Historical Noise
  - 20 Executive Attention Is Scarce
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - live `meetings.json` subject is `100 BACK WORKOUT`
  - live executive summary contains workout instructions rather than executive meeting prep
  - [MeetingsPage.tsx](web/src/pages/MeetingsPage.tsx) is entirely static readout
- Classification: REPLACE
- Reason:
  - both relevance and workflow are wrong
- Recommended product behaviour:
  - only current executive meetings should surface
  - each meeting should support:
    - prepare
    - add question
    - add decision sought
    - link follow-up
    - record outcome
- Required user engagement loop:
  - Understand -> Investigate -> Decide -> Act -> Track
- AI value required:
  - concise briefing, stakeholder context, question generation, delta detection
- Data/evidence dependencies:
  - meeting recency and relevance filters
  - linked entities
- Reusable existing components:
  - meeting page shell only
- Estimated implementation complexity: Large
- Dependencies:
  - current meeting identification quality
- Risks:
  - user distrust if irrelevant workout or personal notes are surfaced as executive meetings

### 7. Objectives Register

- Capability: Objectives register
- Current live behaviour:
  - six canonical objectives now render correctly
  - cards are clickable and no markdown artefacts appear
  - however most cards show sparse management content and weak linkage
- User job to be done:
  - understand executive objectives and navigate into the management workspace
- Intended outcome:
  - the user sees the right objective set and can drill into management work
- Charter principles passed:
  - 1 Simplicity Over Complexity
  - 3 Explainability by Default
  - 7 Evidence Retention by Default
  - 18 Evidence Must Inform, Not Burden partially
- Charter principles failed:
  - 13 Engagement Over Presentation partly
  - 16 Actionability by Default partly
  - 21 AI Must Add Value Beyond Retrieval partly
- Specific evidence from the live product:
  - live `objectives.json` correctly shows the six canonical objective titles
  - live browser register shows clickable cards
  - many objective cards show:
    - owner `Not defined`
    - no supporting projects
    - no linked decisions
    - no open actions
- Classification: REPAIR
- Reason:
  - the objective set is now correct, but the management layer is still shallow
- Recommended product behaviour:
  - keep the canonical set
  - strengthen engagement, evidence explanation and relationship usefulness
- Required user engagement loop:
  - Understand -> Investigate -> Decide -> Act -> Track
- AI value required:
  - identify linkage gaps and propose next actions
- Data/evidence dependencies:
  - project, decision, open-loop and follow-up linkage quality
- Reusable existing components:
  - objective register
  - stable routes
  - objective detail shell
  - SMART assessment shell
- Estimated implementation complexity: Medium
- Dependencies:
  - upstream linkage quality
- Risks:
  - objectives remain nominal rather than operational

### 8. Objective Detail Workspace

- Capability: Objective detail view
- Current live behaviour:
  - direct routes work
  - SMART assessment is visible
  - management fields and persistence exist
  - but recommendations and evidence explanation are still weak and often sparse
- User job to be done:
  - manage an objective as a live executive commitment
- Intended outcome:
  - the user can understand, amend, enrich, link and review the objective
- Charter principles passed:
  - 3 Explainability by Default
  - 4 Auditability by Design
  - 7 Evidence Retention by Default
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
- Charter principles failed:
  - 18 Evidence Must Inform, Not Burden
  - 21 AI Must Add Value Beyond Retrieval partly
- Specific evidence from the live product:
  - live browser objective detail route works for `/objectives/be4aecfea690`
  - the detail page exposes management fields, SMART assessment and persistence surfaces
  - evidence is still often shown mainly as provenance paths
- Classification: REPAIR
- Reason:
  - this is one of the stronger foundations in the current product, but not fully charter-complete
- Recommended product behaviour:
  - retain the workspace
  - improve human-readable evidence explanation and actionable linkage quality
- Required user engagement loop:
  - Understand -> Investigate -> Decide -> Act -> Track
- AI value required:
  - enrich weak definitions and relationship gaps without inventing facts
- Data/evidence dependencies:
  - richer linkage and review evidence
- Reusable existing components:
  - detail page
  - persistence
  - audit
  - SMART proposal controls
- Estimated implementation complexity: Medium
- Dependencies:
  - linkage repair
- Risks:
  - if evidence remains mostly provenance, the user still has to reconstruct meaning manually

### 9. Projects Register

- Capability: Projects register
- Current live behaviour:
  - full canonical 38 projects are available
  - searchable/filterable/sortable register exists
  - live list payload is now reduced to `36958` bytes
- User job to be done:
  - review active projects and open the relevant project workspace
- Intended outcome:
  - the user can manage delivery work from a reliable project list
- Charter principles passed:
  - 1 Simplicity Over Complexity
  - 3 Explainability by Default
  - 13 Engagement Over Presentation partially
  - 19 Current Reality Over Historical Noise partially
- Charter principles failed:
  - 17 Business Language Over System Language in some recommendations
  - 20 Executive Attention Is Scarce where closed or weak projects still surface
  - 21 AI Must Add Value Beyond Retrieval only partially
- Specific evidence from the live product:
  - live `projects.json` count is `38`
  - live browser register shows 38 visible and canonical
  - daily brief and recommendations still include:
    - `Assign an accountable owner for Project Vinnie (WATCH)`
  - user explicitly identified closed Project Vinnie being surfaced as current work
- Classification: REPAIR
- Reason:
  - the register is usable, but currentness and recommendation quality are not charter-complete
- Recommended product behaviour:
  - keep the register and workspace pattern
  - improve currentness, closure and recommendation quality
- Required user engagement loop:
  - Understand -> Investigate -> Decide -> Act -> Track
- AI value required:
  - identify project risk, stale projects, decision blockers and relevance
- Data/evidence dependencies:
  - project state, closure state, recency and linked matter quality
- Reusable existing components:
  - register
  - filters/sort
  - detail routing
  - persistence
- Estimated implementation complexity: Medium
- Dependencies:
  - currentness assessment
- Risks:
  - stale or closed projects continue to compete for executive attention

### 10. Project Detail Workspace

- Capability: Project detail view
- Current live behaviour:
  - persistence, audit, relationships and management fields exist
  - direct routes work
  - detail payload is now isolated behind per-record drill-through
- User job to be done:
  - manage a project as an active delivery matter
- Intended outcome:
  - the user can update state, manage links, add notes and milestones, and track delivery
- Charter principles passed:
  - 4 Auditability by Design
  - 7 Evidence Retention by Default
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
- Charter principles failed:
  - 18 Evidence Must Inform, Not Burden partly
  - 19 Current Reality Over Historical Noise partly
- Specific evidence from the live product:
  - live direct route loads project detail
  - project workspace persistence was already proven live in prior product work
  - detail payload is no longer forced onto list-page boot
- Classification: KEEP
- Reason:
  - this is currently the strongest governed engagement pattern in the product
- Recommended product behaviour:
  - retain and use as one of the reference patterns for other domains
- Required user engagement loop:
  - Understand -> Investigate -> Decide -> Act -> Track
- AI value required:
  - targeted enrichment and relationship assistance
- Data/evidence dependencies:
  - current project evidence
- Reusable existing components:
  - almost all of this capability
- Estimated implementation complexity: Small
- Dependencies:
  - none for retention
- Risks:
  - preserving currentness quality remains necessary

### 11. Decisions Register

- Capability: Decisions register
- Current live behaviour:
  - searchable register exists
  - direct detail routes exist
  - read-only only
  - behaves mainly like a system-of-record list
- User job to be done:
  - understand decisions, decide whether action is required, and progress or resolve them
- Intended outcome:
  - decisions become an engagement workflow, not just a note register
- Charter principles passed:
  - 3 Explainability by Default
  - 7 Evidence Retention by Default
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 18 Evidence Must Inform, Not Burden
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - [DecisionsPage.tsx](web/src/pages/DecisionsPage.tsx) is a searchable register only
  - [DecisionDetailPage.tsx](web/src/pages/DecisionDetailPage.tsx) shows static detail, related entities and evidence
  - there are no decision workflow actions
- Classification: REPAIR
- Reason:
  - correct register foundation exists, but the user cannot progress a decision
- Recommended product behaviour:
  - add decision workflows such as:
    - accept
    - amend
    - assign
    - approve
    - reject
    - close
    - link to project/objective/risk
- Required user engagement loop:
  - Understand -> Decide -> Act -> Track -> Resolve
- AI value required:
  - rationale summarisation, dependency identification, blocked-decision detection
- Data/evidence dependencies:
  - decision status lifecycle and ownership
- Reusable existing components:
  - register
  - detail shell
  - stable routes
- Estimated implementation complexity: Medium
- Dependencies:
  - persisted workflow actions
- Risks:
  - decisions remain dead records rather than operational control points

### 12. Follow-ups

- Capability: Follow-ups full collection
- Current live behaviour:
  - full canonical `61` items now reach the live API and page
  - page shows KPI counts, a top-3 summary and the full collection
  - the full collection is a static list with evidence/provenance and no workflow
- User job to be done:
  - review, assign, progress, defer, close and track follow-up actions
- Intended outcome:
  - the user can move follow-ups through their lifecycle
- Charter principles passed:
  - 7 Evidence Retention by Default
  - 13 Engagement Over Presentation only at the navigation level
- Charter principles failed:
  - 16 Actionability by Default
  - 18 Evidence Must Inform, Not Burden
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - live `followups.json` count is `61`
  - [FollowupsPage.tsx](web/src/pages/FollowupsPage.tsx) renders articles only; no buttons, no transitions, no detail route
  - source path is presented prominently; evidence is mainly raw path lists
  - the KPI summary is still just the first due-today items rather than an executive summary
- Classification: REPAIR
- Reason:
  - collection completeness is fixed, but the product still stops at display
- Recommended product behaviour:
  - keep the canonical collection
  - add workflow actions and a detail route
  - replace “first item” summary with a meaningful executive follow-up summary
- Required user engagement loop:
  - Understand -> Investigate -> Act -> Track -> Resolve
- AI value required:
  - summarise what needs attention, why, and by whom
- Data/evidence dependencies:
  - owner, due date, related matter, status transitions
- Reusable existing components:
  - collection page
  - counts
  - published domain endpoint
- Estimated implementation complexity: Medium
- Dependencies:
  - work-item action model
- Risks:
  - static lists create backlog visibility without backlog control

### 13. Open Loops

- Capability: Open Loops full collection
- Current live behaviour:
  - full canonical `208` items reach the live API and page
  - many items are still rendered as long multi-matter paragraphs
  - page is static and has no operational workflow
- User job to be done:
  - understand unresolved matters, identify owners, and drive them to closure
- Intended outcome:
  - each open matter is atomic, actionable and trackable
- Charter principles passed:
  - 7 Evidence Retention by Default
- Charter principles failed:
  - 14 One Matter, One Primary Operational State
  - 15 Atomicity Before Intelligence
  - 16 Actionability by Default
  - 18 Evidence Must Inform, Not Burden
  - 19 Current Reality Over Historical Noise
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - live `daily-brief.json` `open_loops_blocking_progress` contains extremely long collapsed paragraphs representing multiple independent matters
  - [OpenLoopsPage.tsx](web/src/pages/OpenLoopsPage.tsx) renders a static list with no drill-through and no workflow
  - watchlist-style and summary-style text remains blended into some displayed items
- Classification: REPLACE
- Reason:
  - this domain still violates matter atomicity and engagement rules
- Recommended product behaviour:
  - one open matter, one record
  - direct actions such as assign, defer, escalate, resolve, convert to risk/decision/follow-up where appropriate
- Required user engagement loop:
  - Understand -> Investigate -> Decide -> Act -> Track -> Resolve
- AI value required:
  - split, classify, summarise, prioritise and detect blockers
- Data/evidence dependencies:
  - atomic work-item extraction quality
  - currentness assessment
- Reusable existing components:
  - published full collection plumbing
  - counts
- Estimated implementation complexity: Large
- Dependencies:
  - matter atomicity repair
- Risks:
  - one collapsed paragraph can hide several unrelated executive matters

### 14. Risks

- Capability: Risks route and risk model
- Current live behaviour:
  - dedicated `/risks` route is a placeholder
  - live `risks.json` is only a thin summary list
  - current risk signals are partly generated from internal data-quality conditions and open-loop text blobs
- User job to be done:
  - identify real executive risks, understand impact, decide treatment, and track mitigation
- Intended outcome:
  - risks are explicit, current, explainable and actionable
- Charter principles passed:
  - almost none at the product level
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 17 Business Language Over System Language
  - 19 Current Reality Over Historical Noise
  - 20 Executive Attention Is Scarce
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - live `risks.json` includes `Project has no graph linkage`
  - [App.tsx](web/src/App.tsx) routes `/risks` to a placeholder page
  - there is no risk workflow
- Classification: REPLACE
- Reason:
  - the live capability is not a risk product; it is a partial symptom list
- Recommended product behaviour:
  - explicit risk register with:
    - risk statement
    - why it matters
    - current impact
    - owner
    - mitigation
    - status
    - evidence
    - actions
- Required user engagement loop:
  - Understand -> Investigate -> Decide -> Act -> Track -> Resolve
- AI value required:
  - risk identification, consequence framing, treatment options, gap detection
- Data/evidence dependencies:
  - current matter quality
  - closure logic
  - relationship quality
- Reusable existing components:
  - snapshot endpoint pattern only
- Estimated implementation complexity: Large
- Dependencies:
  - matter and relationship repair
- Risks:
  - continued surfacing of internal defects as executive risk destroys trust

### 15. Knowledge Graph / Company Deduplication

- Capability: Knowledge / Knowledge Graph
- Current live behaviour:
  - static counts and top nodes
  - no drill-through into companies, people, duplicates or relationships
  - company route is still placeholder
- User job to be done:
  - inspect relationship coverage, dedup issues and counterparty context
- Intended outcome:
  - the user can understand and fix knowledge coverage where it affects executive work
- Charter principles passed:
  - 6 Observability by Design partially
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 18 Evidence Must Inform, Not Burden
  - 21 AI Must Add Value Beyond Retrieval
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - [KnowledgePage.tsx](web/src/pages/KnowledgePage.tsx) shows only counts and highest-connectivity labels
  - `/companies` is a placeholder route
- Classification: REPLACE
- Reason:
  - the current surface is not a usable knowledge-graph or company-dedup tool
- Recommended product behaviour:
  - expose graph matters through business entities and duplicates, not topology trivia
- Required user engagement loop:
  - Understand -> Investigate -> Link -> Decide -> Resolve
- AI value required:
  - duplicate detection, relationship explanation, coverage gap identification
- Data/evidence dependencies:
  - company/person/entity relationships and dedup rules
- Reusable existing components:
  - entity counts
  - top node calculations
- Estimated implementation complexity: Large
- Dependencies:
  - company/people route implementations
- Risks:
  - graph becomes a technical curiosity instead of business value

### 16. Governance / Board

- Capability: Board page and Governance route
- Current live behaviour:
  - Board page is a static governance summary and member registry
  - Governance route is still placeholder
- User job to be done:
  - prepare and run governance work with explicit decisions, agenda and issues
- Intended outcome:
  - governance becomes a working operating surface
- Charter principles passed:
  - 3 Explainability by Default
  - 7 Evidence Retention by Default partly
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - [BoardPage.tsx](web/src/pages/BoardPage.tsx) is entirely static
  - `/governance` in [App.tsx](web/src/App.tsx) is placeholder-only
- Classification: REPAIR
- Reason:
  - the board registry content is reusable, but the live governance product is incomplete
- Recommended product behaviour:
  - preserve board metadata
  - add governance workflows:
    - agenda matters
    - board decisions
    - approvals
    - unresolved governance loops
- Required user engagement loop:
  - Understand -> Decide -> Act -> Track -> Resolve
- AI value required:
  - agenda preparation, unresolved decision surfacing, risk/governance synthesis
- Data/evidence dependencies:
  - board matters, decisions and governance loops
- Reusable existing components:
  - board registry
  - cadence sections
- Estimated implementation complexity: Medium
- Dependencies:
  - governance route and decision workflows
- Risks:
  - a governance page that cannot progress governance work is ceremonial only

### 17. Organisation Design

- Capability: People / Organisation Design
- Current live behaviour:
  - no true organisation-design workspace exists
  - `/people` is placeholder-only
- User job to be done:
  - understand ownership, accountability, load and organisational gaps
- Intended outcome:
  - the user can manage people/accountability structure tied to work
- Charter principles passed:
  - none at live capability level
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - [App.tsx](web/src/App.tsx) routes `/people` to `PlaceholderPage`
- Classification: REPLACE
- Reason:
  - there is no live capability yet
- Recommended product behaviour:
  - build from ownership/accountability use cases, not a people directory
- Required user engagement loop:
  - Understand -> Investigate -> Assign -> Track
- AI value required:
  - accountability gap detection, overload detection, stakeholder context
- Data/evidence dependencies:
  - people entities, ownership links, work-item relationships
- Reusable existing components:
  - canonical people data only
- Estimated implementation complexity: Large
- Dependencies:
  - people route and ownership model usage
- Risks:
  - hidden accountability gaps remain spread across domains

### 18. Operations

- Capability: Operations / Admin / refresh controls
- Current live behaviour:
  - live snapshot controls work
  - environment and deployment information is visible
  - operations actions are still command strings, not governed in-product workflows
  - AI Models / Integrations / System Health remain placeholders
- User job to be done:
  - monitor platform health, refresh safely, and understand operational posture
- Intended outcome:
  - operations are visible, reliable and governed
- Charter principles passed:
  - 4 Auditability by Design partly
  - 6 Observability by Design
  - 7 Evidence Retention by Default
- Charter principles failed:
  - 13 Engagement Over Presentation for most admin actions
  - 17 Business Language Over System Language on business surfaces
  - 22 No Capability Without a Complete User Loop for placeholder routes
- Specific evidence from the live product:
  - snapshot refresh is live and resilient
  - admin page exposes CLI commands as UI content in [AdminSecurityPage.tsx](web/src/pages/AdminSecurityPage.tsx)
  - `/ai-models`, `/integrations`, `/system-health` are placeholders
- Classification: REPAIR
- Reason:
  - operational visibility exists and is valuable, but several areas remain presentation-only or placeholder-only
- Recommended product behaviour:
  - keep snapshot controls and operational state
  - convert admin actions from command descriptions into governed operational workflows where needed
- Required user engagement loop:
  - Understand -> Act -> Verify
- AI value required:
  - low; mostly governance and observability
- Data/evidence dependencies:
  - runtime telemetry and snapshot status
- Reusable existing components:
  - snapshot model
  - refresh status
  - admin inventory
- Estimated implementation complexity: Medium
- Dependencies:
  - operational page shaping
- Risks:
  - exposing commands as product actions without actual execution paths creates false affordance

### 19. Ask Alfred

- Capability: Ask Alfred
- Current live behaviour:
  - read-only panel backed by precomputed answers
  - custom questions are not executed
  - recommended next actions are text only
- User job to be done:
  - interrogate the executive system with meaningful questions and progress the answer
- Intended outcome:
  - Alfred answers a real question, explains evidence and lets the user act
- Charter principles passed:
  - 3 Explainability by Default partly
  - 21 AI Must Add Value Beyond Retrieval partly
- Charter principles failed:
  - 13 Engagement Over Presentation
  - 16 Actionability by Default
  - 22 No Capability Without a Complete User Loop
- Specific evidence from the live product:
  - [AskAlfredPage.tsx](web/src/pages/AskAlfredPage.tsx) explicitly states:
    - read-only
    - custom questions are not executed yet
  - recommended actions are not executable
- Classification: REPAIR
- Reason:
  - useful answer content exists, but the product loop is incomplete
- Recommended product behaviour:
  - preserve evidence-backed answers
  - add executable next-step controls and real question execution
- Required user engagement loop:
  - Investigate -> Decide -> Act
- AI value required:
  - synthesis, option framing, implication reduction
- Data/evidence dependencies:
  - safe question execution over current snapshot/state
- Reusable existing components:
  - question patterns
  - answer card layout
- Estimated implementation complexity: Medium
- Dependencies:
  - governed action routing
- Risks:
  - user expectation exceeds actual capability

### 20. Refresh / Snapshot Controls

- Capability: Published snapshot controls
- Current live behaviour:
  - immediate page load from last-known-good snapshot
  - atomic refresh
  - previous content remains visible during refresh
  - live footer now shows correct snapshot timestamp and status
- User job to be done:
  - trust the current state and refresh it safely
- Intended outcome:
  - no blank product, no partial refresh, clear status
- Charter principles passed:
  - 1 Simplicity Over Complexity
  - 4 Auditability by Design partly
  - 6 Observability by Design
  - 7 Evidence Retention by Default
- Charter principles failed:
  - none material for this capability
- Specific evidence from the live product:
  - live `refresh-status.json` is correct
  - live UI footer shows `Status: GREEN` and current snapshot time
  - current snapshot remains available through refresh/restart
- Classification: KEEP
- Reason:
  - this is a sound operational foundation and should remain
- Recommended product behaviour:
  - retain as-is and extend only in service of user-facing domain quality
- Required user engagement loop:
  - Understand -> Act -> Verify
- AI value required:
  - none required beyond safe publication discipline
- Data/evidence dependencies:
  - snapshot publisher
- Reusable existing components:
  - all of it
- Estimated implementation complexity: Small
- Dependencies:
  - none
- Risks:
  - low; main risk is future regression

## Explicit Defect Findings

1. Burning Fires showing “Project has no Graph linkage” as an executive risk.
- Classification: REPLACE
- Evidence:
  - live `risks.json` and `daily-brief.json`

2. Burning Fires with no useful drill-through or action.
- Classification: REPLACE
- Evidence:
  - static cards in `DashboardPage.tsx`

3. Duplicate matters appearing in Risks, Open Loops and Plan Today.
- Classification: REPAIR at product level, REPLACE in risk/open-loop surfaces
- Evidence:
  - the same long unresolved paragraphs appear across `risks_escalating`, `open_loops_blocking_progress`, and `recommended_agenda`

4. Multiple Open Loops collapsed into one paragraph.
- Classification: REPLACE
- Evidence:
  - live `open_loops_blocking_progress` strings contain many separate matters in one record

5. CAPEX-at-Risk recommendation with unclear meaning, no source explanation and no drill-through.
- Classification: REPAIR
- Evidence:
  - live `top_three_priorities` contains `Assign an accountable owner for CAPEX (AT RISK)` with no in-card action path from home

6. Closed Project Vinnie being recommended as current work.
- Classification: REPAIR
- Evidence:
  - live `top_three_priorities` includes `Assign an accountable owner for Project Vinnie (WATCH)`

7. Priorities appearing interactive but not clicking through.
- Classification: REPAIR
- Evidence:
  - some route cards click, but many destination routes are placeholders or non-operational pages

8. Meeting drill-through being static and non-actionable.
- Classification: REPLACE
- Evidence:
  - `MeetingsPage.tsx` static readout only

9. Follow-up KPI showing the first item rather than a meaningful executive summary.
- Classification: REPAIR
- Evidence:
  - follow-up page `Priority Now` simply renders `daily_brief.followups_due_today`

10. Follow-up full collection being a static list with no workflow.
- Classification: REPAIR
- Evidence:
  - `FollowupsPage.tsx` has no actions or drill-through

11. Raw `.md` filenames being presented as evidence instead of human-readable evidence summaries.
- Classification: REPAIR
- Evidence:
  - multiple pages present `source_path` and provenance paths directly as visible evidence content

12. Decisions behaving as a system-of-record list rather than an engagement workflow.
- Classification: REPAIR
- Evidence:
  - decisions are read-only and non-actionable

13. “Next Best Action” not providing an executable action.
- Classification: REPAIR
- Evidence:
  - dashboard card has no action controls

14. Risks being generated from internal system/data-quality conditions rather than meaningful executive risk.
- Classification: REPLACE
- Evidence:
  - `Project has no graph linkage` in live risk surfaces

15. Capabilities ending at presentation rather than engagement.
- Classification: widespread REPAIR/REPLACE
- Evidence:
  - Burning Fires
  - Plan Today
  - Meetings
  - Follow-ups
  - Open Loops
  - Decisions
  - Board
  - Knowledge Graph
  - placeholder routes

## Economic Recovery Assessment

Estimated reusable percentage:
- approximately `55%`

What should be retained:
- published snapshot and last-known-good refresh model
- VPS deployment/runtime foundations
- canonical extraction parity already achieved for objectives, projects, follow-ups and open loops
- objective and project detail workspace patterns
- persistence and audit foundations already present in objective/project management
- stable routing, shell, and domain endpoint pattern

What should be repaired:
- landing page
- objectives enrichment and relationship usefulness
- projects currentness and recommendation quality
- decisions workflow
- follow-up workflow
- operations/admin actionability
- Ask Alfred action loop
- evidence presentation language

What should be replaced:
- Burning Fires concept as currently implemented
- current risk product
- current open-loop product
- current meeting product
- knowledge-graph/company-dedup surface
- organisation-design surface
- governance placeholder route
- placeholder routes exposed as normal navigation

What should be removed:
- any route exposed publicly that is still only placeholder scaffolding
- executive-language use of technical data-quality defects
- presentation of provenance as primary insight
- duplicate pseudo-matter views that do not own lifecycle

Major remaining engineering effort:
- matter atomicity and state-discipline for open loops and risks
- reusable engagement workflows for decisions, follow-ups and risks
- route-level action and state transitions
- evidence summarisation layer that separates business meaning from raw provenance

Major remaining product-design effort:
- redefine the landing page around executive attention and action
- redesign risk, open-loop and meeting experiences around engagement loops
- establish one consistent action grammar across domains
- decide what routes should be hidden until complete

Is recovery economically sensible?
- Yes, but only conditionally.
- Recovery is economically sensible if the team reuses:
  - extraction parity
  - published snapshot architecture
  - objective/project management patterns
  - persistence and audit foundations
- Recovery is not economically sensible if the team continues to preserve low-value presentation surfaces out of sunk-cost bias.
- A full rebuild on another platform would still need:
  - live vault integration
  - evidence retention
  - governance
  - deployment
  - refresh publishing
  - domain modelling
- Those foundations already exist here, so repairing the current platform is likely cheaper than rebuilding from zero.
- However, preserving the wrong product concepts would be more expensive than replacing them.

## Recommended Recovery Sequence

Recovery should be sequenced by:
- highest executive value
- foundational dependence
- reusable engagement pattern creation
- duplicate-work reduction
- lowest risk of further drift

### Sequence 1 — Landing Page Reset

- Replace Burning Fires, Next Best Action and Plan Today with charter-compliant matter cards.
- Remove internal-language risks from executive home.
- Ensure every surfaced item has a direct action or governing drill-through.

Why first:
- It is the highest-visibility product surface.
- It currently violates the charter most obviously.

### Sequence 2 — Canonical Matter Engagement Pattern

- Establish one reusable user loop pattern for:
  - investigate
  - decide
  - act
  - track
  - resolve
- Apply it first to Follow-ups and Decisions.

Why second:
- It creates the reusable engagement model needed across the rest of the product.

### Sequence 3 — Open Loops and Risks Reset

- Repair atomicity.
- Remove collapsed multi-matter records.
- Separate true risks from unresolved open matters and internal data-quality defects.

Why third:
- This is the largest current source of executive-noise pollution and duplicate work.

### Sequence 4 — Meeting Workflow Reset

- Replace static meeting output with current, actionable meeting preparation.
- Add question, decision sought, follow-up and outcome workflows.

Why fourth:
- Meeting quality is highly visible and currently materially wrong.

### Sequence 5 — Decisions Workflow Completion

- Add decision actions, lifecycle transitions, ownership and closure.

Why fifth:
- Decisions are already a real register and only need the engagement loop completed.

### Sequence 6 — Objective and Project Enrichment Recovery

- Improve linkage quality, evidence summaries and currentness.
- Reuse the already good objective/project workspace foundations.

Why sixth:
- The core surfaces exist and can be improved after the shared engagement pattern is established.

### Sequence 7 — Knowledge Graph / Company Dedup / Organisation Design

- Reframe these as business capabilities, not technical topology pages.

Why seventh:
- They depend on clean matter and relationship behaviour from earlier sequences.

### Sequence 8 — Governance / Board / Operations Completion

- Turn static governance/admin surfaces into governed operational products where appropriate.
- Hide or remove routes that are still placeholder-only.

Why eighth:
- These are important, but they depend less on raw extraction and more on coherent workflow patterns already established elsewhere.

## Reset Recommendation

Proceed with a governed repair, not feature continuation.

Do not resume broad domain expansion until:
- the landing page is charter-compliant
- a reusable engagement loop exists
- open loops and risks no longer violate atomicity and executive-attention rules
- placeholder routes stop pretending to be capabilities
