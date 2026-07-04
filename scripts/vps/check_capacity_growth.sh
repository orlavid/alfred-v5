#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="${1:-$(script_log_path "check_capacity_growth")}"
INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
OUTPUT_DIR="${ALFRED_OUTPUT_PATH:-$INSTALL_ROOT/app/output}"
WARN_DISK_FREE_GB="${WARN_DISK_FREE_GB:-20}"
WARN_INODE_FREE_PCT="${WARN_INODE_FREE_PCT:-15}"
WARN_LOG_SIZE_MB="${WARN_LOG_SIZE_MB:-1024}"
WARN_OUTPUT_SIZE_MB="${WARN_OUTPUT_SIZE_MB:-2048}"

: > "$LOG_FILE"

log_line "$LOG_FILE" "Capacity and growth assessment started."
log_line "$LOG_FILE" "Thresholds: disk ${WARN_DISK_FREE_GB}GB free, inode ${WARN_INODE_FREE_PCT}% free, logs ${WARN_LOG_SIZE_MB}MB, output ${WARN_OUTPUT_SIZE_MB}MB."

require_command "$LOG_FILE" df
require_command "$LOG_FILE" du
require_command "$LOG_FILE" docker
require_command "$LOG_FILE" awk

run_logged "$LOG_FILE" "capture disk free" df -h "$INSTALL_ROOT"
run_logged "$LOG_FILE" "capture inode free" df -i "$INSTALL_ROOT"
run_logged "$LOG_FILE" "capture docker usage" docker system df

if [[ -d "$INSTALL_ROOT/logs" ]]; then
  run_logged "$LOG_FILE" "capture Alfred log size" du -sh "$INSTALL_ROOT/logs"
fi

if [[ -d "$OUTPUT_DIR" ]]; then
  run_logged "$LOG_FILE" "capture Alfred output size" du -sh "$OUTPUT_DIR"
fi

run_logged "$LOG_FILE" "capture projected Alfred root size" du -sh "$INSTALL_ROOT"

log_line "$LOG_FILE" "WARN: review disk free against ${WARN_DISK_FREE_GB}GB threshold before production execution."
log_line "$LOG_FILE" "WARN: review inode free against ${WARN_INODE_FREE_PCT}% threshold before production execution."
log_line "$LOG_FILE" "WARN: review Alfred log size against ${WARN_LOG_SIZE_MB}MB threshold before production execution."
log_line "$LOG_FILE" "WARN: review Alfred output size against ${WARN_OUTPUT_SIZE_MB}MB threshold before production execution."
log_line "$LOG_FILE" "PASS: capacity and growth assessment completed."
