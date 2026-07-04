#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUTPUT_DIR="$ROOT_DIR/output/vps"
OUTPUT_FILE="$OUTPUT_DIR/ASSET_DATA.md"

mkdir -p "$OUTPUT_DIR"

cat > "$OUTPUT_FILE" <<'MARKDOWN'
# Hermes VPS Data Discovery

Prepared for Project Phoenix Gate 1 discovery.

This script is read-only. It is intended to capture knowledge and operational data assets and does not change configuration, restart services, or delete data.

## Discovery Commands

```bash
du -sh /docker/obsidian-vault
find /docker/obsidian-vault -type f | wc -l
find /docker/obsidian-vault/07\ Executive\ Briefings -type f | wc -l
find /docker/obsidian-vault/09\ Governance -type f | wc -l
du -sh /opt/second-brain/action-queue
ls -lah /opt/second-brain/playbooks
du -sh /opt/llamaindex-bakeoff/index
```

## Expected Output Sections

- Canonical markdown knowledge
- Derived executive reports
- Queue and playbook data
- Retrieval index data
- Classification for migration handling
MARKDOWN

echo "Prepared $OUTPUT_FILE"
