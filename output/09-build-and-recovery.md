# Build and Recovery Guide

Generated: 2026-06-30T21:41:58.616631


## Restore Order

1. Provision the VPS operating system.
2. Install Python, Docker, systemd-compatible services and cloudflared.
3. Restore `/opt/second-brain`.
4. Restore `/opt/llamaindex-bakeoff`.
5. Restore `/opt/alfred-v2`.
6. Restore `/docker/obsidian-vault`.
7. Restore `/etc/cloudflared`.
8. Restore systemd service files and overrides.
9. Restore environment files without exposing secrets.
10. Start Cloudflare.
11. Start LlamaIndex API.
12. Start Telegram.
13. Validate ChatGPT Action.
14. Validate Telegram.
15. Validate Obsidian vault freshness.

## Validation Tests

```bash
curl -I https://v2.alfreddoheny.cloud
curl -s http://127.0.0.1:8788/docs | head
/opt/second-brain/scripts/alfred_router.sh "tell me about the barclays meeting tomorrow"
systemctl status hermes-telegram.service --no-pager -l
```

## Expected Functional Questions

- Prepare me for tomorrow's Barclays meeting.
- Tell me about the Barclays meeting tomorrow.
- Who is Graham Dawe?
- Find the test sync note containing 641923.

## Recovery Rule

During recovery, do not redesign. Restore the smallest broken component that returns the system to intended behaviour.
