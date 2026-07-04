#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="${1:-$(script_log_path "verify_sacred_assets")}"
VAULT_PATH="${ALFRED_OBSIDIAN_VAULT:-/docker/obsidian-vault}"
CLOUDFLARE_CONFIG="${ALFRED_CLOUDFLARE_CONFIG:-/etc/cloudflared/config.yml}"
TELEGRAM_SERVICE="${ALFRED_TELEGRAM_SERVICE:-hermes-telegram.service}"
LLAMAINDEX_CONFIG="${ALFRED_LLAMAINDEX_CONFIG:-/opt/alfred/config/llamaindex.yaml}"
ENRICHMENT_CONFIG="${ALFRED_ENRICHMENT_CONFIG:-/opt/alfred/config/enrichment.yaml}"
RECOVERY_BUNDLE="${ALFRED_RECOVERY_BUNDLE:-/root/hermes-backup-retention.sh}"

: > "$LOG_FILE"

log_line "$LOG_FILE" "Sacred asset verification started."
log_line "$LOG_FILE" "This script is read-only and verifies assets without modifying Hermes, Cloudflare, Telegram, or the vault."
log_line "$LOG_FILE" "Do not change Cloudflare. Verify presence only."

require_command "$LOG_FILE" systemctl
require_command "$LOG_FILE" test

require_file "$LOG_FILE" "$CLOUDFLARE_CONFIG"
run_logged "$LOG_FILE" "verify Telegram service presence" systemctl status "$TELEGRAM_SERVICE" --no-pager
require_directory "$LOG_FILE" "$VAULT_PATH"
run_logged "$LOG_FILE" "verify vault readability" bash -lc "find \"$VAULT_PATH\" -maxdepth 2 -type f | head -50"

if [[ -f "$LLAMAINDEX_CONFIG" ]]; then
  log_line "$LOG_FILE" "PASS: optional LlamaIndex config detected at $LLAMAINDEX_CONFIG"
else
  log_line "$LOG_FILE" "WARN: optional LlamaIndex config not detected at $LLAMAINDEX_CONFIG"
fi

if [[ -f "$ENRICHMENT_CONFIG" ]]; then
  log_line "$LOG_FILE" "PASS: optional enrichment config detected at $ENRICHMENT_CONFIG"
else
  log_line "$LOG_FILE" "WARN: optional enrichment config not detected at $ENRICHMENT_CONFIG"
fi

require_file "$LOG_FILE" "$RECOVERY_BUNDLE"

if [[ "${HOSTINGER_SNAPSHOT_CONFIRMED:-no}" != "yes" ]]; then
  fail_line "$LOG_FILE" "Hostinger snapshot confirmation missing. Set HOSTINGER_SNAPSHOT_CONFIRMED=yes after manual confirmation."
fi

log_line "$LOG_FILE" "PASS: sacred asset verification completed."
