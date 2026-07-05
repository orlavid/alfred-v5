#!/bin/bash
set -euo pipefail

DEPLOY_ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ALFRED_INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
ALFRED_DEPLOY_LOG_DIR="${ALFRED_DEPLOY_LOG_DIR:-$DEPLOY_ROOT_DIR/deployment_logs}"
mkdir -p "$ALFRED_DEPLOY_LOG_DIR"

timestamp_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

is_dry_run() {
  [[ "${ALFRED_DRY_RUN:-0}" == "1" ]]
}

script_log_path() {
  local script_name="$1"
  printf "%s/%s.log" "$ALFRED_DEPLOY_LOG_DIR" "$script_name"
}

log_line() {
  local log_file="$1"
  shift
  local message="$*"
  printf "[%s] %s\n" "$(timestamp_utc)" "$message" | tee -a "$log_file"
}

fail_line() {
  local log_file="$1"
  shift
  log_line "$log_file" "FAIL: $*"
  exit 1
}

run_logged() {
  local log_file="$1"
  local label="$2"
  shift 2
  log_line "$log_file" "RUN: $label"
  "$@" >>"$log_file" 2>&1 || fail_line "$log_file" "$label"
  log_line "$log_file" "PASS: $label"
}

require_command() {
  local log_file="$1"
  local command_name="$2"
  command -v "$command_name" >/dev/null 2>&1 || fail_line "$log_file" "missing required command: $command_name"
  log_line "$log_file" "PASS: command available: $command_name"
}

require_file() {
  local log_file="$1"
  local path="$2"
  [[ -f "$path" ]] || fail_line "$log_file" "missing required file: $path"
  log_line "$log_file" "PASS: file present: $path"
}

require_directory() {
  local log_file="$1"
  local path="$2"
  [[ -d "$path" ]] || fail_line "$log_file" "missing required directory: $path"
  log_line "$log_file" "PASS: directory present: $path"
}

require_non_empty() {
  local log_file="$1"
  local label="$2"
  local value="$3"
  [[ -n "$value" ]] || fail_line "$log_file" "missing required value: $label"
  log_line "$log_file" "PASS: required value provided: $label"
}

run_or_note_dry_run() {
  local log_file="$1"
  local label="$2"
  shift 2
  if is_dry_run; then
    log_line "$log_file" "DRY-RUN: $label -> $*"
    return 0
  fi
  run_logged "$log_file" "$label" "$@"
}

yaml_value() {
  local file="$1"
  local key="$2"
  awk -F': ' -v lookup="$key" '$1 == lookup {print $2; exit}' "$file" | sed 's/^ *//'
}
