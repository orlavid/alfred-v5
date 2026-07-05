#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="$ROOT_DIR/output/vps"
OUTPUT_FILE="$OUTPUT_DIR/ASSET_CONFIGURATION.md"

mkdir -p "$OUTPUT_DIR"

cat > "$OUTPUT_FILE" <<'MARKDOWN'
# Hermes VPS Configuration Discovery

Prepared for Project Phoenix Gate 1 discovery.

This script is read-only. It is intended to capture configuration assets and does not change configuration, restart services, or delete data.

## Discovery Commands

```bash
systemctl cat hermes-telegram.service
ls -lah /etc/systemd/system/hermes-telegram.service*
stat /etc/cloudflared/config.yml
sed -n '1,200p' /etc/cloudflared/config.yml
stat /root/.openrouter.env
crontab -l
find /etc/systemd/system -maxdepth 2 -type f | sort
```

## Safety Notes

- Secret-bearing files should be inventoried by path, owner, mode, and size only unless explicit secret review is approved later.
- Drop-in overrides should be captured separately from service units.
- Cloud ingress and local port mappings should be documented but not changed.
MARKDOWN

echo "Prepared $OUTPUT_FILE"
