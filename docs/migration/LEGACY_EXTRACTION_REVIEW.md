# Legacy Extraction Review

## Useful Legacy Extraction Patterns

- Prefer Obsidian folder conventions over engineering output scans.
- Resolve executive entities from markdown notes rather than generated reports.
- Treat daily logs, objectives, projects, follow-ups, and open loops as separate executive domains.
- Build entity links from wikilinks first, then enrich with path and folder hints.
- Keep recursive vault search bounded by executive folders and explicit exclusions.

## Vault Folders Used

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

## Query and Search Strategies

- Search markdown notes recursively within the live vault only.
- Classify domains from folder names, filenames, and executive language in note content.
- Build relationships from wikilinks and direct entity mentions.
- Ignore generated engineering artefacts and migration paperwork when building executive state.

## Reuse

- Obsidian-first folder mapping.
- Recursive markdown vault scan with explicit exclusions.
- Independent extraction for objectives, projects, daily logs, follow-ups, and open loops.
- Wikilink-driven relationship building.

## Discard

- Any dependency on legacy VPS services at runtime.
- Generated engineering inventory as a source of executive truth.
- Broad filesystem scans that treat repo documentation or output artefacts as executive knowledge.
- Importing or replaying old executive state.
