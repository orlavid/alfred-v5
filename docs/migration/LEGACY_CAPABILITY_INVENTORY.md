# Legacy Capability Inventory

## Scope

This document captures the proven executive-knowledge acquisition patterns observed from Alfred/Hermes archaeology artefacts and the surviving extraction logic already mirrored into Alfred v5.

It is intentionally read-only:

- no VPS code is modified
- no legacy runtime dependency is introduced
- no legacy executive state is imported

Confidence levels below reflect how directly each behaviour is evidenced in local archaeology material:

- `HIGH`: directly visible in current extracted code paths or explicit review artefacts
- `MEDIUM`: strongly implied by review artefacts and surviving interfaces
- `LOW`: inferred from adjacent behaviour only

## Evidence Base

- [scripts/vps/review_legacy_extraction.sh](/Users/dohenyp/Projects/alfred-handbook/scripts/vps/review_legacy_extraction.sh)
- [docs/migration/LEGACY_EXTRACTION_REVIEW.md](/Users/dohenyp/Projects/alfred-handbook/docs/migration/LEGACY_EXTRACTION_REVIEW.md)
- [executive/knowledge/vault.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/vault.py)
- [executive/knowledge/extractor.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/extractor.py)
- [src/knowledge/providers](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers)
- [scripts/vps/build_dependency_graph.py](/Users/dohenyp/Projects/alfred-handbook/scripts/vps/build_dependency_graph.py)

## Capability Inventory

| Capability | Observed Legacy Behaviour | Reusable Logic | Do Not Reuse | Confidence |
| --- | --- | --- | --- | --- |
| Vault traversal | Recursive markdown scan of the Obsidian vault only, not the whole filesystem. | Vault-root-bounded `rglob("*.md")` scan and path-relative note identities. | Broad repo scans or generated output as executive truth. | HIGH |
| Recursive search | Search strategy starts from the authoritative vault root and descends through executive folders. | Single entry vault loader with explicit exclusions. | Any traversal that follows build artefacts, logs, or migration docs. | HIGH |
| Folder classification | Executive domains inferred first from Obsidian folder conventions, then from note title/content hints. | Folder map for Daily Logs, Projects, Companies, Decisions, Meetings, Risks, Open Loops, Follow Ups, Objectives, Briefings. | Engineering/inventory folders as domain classifiers. | HIGH |
| Objective extraction | Objectives treated as an independent executive domain, not a generic note subtype. | Dedicated provider that selects only objective-classified notes. | Synthetic objectives or fallback objectives. | HIGH |
| Project extraction | Projects sourced from project-classified notes and linked later via wikilinks/resolution. | Dedicated project provider over classified notes. | Project creation from reports or dashboard summaries. | HIGH |
| Follow-up extraction | Follow-ups isolated from general tasks and inferred from explicit folder/text cues. | Dedicated follow-up provider over follow-up notes. | Generating follow-ups from reasoning output. | HIGH |
| Open-loop extraction | Open loops extracted as a distinct unresolved-governance domain. | Dedicated open-loop provider over open-loop notes. | Conflating open loops with generic risks or actions. | HIGH |
| Daily brief generation | Executive briefing layer summarises already-extracted vault intelligence rather than rescanning raw files itself. | Briefing built over analysed vault output. | Hard-coded meeting subjects or synthetic agenda content. | MEDIUM |
| Executive briefing generation | Briefings persisted back into executive briefing folders in the vault. | Separate executive briefing domain and report-generation layer over analysed knowledge. | Treating generated briefings as source evidence for new entities. | MEDIUM |
| Entity resolution | Wikilinks appear to be the first-class relationship primitive; path/folder hints enrich afterwards. | Link extraction before canonical resolution, then graph construction. | Name-only fuzzy generation without note evidence. | HIGH |
| Semantic search integration | Semantic layer existed beside the vault and was treated as an enrichment/index, not the source of record. | Semantic search as optional downstream dependency over canonical vault content. | Making semantic index mandatory for baseline extraction. | MEDIUM |
| Exclusion rules | Legacy approach avoided engineering artefacts and generated inventory when building executive state. | Explicit path exclusions such as `output/`, `docs/migration/`, `.git/`, `.obsidian/`, `node_modules/`. | Any fallback that re-ingests Alfred-generated reports as executive evidence. | HIGH |
| Obsidian-specific heuristics | Folder naming, note naming, executive language, and wikilinks combine to classify notes. | Obsidian-first heuristics layered in this order: folder, filename, content, wikilinks. | Repo-centric heuristics based on code/docs locations. | HIGH |

## Canonical Legacy Folder Model

The surviving evidence points to this executive vault taxonomy:

- `01 Daily Logs/`
- `02 People/`
- `03 Projects/`
- `04 Companies/`
- `04 Decisions/`
- `05 Meetings/`
- `06 Risks/`
- `07 Open Loops/`
- `08 Follow Ups/`
- `09 Objectives/`
- `10 Briefings/`

These folders are not a UI choice. They are the legacy extraction contract.

## Reuse Decision

Reuse these behaviours:

- authoritative live vault root
- recursive markdown-only traversal
- explicit exclusion rules
- folder-first executive classification
- dedicated per-domain extraction
- wikilink-first relationship acquisition

Discard these behaviours:

- runtime dependence on Hermes services
- scanning Alfred output artefacts as evidence
- synthetic executive content
- legacy deployment/runtime coupling
