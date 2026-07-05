#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="$(script_log_path "deploy_vps")"
: > "$LOG_FILE"

ROLLBACK_TRIGGERED=0

rollback_on_failure() {
  local exit_code=$?
  if [[ $exit_code -eq 0 ]]; then
    return 0
  fi
  if [[ $ROLLBACK_TRIGGERED -eq 1 ]]; then
    exit "$exit_code"
  fi
  ROLLBACK_TRIGGERED=1
  log_line "$LOG_FILE" "FAIL: deployment gate failed with exit code $exit_code; starting automatic rollback."
  "$ROOT_DIR/deploy_rollback.sh" >>"$LOG_FILE" 2>&1 || log_line "$LOG_FILE" "FAIL: automatic rollback also failed."
  exit "$exit_code"
}

trap rollback_on_failure EXIT

run_gate() {
  local label="$1"
  shift
  run_logged "$LOG_FILE" "$label" "$@"
}

log_line "$LOG_FILE" "Project Phoenix live knowledge cutover deployment started."

require_command "$LOG_FILE" git
require_command "$LOG_FILE" python3
require_command "$LOG_FILE" pytest
require_command "$LOG_FILE" npm

run_gate "pull GitHub" git pull --ff-only
run_gate "install" "$ROOT_DIR/deploy_stage2.sh"
run_gate "build" python3 "$ROOT_DIR/build_everything.py"
run_gate "run tests" pytest
run_gate "run Live Knowledge Certification" python3 "$ROOT_DIR/build_live_knowledge_certification.py"
run_gate "run Executive Acceptance" "$ROOT_DIR/deploy_validation.sh"
run_gate "start service" "$ROOT_DIR/scripts/install/start_alfred.sh"
run_gate "smoke test" "$ROOT_DIR/scripts/install/status_alfred.sh"

trap - EXIT
log_line "$LOG_FILE" "PASS: live knowledge cutover deployment completed."
