# Hermes VPS Asset Runtime

Prepared from Alfred's current VPS evidence pack for Project Phoenix Gate 1 discovery.

| Path | Purpose | Approximate Size | Dependencies | Disposition |
| --- | --- | --- | --- | --- |
| `/etc/systemd/system/hermes-telegram.service` | Hermes Telegram bot service entrypoint. | `4K` | `/root/hermes-telegram.py`; `docker.service`; `/root/.openrouter.env` | `REPLACE` |
| `docker://hermes-agent-mctr-hermes-agent-1` | Primary Hermes agent container currently evidenced as running. | `9.84G image / 3.04G content` | `ghcr.io/hostinger/hvps-hermes-agent:latest`; `/opt/second-brain`; `/docker/obsidian-vault` | `REPLACE` |
| `docker://hermes-agent-lp1i-hermes-agent-1` | Historical exited Hermes container retained on the host. | `9.84G image / 3.04G content` | `ghcr.io/hostinger/hvps-hermes-agent:latest` | `ARCHIVE` |
| `tcp://127.0.0.1:8788` | Legacy LlamaIndex API listener used for retrieval and evidence packaging. | `N/A` | `/opt/llamaindex-bakeoff/app.py`; `/opt/llamaindex-bakeoff/index` | `REPLACE` |
| `tcp://localhost:4865` | Alfred hostname ingress target from Cloudflare configuration. | `N/A` | `/etc/cloudflared/config.yml`; target local web service | `UNKNOWN` |
| `tcp://127.0.0.1:4880` | v2 hostname ingress target from Cloudflare configuration. | `N/A` | `/etc/cloudflared/config.yml`; target local web service | `UNKNOWN` |

## Notes

- Runtime components are not classified as `KEEP`; they should be recreated or superseded on the target Alfred package.
- The ingress targets on `4865` and `4880` are discovered endpoints, but the owning services are not fully evidenced in this repository snapshot, so they remain `UNKNOWN`.
