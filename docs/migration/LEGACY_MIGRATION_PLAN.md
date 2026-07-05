# Legacy Migration Plan

## Objective

Move proven legacy executive-knowledge acquisition behaviour into Alfred v5 provider architecture without making Alfred depend on Hermes or the legacy VPS.

## Stage 1

### Wrap legacy implementation

Build wrapper adapters around the proven behaviour only:

- vault traversal
- exclusions
- folder classification
- objective extraction
- project extraction
- follow-up extraction
- open-loop extraction
- daily brief composition

Rules:

- preserve observable behaviour
- preserve existing executive folder semantics
- keep runtime read-only
- keep the wrapping boundary at `VaultNote -> ProviderMatch -> VaultEntity`

Deliverable:

- provider wrappers that emulate legacy extraction behaviour behind Alfred v5 interfaces

Exit criteria:

- Alfred v5 can run end-to-end using wrapped legacy capability boundaries
- no Hermes runtime dependency exists in production execution

## Stage 2

### Replace one capability at a time

Replacement order:

1. vault traversal and exclusions
2. folder classification
3. objective provider
4. project provider
5. follow-up provider
6. open-loop provider
7. daily brief / executive briefing composition

Rules:

- only replace one capability at once
- compare observable output before and after each replacement
- keep canonical entity resolution and graph shared

Validation for each replacement:

- same source notes
- same entity counts
- same resolved aliases
- same downstream ExecutiveState behaviour
- no synthetic content introduced

## Stage 3

### Retire legacy code only after identical observable behaviour

Legacy code may be retired only when all conditions are true:

- output parity is demonstrated for the capability being replaced
- no dependency on VPS/Hermes runtime remains
- production validation remains green
- executive outputs remain evidence-backed

Observable parity means:

- same domain coverage
- same exclusion behaviour
- same relationship acquisition behaviour
- same end-user dashboard/briefing semantics for evidence-backed content

## Risks

- replacing traversal and classification together would hide regressions
- generated reports may contaminate extraction if exclusions drift
- semantic infrastructure may be mistaken for source-of-truth logic
- briefing code may accidentally fabricate upstream entities if not kept downstream

## Recommendation

Adopt a two-layer architecture permanently:

- Layer 1: canonical vault acquisition
- Layer 2: downstream intelligence and presentation

Legacy behaviour belongs only in Layer 1 wrappers until each capability is cleanly replaced.
