This is how I would write it as a **foundational AI product design manifesto** for an AI coding platform.

The objective is not to tell the AI *what screens to build*. The objective is to tell the AI *how to think about the product* when making design and architecture decisions.

Importantly, I would explicitly instruct the AI to optimise for **simplicity, maintainability, auditability and regulatory compliance**, not technical sophistication.

***

# AI Product Design Principles

## Foundational Architecture & Governance Requirements

### Purpose

This document defines the mandatory design principles that must be followed when designing, implementing, and maintaining this product.

The objective is to build a practical, maintainable, AI-enabled platform that can be understood, operated and supported by a normal business and technology team.

The goal is **not** to create the most technically advanced solution possible.

The goal is to create a solution that:

* Delivers measurable business outcomes.
* Can be easily understood by product owners and administrators.
* Can be operated without specialist AI expertise.
* Can be audited and evidenced.
* Supports regulatory compliance.
* Can evolve safely over time.
* Remains maintainable if the original developers are no longer available.

***

# Principle 1: Simplicity Over Complexity

## Requirement

Always choose the simplest design that achieves the business outcome.

Avoid introducing:

* Complex frameworks
* Excessive abstractions
* Novel architectural patterns
* Unnecessary microservices
* Over-engineering

## Design Guidance

The platform should favour:

* Clear workflows
* Simple user journeys
* Readable code
* Configurable behaviour
* Minimal moving parts

## Success Criteria

A competent product owner should be able to explain:

* How the solution works
* How decisions are made
* How workflows operate
* How configuration changes can be made

without requiring a developer.

***

# Principle 2: Human-Led, AI-Assisted

## Requirement

AI must support decisions.

AI must not become an uncontrolled decision maker.

## Design Guidance

The system should:

* Recommend
* Classify
* Prioritise
* Summarise
* Assist

The system should not:

* Make irreversible decisions autonomously
* Execute material regulatory actions without approval

## Success Criteria

Every AI output should support:

* Accept
* Reject
* Override
* Escalate

by a human user.

***

# Principle 3: Explainability by Default

## Requirement

Users must understand why the AI produced an output.

AI outputs without explanation are not acceptable.

## Design Guidance

All AI-generated outputs should be accompanied by:

* Reasoning summary
* Source references
* Confidence indicators
* Evidence links

## Success Criteria

A user can answer:

* Why was this decision suggested?
* What information was used?
* What evidence supports it?

without technical assistance.

***

# Principle 4: Auditability by Design

## Requirement

Every significant AI interaction must be auditable.

Audit functionality is not optional.

## Design Guidance

The platform must maintain:

* Full decision history
* Workflow history
* User actions
* Approvals
* Exceptions
* Escalations

## Success Criteria

An auditor should be able to reconstruct:

* What occurred
* Who performed it
* When it occurred
* What information was available at the time
* What AI component participated

using platform evidence alone.

***

# Principle 5: Regulatory Compliance by Design

## Requirement

The product must support compliance with:

* EU AI Act
* DORA
* GDPR
* FCA requirements
* Internal governance frameworks

where applicable.

## Design Guidance

Compliance controls must be embedded into workflows.

Compliance cannot rely upon users remembering to perform additional steps outside the system.

## Mandatory Capabilities

* AI inventory
* Model ownership
* Risk classification
* Review lifecycle management
* Approval workflows
* Evidence retention

## Success Criteria

The platform can produce evidential records demonstrating compliance activity.

***

# Principle 6: Observability by Design

## Requirement

Observability is a first-class capability.

It is not a technical dashboard for developers.

It is a business and governance capability.

## Design Guidance

The platform must continuously monitor:

### AI Activity

* Model usage
* Prompt execution
* Recommendation volumes
* AI-assisted decisions

### Quality

* User acceptance rates
* Override rates
* Exception rates
* Confidence trends

### Risk

* Failed decisions
* Escalations
* Compliance breaches
* Suspicious behaviour

## Success Criteria

Management can answer:

* Is AI helping?
* Is AI trusted?
* Is AI accurate?
* Is AI creating risk?
* Is AI compliant?

from standard dashboard reporting.

***

# Principle 7: Evidence Retention by Default

## Requirement

Evidence must be retained automatically.

Evidence collection must never rely on users remembering to save records manually.

## Design Guidance

The platform should automatically store:

* Inputs
* Outputs
* Supporting evidence
* User decisions
* Approvals
* Exceptions

## Success Criteria

An auditor can retrieve evidence without requiring screenshots, emails or external documentation.

***

# Principle 8: Adaptability Over Customisation

## Requirement

The platform must be easy to evolve.

Configuration should be preferred over development.

## Design Guidance

Business changes should primarily be addressed through:

* Configuration
* Rules
* Workflow changes
* Metadata

rather than new code.

## Success Criteria

Most process changes should not require a developer.

***

# Principle 9: Interoperability First

## Requirement

The platform must assume it will coexist with other systems.

## Design Guidance

Every major capability should expose standard interfaces.

The platform should avoid creating proprietary dependencies wherever possible.

## Success Criteria

Core services can be replaced or upgraded without rebuilding the entire solution.

***

# Principle 10: Outcome-Focused Measurement

## Requirement

Success must be measured through business outcomes.

Not AI activity.

## Do Not Measure

* Number of prompts
* Number of chatbot interactions
* Token consumption

## Measure

* Time saved
* Risk reduced
* Process efficiency
* Compliance effectiveness
* User adoption
* Decision quality

## Success Criteria

Every AI capability must have a measurable business objective.

***

# Principle 11: Data Governance Before AI

## Requirement

The platform must treat data quality as a prerequisite.

Bad data cannot be solved by better AI.

## Design Guidance

The platform should:

* Identify data ownership
* Track lineage
* Apply classification
* Validate quality

before significant AI processing occurs.

## Success Criteria

Users know:

* Where data came from
* Who owns it
* Whether it is trusted
* Whether it is suitable for AI usage

***

# Principle 12: Progressive AI Maturity

## Requirement

Do not build for hypothetical future complexity.

Build for today's needs while enabling future growth.

## Design Guidance

Start with:

* Single AI services
* Simple workflows
* Human approvals
* Basic automation

Expand only when justified through measurable value.

## Explicitly Avoid

* Premature multi-agent architectures
* Autonomous enterprise-wide AI orchestration
* Complex distributed decision engines
* Functionality without a validated business case

## Success Criteria

Every layer of complexity can be justified by an identified business outcome.

***

# Final Instruction To The AI Development Platform

When design choices are available:

1. Choose the simplest maintainable solution.
2. Prefer configuration over coding.
3. Prefer transparency over sophistication.
4. Prefer evidence over assumptions.
5. Prefer governance over automation.
6. Prefer observability over hidden intelligence.
7. Prefer human accountability over autonomous decision making.
8. Design every capability as though it may need to be explained to an auditor, regulator, product owner or future support team.

**If a proposed feature improves technical sophistication but reduces explainability, maintainability, operability, auditability or regulatory compliance, reject the feature and choose the simpler alternative.**

This principle takes precedence over all other architectural considerations.

***

Personally, I would make **Observability, Auditability and Evidence Retention** the three non-negotiable design pillars. Most AI products focus on generating outputs; regulated firms need to prove **how** the output was produced, **why** it was produced, **whether it was used**, and **whether it complied with governance requirements**. If those three pillars are built properly, EU AI Act, FCA, DORA and internal audit requirements become significantly easier to satisfy.
