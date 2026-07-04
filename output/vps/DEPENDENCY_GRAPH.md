# Hermes VPS Dependency Graph

Prepared from Alfred's current VPS evidence pack for Project Phoenix Gate 1 discovery.

```mermaid
graph TD
    vault["/docker/obsidian-vault"]
    briefings["/docker/obsidian-vault/07 Executive Briefings"]
    governance["/docker/obsidian-vault/09 Governance"]
    secondbrain["/opt/second-brain"]
    scripts["/opt/second-brain/scripts"]
    queue["/opt/second-brain/action-queue"]
    titan["/opt/second-brain/playbooks/titan_actions.json"]
    telegrampy["/root/hermes-telegram.py"]
    telegramsvc["/etc/systemd/system/hermes-telegram.service"]
    vaultoverride["/etc/systemd/system/hermes-telegram.service.d/20-authoritative-vault.conf"]
    envoverride["/etc/systemd/system/hermes-telegram.service.d/30-openrouter-env.conf"]
    envfile["/root/.openrouter.env"]
    llamaapp["/opt/llamaindex-bakeoff/app.py"]
    llamaindex["/opt/llamaindex-bakeoff/index"]
    llamaapi["tcp://127.0.0.1:8788"]
    container["docker://hermes-agent-mctr-hermes-agent-1"]
    cloudflare["/etc/cloudflared/config.yml"]
    target4865["tcp://localhost:4865"]
    target4880["tcp://127.0.0.1:4880"]

    briefings --> vault
    governance --> vault
    scripts --> secondbrain
    scripts --> vault
    queue --> secondbrain
    titan --> secondbrain
    telegrampy --> scripts
    telegrampy --> vault
    telegrampy --> envfile
    telegramsvc --> telegrampy
    telegramsvc --> envfile
    vaultoverride --> telegramsvc
    vaultoverride --> vault
    envoverride --> telegramsvc
    envoverride --> envfile
    llamaapp --> llamaindex
    llamaindex --> vault
    llamaapi --> llamaapp
    container --> secondbrain
    container --> vault
    cloudflare --> target4865
    cloudflare --> target4880
    cloudflare --> llamaapi
```

## Migration Reading

- `KEEP` flows centre on `/docker/obsidian-vault`, derived governance records, and queued action state.
- `REPLACE` flows centre on the runtime wrappers: systemd units, container runtime, and retrieval API.
- `ARCHIVE` flows preserve legacy scripts and ingress configuration as reference material during migration.
