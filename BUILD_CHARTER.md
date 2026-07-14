# Build Charter

Source material:
- [PMC-Design-Principles.md](docs/source/PMC-Design-Principles.md)
- [ARCHITECTURE_CONSTITUTION.md](ARCHITECTURE_CONSTITUTION.md)

## Governing Product Purpose

“Alfred is an AI-assisted Executive System of Engagement that converts evidence into understanding, decisions and action.

Alfred is not a system for displaying what it knows.

Any capability that ends at presentation is incomplete.”

## Purpose

This charter governs all Alfred product and user-experience decisions.

Its purpose is to ensure Alfred is:
- simple enough to operate and support
- evidence-backed and auditable
- useful to executives in real work
- safe for regulated environments
- designed as a system of engagement rather than a system of passive display

The goal is not to build the most sophisticated AI product.

The goal is to build a practical executive operating product that helps the user:

Understand -> Investigate -> Decide -> Act -> Track -> Resolve

## Non-Negotiable Principles

### 1. Simplicity Over Complexity

Choose the simplest maintainable design that achieves the outcome.

Avoid:
- unnecessary abstractions
- complex orchestration for unproven value
- novel patterns that reduce operability
- technical sophistication with no user benefit

Success means a competent product owner can explain how the capability works and how it is operated.

### 2. Human-Led, AI-Assisted

AI recommends, classifies, prioritises, summarises and assists.

AI does not become an uncontrolled decision maker.

Every significant AI output should support human actions such as:
- accept
- reject
- override
- escalate

### 3. Explainability by Default

Users must be able to understand:
- why Alfred surfaced something
- what evidence was used
- what confidence Alfred has
- what assumptions or gaps remain

An unexplained AI output is not complete.

### 4. Auditability by Design

Every significant AI-assisted workflow must preserve:
- what happened
- who did it
- when
- what evidence was available
- what AI contribution occurred

Audit is a primary product requirement, not a later add-on.

### 5. Regulatory Compliance by Design

Alfred must support compliance-friendly operation for regulated environments.

That means:
- controlled workflows
- recorded approvals and exceptions
- retained evidence
- visible model and workflow ownership
- explainable decisions

Compliance cannot depend on users remembering off-system steps.

### 6. Observability by Design

Observability is a business and governance capability, not just technical telemetry.

Management must be able to understand:
- whether Alfred is helping
- whether Alfred is trusted
- whether Alfred is accurate enough
- whether Alfred is creating risk
- whether Alfred is being operated safely

### 7. Evidence Retention by Default

Evidence must be automatically retained.

Retention must include:
- inputs
- outputs
- source evidence
- user decisions
- approvals
- exceptions

Evidence collection must not rely on manual user discipline.

### 8. Adaptability Over Customisation

Prefer:
- configuration
- rules
- metadata
- workflow shaping

over repeated bespoke engineering.

Product change should normally not require code unless there is a genuine capability gap.

### 9. Interoperability First

Alfred must coexist with other systems and avoid avoidable lock-in.

Core capabilities should be replaceable or evolvable without rebuilding the whole product.

### 10. Outcome-Focused Measurement

Success is measured by business outcomes, not AI activity.

Do not treat:
- prompt counts
- chat volume
- token consumption

as product success.

Measure instead:
- time saved
- risk reduced
- decision quality improved
- process friction removed
- user adoption
- compliance effectiveness

### 11. Data Governance Before AI

Bad data is not fixed by more AI.

Before significant AI processing, Alfred should make clear:
- where the data came from
- who owns it
- whether it is trusted
- whether it is suitable for the intended use

### 12. Progressive AI Maturity

Do not build for hypothetical complexity.

Start with simple, valuable, governed workflows and add complexity only when justified by measurable value.

Explicitly avoid premature:
- multi-agent complexity
- autonomous enterprise orchestration
- speculative AI features without a business case

### 13. Engagement Over Presentation

Alfred is not a system for displaying what it knows.

Alfred exists to help the user:

Understand -> Investigate -> Decide -> Act -> Track -> Resolve

A static page, card, list, insight or recommendation is not complete merely because it displays information.

Every significant user-facing item should enable appropriate engagement such as:
- investigate
- ask Alfred
- assign
- act
- decide
- link
- defer
- escalate
- resolve
- dismiss

If the user asks “So what?” or “What can I do with this?”, the product must have an answer.

### 14. One Matter, One Primary Operational State

The same underlying matter must not independently exist as multiple active executive records.

A matter may have many relationships, but it must have one primary operational classification at a time, for example:
- Risk
- Open Loop
- Follow-up
- Project
- Decision

Views such as Plan Today may reference the canonical matter but must not create another duplicate record.

Movement between states must preserve:
- history
- relationships
- evidence
- audit trail

### 15. Atomicity Before Intelligence

