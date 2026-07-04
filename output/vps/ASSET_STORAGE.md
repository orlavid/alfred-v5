# Hermes VPS Asset Storage

Prepared from Alfred's current VPS evidence pack for Project Phoenix Gate 1 discovery.

| Path | Purpose | Approximate Size | Dependencies | Disposition |
| --- | --- | --- | --- | --- |
| `/docker/obsidian-vault` | Canonical Obsidian knowledge vault and source of truth. | `55M` | `docker mount`; `Obsidian sync`; `Hermes capture path` | `KEEP` |
| `/opt/llamaindex-bakeoff/index` | Persisted semantic retrieval index used by the legacy LlamaIndex API. | `170M` | `/docker/obsidian-vault`; `/opt/llamaindex-bakeoff/app.py`; `Python environment` | `REPLACE` |
| `/opt/second-brain` | Legacy Hermes runtime root containing scripts, playbooks, and operational state. | `250M (estimated)` | `systemd services`; `docker runtime`; `Python scripts` | `REPLACE` |
| `/opt/second-brain/scripts` | Legacy deterministic automation and enrichment script collection. | `25M (estimated)` | `/opt/second-brain`; `Python environment`; `/docker/obsidian-vault` | `ARCHIVE` |
| `/opt/hermes-trading` | Legacy trading adjunct repository referenced from Telegram workflows. | `50M (estimated)` | `Python environment`; `Telegram invocation` | `ARCHIVE` |

## Notes

- `/docker/obsidian-vault` is the primary `KEEP` asset because it is the canonical knowledge store.
- Retrieval and runtime storage assets are marked `REPLACE` or `ARCHIVE` because Alfred v5 should rebuild them from the source vault and codebase rather than copy them blindly.
