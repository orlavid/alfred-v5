# Legacy Call Graph

## Purpose

This call graph traces the legacy executive-knowledge acquisition behaviour into concrete code surfaces that Alfred v5 can wrap.

The emphasis is observable behaviour, not historical completeness.

## Capability Graph

| Capability | Entry Point | Files | Functions / Classes | Dependencies | Outputs | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| Vault traversal | Provider extraction start | [executive/knowledge/extractor.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/extractor.py), [src/knowledge/providers/__init__.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/__init__.py), [executive/knowledge/vault.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/vault.py) | `extract_entities()`, `extract_provider_entities()`, `load_vault()` | live vault root, exclusions, markdown filesystem | `VaultNote[]` then `VaultEntity[]` | HIGH |
| Recursive search | Vault loader | [executive/knowledge/vault.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/vault.py) | `load_vault()` | `Path.rglob("*.md")`, `_is_excluded_path()` | relative-path notes | HIGH |
| Folder classification | Vault loader classification | [executive/knowledge/vault.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/vault.py) | `classify()` | folder map, filename/content heuristics | note `kind` | HIGH |
| Objective extraction | Objective provider | [src/knowledge/providers/objective_provider.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/objective_provider.py), [src/knowledge/providers/base.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/base.py) | `ObjectiveProvider.extract_matches()`, `ExecutiveKnowledgeProvider.extract_entities()` | classified notes | objective entities | HIGH |
| Project extraction | Project provider | [src/knowledge/providers/project_provider.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/project_provider.py), [src/knowledge/providers/base.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/base.py) | `ProjectProvider.extract_matches()` | classified notes | project entities | HIGH |
| Follow-up extraction | Follow-up provider | [src/knowledge/providers/followup_provider.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/followup_provider.py), [src/knowledge/providers/base.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/base.py) | `FollowupProvider.extract_matches()` | classified notes | follow-up entities | HIGH |
| Open-loop extraction | Open-loop provider | [src/knowledge/providers/open_loop_provider.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/open_loop_provider.py), [src/knowledge/providers/base.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/base.py) | `OpenLoopProvider.extract_matches()` | classified notes | open-loop entities | HIGH |
| Daily-log extraction | Daily-log provider | [src/knowledge/providers/daily_log_provider.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/daily_log_provider.py), [src/knowledge/providers/base.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/base.py) | `DailyLogProvider.extract_matches()` | classified notes | daily-log entities | HIGH |
| Generic executive extraction | Generic Obsidian provider | [src/knowledge/providers/obsidian_provider.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/obsidian_provider.py) | `ObsidianProvider.extract_matches()` | classified notes | companies, people, decisions, meetings, risks, policies, briefings | HIGH |
| Link acquisition | Entity extractor | [executive/knowledge/extractor.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/extractor.py), [src/knowledge/providers/base.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/base.py) | `extract_links()`, `_extract_links()` | wikilinks in markdown | link arrays on entities | HIGH |
| Tag acquisition | Entity extractor | [executive/knowledge/extractor.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/extractor.py), [src/knowledge/providers/base.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/base.py) | `extract_tags()`, `_extract_tags()` | markdown tags | tag arrays on entities | HIGH |
| Entity resolution | Knowledge builder graph phase | [src/knowledge/executive_knowledge_builder.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/executive_knowledge_builder.py), [executive/knowledge/resolver.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/resolver.py) | `build_entity_resolution()`, `build_resolution_index()`, `resolve_link_with_index()` | provider entities, aliases, links | canonical entities, alias index | HIGH |
| Knowledge graph | Knowledge builder graph phase | [src/knowledge/executive_knowledge_builder.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/executive_knowledge_builder.py), [executive/knowledge/graph.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/graph.py) | `build_graph()`, `_build_relationships()` | canonical entities, links | edges / neighbours | HIGH |
| Daily brief generation | Briefing/report layer | [src/daily/daily_brief.py](/Users/dohenyp/Projects/alfred-handbook/src/daily/daily_brief.py), [src/executive/executive_state.py](/Users/dohenyp/Projects/alfred-handbook/src/executive/executive_state.py) | `build_daily_brief()`, `build_executive_state()` | analysed executive state | daily brief report | MEDIUM |
| Executive briefing generation | Executive briefing/report layer | [executive/knowledge/executive_briefing.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/executive_briefing.py), [src/executive/executive_intelligence.py](/Users/dohenyp/Projects/alfred-handbook/src/executive/executive_intelligence.py) | `build_briefing()`, `build_executive_intelligence()` | analysed objective/project/finding state | briefing headlines and detail | MEDIUM |
| Semantic search integration | Optional semantic estate | [scripts/vps/build_dependency_graph.py](/Users/dohenyp/Projects/alfred-handbook/scripts/vps/build_dependency_graph.py), [scripts/vps/review_legacy_extraction.sh](/Users/dohenyp/Projects/alfred-handbook/scripts/vps/review_legacy_extraction.sh) | asset review only in this repo | semantic index path, bakeoff app, vault mount | enrichment/search capability beside vault | MEDIUM |
| Exclusion rules | Vault loader | [executive/knowledge/vault.py](/Users/dohenyp/Projects/alfred-handbook/executive/knowledge/vault.py), [src/knowledge/providers/obsidian_provider.py](/Users/dohenyp/Projects/alfred-handbook/src/knowledge/providers/obsidian_provider.py) | `_is_excluded_path()` | excluded segments/prefixes | contamination-free note set | HIGH |
| Legacy review and discovery | Read-only archaeology | [scripts/vps/review_legacy_extraction.sh](/Users/dohenyp/Projects/alfred-handbook/scripts/vps/review_legacy_extraction.sh), [docs/migration/LEGACY_EXTRACTION_REVIEW.md](/Users/dohenyp/Projects/alfred-handbook/docs/migration/LEGACY_EXTRACTION_REVIEW.md) | shell review patterns only | VPS filesystem, ripgrep | operator report, not runtime data | HIGH |

## Minimal Execution Flow

1. Resolve authoritative vault root.
2. Recursively load markdown notes with exclusions.
3. Classify each note into an executive domain.
4. Run dedicated providers by domain.
5. Extract links and tags from note bodies.
6. Canonicalise entities and aliases.
7. Build the relationship graph.
8. Feed downstream consumers:
   - ExecutiveState
   - Daily Brief
   - Executive Intelligence
   - Executive Reasoning
   - Dashboard API

## Legacy Wrapping Boundary

The stable wrapping seam is here:

- input: `vault_root -> VaultNote[]`
- domain split: `VaultNote[] -> ProviderMatch[]`
- entity output: `ProviderMatch[] -> VaultEntity[]`

That is the correct point to preserve legacy behaviour while replacing internals one capability at a time.
