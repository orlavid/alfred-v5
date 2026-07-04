# Hermes VPS Asset Data

Prepared from Alfred's current VPS evidence pack for Project Phoenix Gate 1 discovery.

| Path | Purpose | Approximate Size | Dependencies | Disposition |
| --- | --- | --- | --- | --- |
| `/docker/obsidian-vault/07 Executive Briefings` | Generated executive briefings retained inside the canonical vault. | `10M (estimated)` | `/docker/obsidian-vault`; `daily briefing jobs` | `KEEP` |
| `/docker/obsidian-vault/09 Governance` | Governance intelligence, board packs, watchlists, and decision reports. | `20M (estimated)` | `/docker/obsidian-vault`; `/opt/second-brain/scripts` | `KEEP` |
| `/opt/second-brain/action-queue` | Queued human or agent actions awaiting executor processing. | `5M (estimated)` | `/opt/second-brain`; `titan executor` | `KEEP` |
| `/opt/second-brain/playbooks/titan_actions.json` | Legacy Titan action playbook referenced by executor workflows. | `1M (estimated)` | `/opt/second-brain`; `titan executor` | `ARCHIVE` |
| `/root/hermes-telegram.py` | Legacy Telegram orchestration script capturing notes into the vault and invoking agent scripts. | `40K` | `/opt/second-brain/scripts`; `/docker/obsidian-vault`; `/root/.openrouter.env` | `ARCHIVE` |
| `/opt/llamaindex-bakeoff/app.py` | Legacy retrieval API application exposing semantic evidence search. | `16K` | `/opt/llamaindex-bakeoff/index`; `FastAPI`; `Uvicorn` | `REPLACE` |

## Notes

- Canonical markdown knowledge and queued operational state are the main `KEEP` data assets.
- Generated APIs and legacy orchestration scripts remain important for analysis but should not be treated as canonical target-state data.
