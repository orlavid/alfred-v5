#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="$(script_log_path "deploy_rollback")"
: > "$LOG_FILE"

log_line "$LOG_FILE" "Project Phoenix Gate 3 rollback started."
log_line "$LOG_FILE" "Rollback does not delete Alfred, Hermes, Cloudflare, Telegram, or vault assets."
log_line "$LOG_FILE" "Rollback does not restore from a Hostinger snapshot automatically; snapshot recovery requires separate explicit approval."

if [[ -d "$ALFRED_INSTALL_ROOT" ]]; then
  run_or_note_dry_run "$LOG_FILE" "stop Alfred runtime markers" "$ROOT_DIR/scripts/install/stop_alfred.sh"
  if is_dry_run; then
    log_line "$LOG_FILE" "DRY-RUN: would write rollback marker under $ALFRED_INSTALL_ROOT/runtime/ROLLBACK_INFO"
  else
    mkdir -p "$ALFRED_INSTALL_ROOT/runtime"
    printf "rolled_back_at=%s\n" "$(timestamp_utc)" > "$ALFRED_INSTALL_ROOT/runtime/ROLLBACK_INFO"
    printf "scope=disable_or_remove_alfred_runtime_markers_only\n" >> "$ALFRED_INSTALL_ROOT/runtime/ROLLBACK_INFO"
    log_line "$LOG_FILE" "PASS: rollback marker written to $ALFRED_INSTALL_ROOT/runtime/ROLLBACK_INFO"
  fi
else
  log_line "$LOG_FILE" "PASS: Alfred install root not present; nothing to stop."
fi

log_line "$LOG_FILE" "PASS: Rollback completed with Alfred preserved in place."
