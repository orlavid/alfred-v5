#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="$(script_log_path "deploy_vps")"
: > "$LOG_FILE"

ROLLBACK_TRIGGERED=0
REMOTE_RELEASE_READY=0

shell_quote() {
  printf "'%s'" "$(printf "%s" "$1" | sed "s/'/'\\\\''/g")"
}

VENV_DIR="$ROOT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
PACKAGE_DIR="${ALFRED_DEPLOY_PACKAGE_DIR:-$ROOT_DIR/.deploy}"
PACKAGE_PATH="$PACKAGE_DIR/alfred-handbook-deploy.tgz"
REMOTE_USER="${ALFRED_REMOTE_USER:-root}"
REMOTE_HOST="${ALFRED_REMOTE_HOST:?ALFRED_REMOTE_HOST is required}"
REMOTE_TARGET="$REMOTE_USER@$REMOTE_HOST"
REMOTE_STAGE_ROOT="${ALFRED_REMOTE_STAGE_ROOT:-/tmp/alfred-deploy}"
REMOTE_INSTALL_ROOT="${ALFRED_REMOTE_INSTALL_ROOT:-/opt/alfred}"
REMOTE_RELEASE_DIR="${ALFRED_REMOTE_RELEASE_DIR:-$REMOTE_STAGE_ROOT/release}"
REMOTE_BUNDLE_PATH="$REMOTE_STAGE_ROOT/alfred-handbook-deploy.tgz"

rollback_on_failure() {
  local exit_code=$?
  if [[ $exit_code -eq 0 ]]; then
    return 0
  fi
  if [[ $ROLLBACK_TRIGGERED -eq 1 ]]; then
    exit "$exit_code"
  fi
  ROLLBACK_TRIGGERED=1
  log_line "$LOG_FILE" "FAIL: deployment gate failed with exit code $exit_code; starting automatic VPS rollback."
  if [[ $REMOTE_RELEASE_READY -eq 1 ]]; then
    remote_run "rollback Alfred on VPS" bash -lc "cd '$REMOTE_RELEASE_DIR' && if [[ -f deploy_rollback.sh ]]; then ALFRED_INSTALL_ROOT='$REMOTE_INSTALL_ROOT' ./deploy_rollback.sh; else echo 'INFO: deploy_rollback.sh not present; skipping rollback helper.'; fi" \
      || log_line "$LOG_FILE" "FAIL: automatic VPS rollback also failed."
  else
    log_line "$LOG_FILE" "INFO: remote release not prepared; skipping VPS rollback."
  fi
  exit "$exit_code"
}

trap rollback_on_failure EXIT

run_gate() {
  local label="$1"
  shift
  run_logged "$LOG_FILE" "$label" "$@"
}

remote_run() {
  local label="$1"
  shift
  run_logged "$LOG_FILE" "$label" ssh -o BatchMode=yes "$REMOTE_TARGET" "$@"
}

remote_copy() {
  local label="$1"
  local source_path="$2"
  local target_path="$3"
  run_logged "$LOG_FILE" "$label" scp "$source_path" "$REMOTE_TARGET:$target_path"
}

ensure_python_environment() {
  if [[ ! -x "$VENV_PYTHON" ]]; then
    run_logged "$LOG_FILE" "create virtual environment" python3 -m venv "$VENV_DIR"
  else
    log_line "$LOG_FILE" "PASS: virtual environment already present at $VENV_DIR"
  fi

  run_logged "$LOG_FILE" "upgrade pip in virtual environment" "$VENV_PYTHON" -m pip install --upgrade pip

  if ! "$VENV_PYTHON" -m pytest --version >>"$LOG_FILE" 2>&1; then
    run_logged "$LOG_FILE" "install Python test dependency" "$VENV_PYTHON" -m pip install pytest
  else
    log_line "$LOG_FILE" "PASS: pytest already available in virtual environment"
  fi

  if [[ -f "$ROOT_DIR/package.json" && ! -d "$ROOT_DIR/node_modules" ]]; then
    run_logged "$LOG_FILE" "install Node dependencies" npm install
  elif [[ -f "$ROOT_DIR/package.json" ]]; then
    log_line "$LOG_FILE" "PASS: node_modules already present"
  fi
}

