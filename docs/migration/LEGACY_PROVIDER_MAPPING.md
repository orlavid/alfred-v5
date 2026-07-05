# Legacy Provider Mapping

## Goal

Map proven legacy behaviour onto Alfred v5 provider interfaces without implementing replacements yet.

The rule is simple:

- preserve observable extraction behaviour
- isolate legacy logic behind provider contracts
- keep all future Alfred installs independent from the VPS runtime

## Recommended Wrapper Architecture

### LegacyObsidianTraversalAdapter

Purpose:
- preserve legacy vault traversal, exclusions, and Obsidian-first classification

Inputs:
- `vault_root: Path`

Responsibilities:
- recursive markdown scan
- executive-folder classification
- exclusion enforcement
- `VaultNote` normalization

Outputs:
- `list[VaultNote]`

This is the only wrapper that should know legacy vault traversal details.

### LegacyObjectiveProvider

Wrap:
- objective note selection from legacy traversal/classification

Inputs:
- `list[VaultNote]`

Outputs:
- `list[ProviderMatch]` with `entity_type="objective"`

Observable behaviour to preserve:
- objectives come only from objective-classified notes
- no objective synthesis from reports or recommendations

### LegacyProjectProvider

Wrap:
- project note selection from legacy traversal/classification

Outputs:
- `list[ProviderMatch]` with `entity_type="project"`

Observable behaviour to preserve:
- projects remain independent from objectives until graph/link resolution

### LegacyFollowUpProvider

Wrap:
- follow-up note selection from legacy traversal/classification

Outputs:
- `list[ProviderMatch]` with `entity_type="follow_up"`

Observable behaviour to preserve:
- follow-ups come from explicit follow-up notes, not inferred tasks

### LegacyOpenLoopProvider

Wrap:
- open-loop note selection from legacy traversal/classification

Outputs:
- `list[ProviderMatch]` with `entity_type="open_loop"`

Observable behaviour to preserve:
- open loops remain a dedicated unresolved-work domain

### LegacyDailyBriefProvider

Wrap:
- legacy-style briefing composition over analysed executive state

Inputs:
- canonical entities
- graph
- ExecutiveState-compatible aggregates

Outputs:
- daily brief sections / executive briefing sections

Observable behaviour to preserve:
- briefing is downstream of extracted evidence
- briefing does not create upstream evidence

## Supporting Shared Services

These should remain shared, not duplicated per provider:

- entity resolution
- alias handling
- wikilink extraction
- tag extraction
- relationship graph construction
- production validation

## Recommended Interface Shape

```python
class LegacyCapabilityProvider(ExecutiveKnowledgeProvider):
    domain: str

    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        ...
```

And one shared traversal adapter:

```python
class LegacyObsidianTraversalAdapter:
    def load_notes(self, vault_root: Path) -> list[VaultNote]:
        ...
```

## Dependency Model

- `LegacyObjectiveProvider` depends on `LegacyObsidianTraversalAdapter`
- `LegacyProjectProvider` depends on `LegacyObsidianTraversalAdapter`
- `LegacyFollowUpProvider` depends on `LegacyObsidianTraversalAdapter`
- `LegacyOpenLoopProvider` depends on `LegacyObsidianTraversalAdapter`
- `LegacyDailyBriefProvider` depends on:
  - canonical entities
  - relationship graph
  - ExecutiveState-compatible aggregates

## Non-Goals

Do not wrap:

- Hermes deployment/runtime services
- Telegram orchestration
- Cloudflare
- historical generated reports as source data
- semantic infrastructure as a hard prerequisite