Before Alfred prioritises, summarises, links, recommends or enriches content, it must determine whether the source contains:
- one independently actionable matter, or
- several independently actionable matters

Every independently actionable matter must have:
- its own identity
- lifecycle
- status
- relationships
- workflow

Multiple activities must not be collapsed into one paragraph and presented as one record.

### 16. Actionability by Default

A recommendation should have a corresponding executable workflow wherever reasonably possible.

If Alfred says:
- assign an owner
- review this risk
- approve this decision
- escalate this issue

the interface should provide matching actions where appropriate.

A recommendation with no way to progress the matter is incomplete.

### 17. Business Language Over System Language

Do not expose implementation concepts as executive insights.

Terms such as:
- graph linkage
- canonical contract
- extraction pipeline
- semantic equivalence
- markdown filenames
- internal confidence machinery

must not appear as primary executive language unless the user is explicitly on a technical administration or system-health page.

Technical conditions must be translated into business implications or kept in diagnostics.

### 18. Evidence Must Inform, Not Burden

Evidence presentation must be layered.

Primary:
- human-readable evidence summary
- what the evidence says
- why it matters

Secondary:
- excerpts
- relationships
- supporting context

Tertiary:
- provenance paths
- filenames
- raw source locations

A markdown filename is provenance.
It is not an executive insight.

### 19. Current Reality Over Historical Noise

Before surfacing a matter as active, Alfred must assess whether it is:
- still current
- completed
- superseded
- attached to a closed project
- contradicted by newer evidence
- still relevant

Historical evidence may inform understanding, but it must not automatically become current work.

### 20. Executive Attention Is Scarce

The landing page has the highest quality threshold in Alfred.

An item should earn executive attention only when Alfred can explain:
- what happened
- why it matters
- why now
- what evidence supports it
- what should happen next

Internal data-quality defects must not appear as executive Burning Fires.

### 21. AI Must Add Value Beyond Retrieval

A searchable list of records, headings or filenames is not enough.

Alfred should reduce cognitive work through:
- context
- synthesis
- relationships
- implications
- prioritisation
- recommendations
- gap identification
- options
- proposed next actions

The original evidence must remain available, but the user must not be required to reconstruct meaning manually from raw source files.

### 22. No Capability Without a Complete User Loop

A capability is not complete because:
- a card exists
- a count exists
- a page opens
- data renders
- a test passes

A capability is complete only when the user can progress the underlying work through:

Understand -> Investigate -> Decide -> Act -> Track -> Resolve

## Mandatory Pre-Build Gate

Before implementing or materially changing any user-facing capability, the development process must answer:

1. Who is the user?
2. What job are they trying to accomplish?
3. What business or executive outcome improves?
4. What evidence is available?
5. What value does AI add beyond retrieval?
6. What can the user do with the result?
7. What changes after the user acts?
8. How is the outcome tracked?
9. How is the matter resolved or closed?
10. How will success be measured?

If these questions cannot be answered, do not build the feature.

## Mandatory Product Acceptance Gate

Every user-facing capability must be assessed against all of the following:

- Understandable
- Current
- Evidence-backed
- Evidence explained in human language
- AI adds value beyond retrieval
- User can interrogate it
- User can act
- Action persists
- State changes after action
- Duplicate matters are prevented
- Audit trail exists
- Capability reduces executive effort
- Complete user loop exists

Any NO means the capability is not complete.

Technical tests passing does not override this gate.

## Governance Precedence

1. `BUILD_CHARTER.md` governs product and user-experience decisions.
2. `ARCHITECTURE_CONSTITUTION.md` governs architectural integrity.
3. Definition of Done governs completion scope.
4. Task-local prompts govern implementation only where they do not conflict with the above.

If a task can technically be completed in a way that violates `BUILD_CHARTER.md`, the implementation must be rejected.

Do not silently reinterpret the charter to satisfy a task.

## Permanent Build Rules

- Do not ship presentation without engagement for significant executive work.
- Do not surface duplicate active matters across multiple states as if they are separate work.
- Do not collapse multiple actionable matters into one displayed record.
- Do not promote historical noise into current executive work without current evidence.
- Do not expose technical-system language as executive language on business surfaces.
- Do not surface evidence provenance as if it were the insight itself.
- Do not treat a route, card, count or static detail page as completion.
- Do not claim AI value when Alfred is only listing or retrieving.
- Do not allow internal data-quality defects to dominate the landing page.
- Do not allow a recommendation to exist without a way to progress it where reasonably possible.

## Definition of Product Completeness Under This Charter

A capability is complete only when all of the following are true:

- the user can understand the matter
- the matter is current and evidence-backed
- Alfred explains why it matters now
- the user can investigate the matter
- the user can make or record a decision
- the user can act on it
- the action persists
- Alfred reflects the changed state
- history and audit remain visible
- the matter can be tracked to closure

Anything short of this is incomplete, regardless of code quality or test coverage.