build_release_bundle() {
  mkdir -p "$PACKAGE_DIR"
  rm -f "$PACKAGE_PATH"
  run_logged "$LOG_FILE" "package deployment bundle" \
    env COPYFILE_DISABLE=1 tar --no-xattrs --exclude='.git' --exclude='.venv' --exclude='node_modules' --exclude='dist' --exclude='output' --exclude='deployment_logs' --exclude='.deploy' \
      -czf "$PACKAGE_PATH" -C "$ROOT_DIR" .
}

prepare_remote_release() {
  remote_run "prepare VPS staging directories" mkdir -p "$REMOTE_STAGE_ROOT"
  remote_copy "upload deployment bundle" "$PACKAGE_PATH" "$REMOTE_BUNDLE_PATH"
  remote_run "extract deployment bundle on VPS" bash -lc "rm -rf $(shell_quote "$REMOTE_RELEASE_DIR") && mkdir -p $(shell_quote "$REMOTE_RELEASE_DIR") && tar -xzf $(shell_quote "$REMOTE_BUNDLE_PATH") -C $(shell_quote "$REMOTE_RELEASE_DIR")"
  REMOTE_RELEASE_READY=1
}

run_remote_install() {
  remote_run "install Alfred on VPS" bash -lc "cd $(shell_quote "$REMOTE_RELEASE_DIR") && ALFRED_INSTALL_ROOT=$(shell_quote "$REMOTE_INSTALL_ROOT") ALFRED_OBSIDIAN_VAULT=$(shell_quote "$ALFRED_OBSIDIAN_VAULT") ./deploy_stage2.sh"
}

run_remote_acceptance() {
  remote_run "run Executive Acceptance on VPS" bash -lc "cd $(shell_quote "$REMOTE_RELEASE_DIR") && ALFRED_INSTALL_ROOT=$(shell_quote "$REMOTE_INSTALL_ROOT") ./deploy_validation.sh"
}

run_remote_start() {
  remote_run "start service on VPS" bash -lc "cd $(shell_quote "$REMOTE_RELEASE_DIR") && ALFRED_INSTALL_ROOT=$(shell_quote "$REMOTE_INSTALL_ROOT") ./scripts/install/start_alfred.sh"
}

run_remote_smoke_test() {
  remote_run "smoke test on VPS" bash -lc "cd $(shell_quote "$REMOTE_RELEASE_DIR") && ALFRED_INSTALL_ROOT=$(shell_quote "$REMOTE_INSTALL_ROOT") ./scripts/install/status_alfred.sh"
}

log_line "$LOG_FILE" "Project Phoenix live knowledge cutover deployment started."
log_line "$LOG_FILE" "Local validation runs on the development machine; Alfred installation and smoke verification run on the VPS."

require_command "$LOG_FILE" git
require_command "$LOG_FILE" python3
require_command "$LOG_FILE" npm
require_command "$LOG_FILE" tar
require_command "$LOG_FILE" ssh
require_command "$LOG_FILE" scp

run_gate "pull GitHub" git pull --ff-only
ensure_python_environment
run_gate "build" "$VENV_PYTHON" "$ROOT_DIR/build_everything.py"
run_gate "run tests" "$VENV_PYTHON" -m pytest
run_gate "run Live Knowledge Certification" "$VENV_PYTHON" "$ROOT_DIR/build_live_knowledge_certification.py"
build_release_bundle
prepare_remote_release
run_remote_install
run_remote_acceptance
run_remote_start
run_remote_smoke_test

trap - EXIT
log_line "$LOG_FILE" "PASS: live knowledge cutover deployment completed."
