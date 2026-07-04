#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="$(script_log_path "deploy_stage1")"
: > "$LOG_FILE"

log_line "$LOG_FILE" "Project Phoenix Gate 3 Stage 1 precheck started."
log_line "$LOG_FILE" "This script is read-only. It does not change Hermes, Cloudflare, Telegram, or the Obsidian vault."

require_command "$LOG_FILE" df
require_command "$LOG_FILE" systemctl
require_command "$LOG_FILE" python3
require_command "$LOG_FILE" node
require_command "$LOG_FILE" npm
require_command "$LOG_FILE" docker
require_command "$LOG_FILE" ss

[[ -f "$ROOT_DIR/docs/migration/MIGRATION_MANIFEST.md" ]] || fail_line "$LOG_FILE" "missing migration manifest"
[[ -f "$ROOT_DIR/docs/deployment/VPS_DEPLOYMENT_PLAN.md" ]] || fail_line "$LOG_FILE" "missing VPS deployment plan"
[[ -d /docker/obsidian-vault ]] || fail_line "$LOG_FILE" "vault path /docker/obsidian-vault is not accessible"

if [[ ! -d "$ROOT_DIR/output/vps" ]]; then
  fail_line "$LOG_FILE" "Gate 1 discovery reports are not present under output/vps. Regenerate and review them before deployment."
fi

run_logged "$LOG_FILE" "review migration manifest" sed -n '1,220p' "$ROOT_DIR/docs/migration/MIGRATION_MANIFEST.md"
run_logged "$LOG_FILE" "review deployment plan" sed -n '1,260p' "$ROOT_DIR/docs/deployment/VPS_DEPLOYMENT_PLAN.md"
run_logged "$LOG_FILE" "capture disk availability" df -h
run_logged "$LOG_FILE" "capture Alfred root availability" df -h /opt
run_logged "$LOG_FILE" "capture docker status" docker ps -a
run_logged "$LOG_FILE" "capture docker images" docker images
run_logged "$LOG_FILE" "capture python version" python3 --version
run_logged "$LOG_FILE" "capture node version" node --version
run_logged "$LOG_FILE" "capture npm version" npm --version
run_logged "$LOG_FILE" "capture current services" systemctl list-units --type=service --all
run_logged "$LOG_FILE" "capture Telegram service status" systemctl status hermes-telegram.service --no-pager
run_logged "$LOG_FILE" "capture listeners" ss -ltnp
run_logged "$LOG_FILE" "capture vault size" du -sh /docker/obsidian-vault
run_logged "$LOG_FILE" "capture vault recent files" find /docker/obsidian-vault -maxdepth 2 -type f | head -100

log_line "$LOG_FILE" "PASS: Stage 1 prechecks completed."
