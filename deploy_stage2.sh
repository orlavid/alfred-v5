#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="$(script_log_path "deploy_stage2")"
: > "$LOG_FILE"

log_line "$LOG_FILE" "Project Phoenix Gate 3 Stage 2 installation started."
log_line "$LOG_FILE" "This installs Alfred into $ALFRED_INSTALL_ROOT alongside Hermes without changing Hermes-owned services."
log_line "$LOG_FILE" "Configuration is created only if missing and must include vault path, profile, output path, optional services, and model/API placeholders."

require_command "$LOG_FILE" rsync
require_command "$LOG_FILE" python3
require_command "$LOG_FILE" node
require_command "$LOG_FILE" npm

mkdir -p "$ALFRED_INSTALL_ROOT"
export ALFRED_PYTHON="${ALFRED_PYTHON:-$(command -v python3)}"
export ALFRED_NODE="${ALFRED_NODE:-$(command -v node)}"
export ALFRED_NPM="${ALFRED_NPM:-$(command -v npm)}"
export ALFRED_DEPLOYMENT_PROFILE="${ALFRED_DEPLOYMENT_PROFILE:-VPS}"
export ALFRED_INSTALL_ROOT

require_non_empty "$LOG_FILE" "ALFRED_OBSIDIAN_VAULT" "${ALFRED_OBSIDIAN_VAULT:-}"

run_or_note_dry_run "$LOG_FILE" "install Alfred platform package" "$ROOT_DIR/scripts/install/install_alfred_platform.sh"
run_or_note_dry_run "$LOG_FILE" "preserve or seed Alfred configuration" "$ROOT_DIR/scripts/install/configure_alfred.sh"

CONFIG_FILE="$ALFRED_INSTALL_ROOT/config/config.yaml"
if is_dry_run; then
  log_line "$LOG_FILE" "DRY-RUN: expected configuration path $CONFIG_FILE"
else
  require_file "$LOG_FILE" "$CONFIG_FILE"
fi

if is_dry_run; then
  log_line "$LOG_FILE" "PASS: Stage 2 dry-run completed."
  exit 0
fi

PROFILE="$(awk '/^  profile:/ {print $2; exit}' "$CONFIG_FILE")"
VAULT_PATH="$(awk '/^  vault:/ {print $2; exit}' "$CONFIG_FILE")"
OUTPUT_PATH="$(awk '/^  output:/ {print $2; exit}' "$CONFIG_FILE")"
API_KEY_ENV="$(awk '/^  key_env_var:/ {print $2; exit}' "$CONFIG_FILE")"
LLAMAINDEX_STATUS="$(awk '/llamaindex:/ {print $2; exit}' "$CONFIG_FILE")"
LLM_WIKI_STATUS="$(awk '/llm_wiki_enrichment:/ {print $2; exit}' "$CONFIG_FILE")"
DEEP_RESEARCH_STATUS="$(awk '/deep_research:/ {print $2; exit}' "$CONFIG_FILE")"

require_non_empty "$LOG_FILE" "deployment profile" "$PROFILE"
require_non_empty "$LOG_FILE" "vault path" "$VAULT_PATH"
require_non_empty "$LOG_FILE" "output path" "$OUTPUT_PATH"
require_non_empty "$LOG_FILE" "api key env placeholder" "$API_KEY_ENV"
require_non_empty "$LOG_FILE" "llamaindex status" "$LLAMAINDEX_STATUS"
require_non_empty "$LOG_FILE" "llm wiki status" "$LLM_WIKI_STATUS"
require_non_empty "$LOG_FILE" "deep research status" "$DEEP_RESEARCH_STATUS"

if grep -Eq 'api_key:|token:|secret:' "$CONFIG_FILE"; then
  fail_line "$LOG_FILE" "config file appears to contain secret material; only placeholders are allowed"
fi

log_line "$LOG_FILE" "PASS: Alfred configuration verified without printing secrets."

run_or_note_dry_run "$LOG_FILE" "prepare Alfred build artefacts" "$ROOT_DIR/scripts/install/start_alfred.sh"
run_or_note_dry_run "$LOG_FILE" "capture Alfred package status" "$ROOT_DIR/scripts/install/status_alfred.sh"

log_line "$LOG_FILE" "PASS: Stage 2 installation completed."
