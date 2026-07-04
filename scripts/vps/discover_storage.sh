#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="$ROOT_DIR/output/vps"
OUTPUT_FILE="$OUTPUT_DIR/ASSET_STORAGE.md"

mkdir -p "$OUTPUT_DIR"

cat > "$OUTPUT_FILE" <<'MARKDOWN'
# Hermes VPS Storage Discovery

Prepared for Project Phoenix Gate 1 discovery.

This script is read-only. It is intended to capture storage assets and does not change configuration, restart services, or delete data.

## Discovery Commands

```bash
df -h
du -sh /docker/obsidian-vault
du -sh /opt/llamaindex-bakeoff/index
du -sh /opt/second-brain
du -sh /opt/hermes-trading
find /docker/obsidian-vault -maxdepth 2 -type d | sort
find /opt -maxdepth 3 -type d | sort
```

## Expected Output Sections

- Canonical vault storage
- Retrieval index storage
- Legacy runtime storage
- Archive candidate storage
- Asset classification for KEEP / REPLACE / ARCHIVE / DELETE / UNKNOWN
MARKDOWN

echo "Prepared $OUTPUT_FILE"
