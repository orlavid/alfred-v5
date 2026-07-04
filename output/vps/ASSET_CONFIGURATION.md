# Hermes VPS Asset Configuration

Prepared from Alfred's current VPS evidence pack for Project Phoenix Gate 1 discovery.

| Path | Purpose | Approximate Size | Dependencies | Disposition |
| --- | --- | --- | --- | --- |
| `/etc/systemd/system/hermes-telegram.service.d/20-authoritative-vault.conf` | Service override binding Hermes Telegram to the authoritative vault path. | `4K` | `/etc/systemd/system/hermes-telegram.service`; `/docker/obsidian-vault` | `REPLACE` |
| `/etc/systemd/system/hermes-telegram.service.d/30-openrouter-env.conf` | Service override binding model API environment file. | `4K` | `/etc/systemd/system/hermes-telegram.service`; `/root/.openrouter.env` | `REPLACE` |
| `/etc/cloudflared/config.yml` | Ingress routing for Alfred, v2, and API endpoints. | `4K` | `localhost:4865`; `127.0.0.1:4880`; `127.0.0.1:8788` | `ARCHIVE` |
| `/root/.openrouter.env` | Legacy model API secret environment file. | `4K` | `OpenRouter account`; `hermes-telegram.service` | `UNKNOWN` |
| `/etc/systemd/system` | Host-level service catalogue for Telegram and related runtime components. | `Directory inventory` | `systemd`; service unit files; drop-in overrides | `ARCHIVE` |

## Notes

- Configuration should be reauthored for the target deployment rather than copied without review.
- Secret-bearing files are discovered by path and role only; they should be recreated securely during deploy.
