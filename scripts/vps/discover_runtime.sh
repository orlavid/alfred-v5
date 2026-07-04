#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="$ROOT_DIR/output/vps"
OUTPUT_FILE="$OUTPUT_DIR/ASSET_RUNTIME.md"

mkdir -p "$OUTPUT_DIR"

cat > "$OUTPUT_FILE" <<'MARKDOWN'
# Hermes VPS Runtime Discovery

Prepared for Project Phoenix Gate 1 discovery.

This script is read-only. It is intended to capture runtime assets and does not change configuration, restart services, or delete data.

## Discovery Commands

```bash
systemctl list-units --type=service --all
systemctl list-timers --all
systemctl cat hermes-telegram.service
systemctl status hermes-telegram.service --no-pager
docker ps -a
docker images
ss -ltnp
ps -ef
```

## Expected Output Sections

- Systemd service inventory
- Timer inventory
- Docker runtime inventory
- Listener and port inventory
- Runtime dependency classification
MARKDOWN

echo "Prepared $OUTPUT_FILE"
