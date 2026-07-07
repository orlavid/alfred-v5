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
BUILD_COMMIT="$(git -C "$ROOT_DIR" rev-parse HEAD)"
BUILD_TREE_STATE="$([ -z "$(git -C "$ROOT_DIR" status --short)" ] && echo clean || echo dirty)"
REMOTE_USER="${ALFRED_REMOTE_USER:-root}"
REMOTE_HOST="${ALFRED_REMOTE_HOST:-}"
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
    remote_run "rollback Alfred on VPS" "bash -lc $(shell_quote "cd $(shell_quote "$REMOTE_RELEASE_DIR") && if [[ -f deploy_rollback.sh ]]; then ALFRED_INSTALL_ROOT=$(shell_quote "$REMOTE_INSTALL_ROOT") ./deploy_rollback.sh; else echo 'INFO: deploy_rollback.sh not present; skipping rollback helper.'; fi")" \
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

verify_git_deploy_state() {
  local branch_name
  local upstream_ref
  local worktree_state

  git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
    || fail_line "$LOG_FILE" "deployment must run from a Git working tree."

  branch_name="$(git -C "$ROOT_DIR" symbolic-ref --short -q HEAD || true)"
  [[ -n "$branch_name" ]] \
    || fail_line "$LOG_FILE" "unsupported Git state: detached HEAD. Check out a deployment branch (for example: git checkout main) before running deploy_vps.sh."

  worktree_state="$(git -C "$ROOT_DIR" status --short)"
  [[ -z "$worktree_state" ]] \
    || fail_line "$LOG_FILE" "unsupported Git state: working tree is dirty. Commit or stash local changes before running deploy_vps.sh."

  upstream_ref="$(git -C "$ROOT_DIR" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
  [[ -n "$upstream_ref" ]] \
    || fail_line "$LOG_FILE" "unsupported Git state: branch '$branch_name' has no upstream. Set one with: git branch --set-upstream-to=origin/$branch_name $branch_name"

  log_line "$LOG_FILE" "PASS: Git deployment state is supported on branch $branch_name tracking $upstream_ref"
}

verify_remote_deploy_config() {
  [[ -n "$REMOTE_HOST" ]] \
    || fail_line "$LOG_FILE" "missing required deployment target: ALFRED_REMOTE_HOST"
  log_line "$LOG_FILE" "PASS: remote deployment target is configured for $REMOTE_TARGET"
}

remote_run() {
  local label="$1"
  local remote_command="$2"
  run_logged "$LOG_FILE" "$label" ssh -o BatchMode=yes "$REMOTE_TARGET" "$remote_command"
}

remote_run_script() {
  local label="$1"
  local remote_script="$2"
  local script_file
  script_file="$(mktemp "${TMPDIR:-/tmp}/alfred-remote.XXXXXX")"
  printf '%s\n' "$remote_script" > "$script_file"
  log_line "$LOG_FILE" "RUN: $label"
  ssh -o BatchMode=yes "$REMOTE_TARGET" bash -se <"$script_file" >>"$LOG_FILE" 2>&1 || {
    rm -f "$script_file"
    fail_line "$LOG_FILE" "$label"
  }
  rm -f "$script_file"
  log_line "$LOG_FILE" "PASS: $label"
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
  run_logged "$LOG_FILE" "install canonical Python dependencies" "$VENV_PYTHON" -m pip install -r "$ROOT_DIR/requirements-dev.txt"

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
  remote_run "prepare VPS staging directories" "mkdir -p $(shell_quote "$REMOTE_STAGE_ROOT")"
  remote_copy "upload deployment bundle" "$PACKAGE_PATH" "$REMOTE_BUNDLE_PATH"
  remote_run_script "extract deployment bundle on VPS" "$(cat <<EOF
set -euo pipefail
rm -rf $(shell_quote "$REMOTE_RELEASE_DIR")
mkdir -p $(shell_quote "$REMOTE_RELEASE_DIR")
tar -xzf $(shell_quote "$REMOTE_BUNDLE_PATH") -C $(shell_quote "$REMOTE_RELEASE_DIR")
EOF
)"
  REMOTE_RELEASE_READY=1
}

run_remote_install() {
  remote_run "install Alfred on VPS" "bash -lc $(shell_quote "cd $(shell_quote "$REMOTE_RELEASE_DIR") && ALFRED_INSTALL_ROOT=$(shell_quote "$REMOTE_INSTALL_ROOT") ALFRED_OBSIDIAN_VAULT=$(shell_quote "$ALFRED_OBSIDIAN_VAULT") ALFRED_BUILD_COMMIT=$(shell_quote "$BUILD_COMMIT") ALFRED_BUILD_TREE_STATE=$(shell_quote "$BUILD_TREE_STATE") ./deploy_stage2.sh")"
}

run_remote_acceptance() {
  remote_run "run Executive Acceptance on VPS" "bash -lc $(shell_quote "cd $(shell_quote "$REMOTE_RELEASE_DIR") && ALFRED_INSTALL_ROOT=$(shell_quote "$REMOTE_INSTALL_ROOT") ./deploy_validation.sh")"
}

run_remote_start() {
  remote_run "start service on VPS" "bash -lc $(shell_quote "cd $(shell_quote "$REMOTE_RELEASE_DIR") && ALFRED_INSTALL_ROOT=$(shell_quote "$REMOTE_INSTALL_ROOT") ./scripts/install/start_alfred.sh")"
}

run_remote_smoke_test() {
  remote_run "smoke test on VPS" "bash -lc $(shell_quote "cd $(shell_quote "$REMOTE_RELEASE_DIR") && ALFRED_INSTALL_ROOT=$(shell_quote "$REMOTE_INSTALL_ROOT") ./scripts/install/status_alfred.sh")"
}

log_line "$LOG_FILE" "Project Phoenix live knowledge cutover deployment started."
log_line "$LOG_FILE" "Local validation runs on the development machine; Alfred installation and smoke verification run on the VPS."

require_command "$LOG_FILE" git
require_command "$LOG_FILE" python3
require_command "$LOG_FILE" npm
require_command "$LOG_FILE" tar
require_command "$LOG_FILE" ssh
require_command "$LOG_FILE" scp

verify_git_deploy_state
run_gate "pull GitHub" git pull --ff-only
ensure_python_environment
run_gate "build" "$VENV_PYTHON" "$ROOT_DIR/build_everything.py"
run_gate "run tests" "$VENV_PYTHON" -m pytest
run_gate "run Live Knowledge Certification" "$VENV_PYTHON" "$ROOT_DIR/build_live_knowledge_certification.py"
build_release_bundle
verify_remote_deploy_config
prepare_remote_release
run_remote_install
run_remote_acceptance
run_remote_start
run_remote_smoke_test

trap - EXIT
log_line "$LOG_FILE" "PASS: live knowledge cutover deployment completed."
