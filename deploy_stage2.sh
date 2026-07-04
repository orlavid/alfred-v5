#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="$(script_log_path "deploy_stage2")"
: > "$LOG_FILE"

log_line "$LOG_FILE" "Project Phoenix Gate 3 Stage 2 installation started."
log_line "$LOG_FILE" "This installs Alfred into $ALFRED_INSTALL_ROOT alongside Hermes without changing Hermes-owned services."

require_command "$LOG_FILE" rsync
require_command "$LOG_FILE" python3
require_command "$LOG_FILE" node
require_command "$LOG_FILE" npm

mkdir -p "$ALFRED_INSTALL_ROOT"
export ALFRED_PYTHON="${ALFRED_PYTHON:-$(command -v python3)}"
export ALFRED_NODE="${ALFRED_NODE:-$(command -v node)}"
export ALFRED_NPM="${ALFRED_NPM:-$(command -v npm)}"
export ALFRED_INSTALL_ROOT

run_logged "$LOG_FILE" "install Alfred platform package" "$ROOT_DIR/scripts/install/install_alfred_platform.sh"
run_logged "$LOG_FILE" "preserve or seed Alfred configuration" "$ROOT_DIR/scripts/install/configure_alfred.sh"
run_logged "$LOG_FILE" "prepare Alfred build artefacts" "$ROOT_DIR/scripts/install/start_alfred.sh"
run_logged "$LOG_FILE" "capture Alfred package status" "$ROOT_DIR/scripts/install/status_alfred.sh"

log_line "$LOG_FILE" "PASS: Stage 2 installation completed."
