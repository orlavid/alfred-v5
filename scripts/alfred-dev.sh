#!/bin/bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
SERVE=0

if [[ "${1:-}" == "--serve" ]]; then
  SERVE=1
fi

pass() {
  echo "PASS: $1"
}

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

run_step() {
  local label="$1"
  shift

  if "$@"; then
    pass "$label"
  else
    fail "$label"
  fi
}

cd "$ROOT_DIR" || fail "change directory to repo root"

[[ -x "$VENV_PYTHON" ]] || fail ".venv is missing. Create it before running scripts/alfred-dev.sh"
pass "virtual environment found at .venv"

if [[ ! -d "$ROOT_DIR/node_modules" ]]; then
  echo "INFO: node_modules not found. Running npm install..."
  run_step "npm install" npm install
else
  pass "npm dependencies already installed"
fi

run_step "build Dashboard API" "$VENV_PYTHON" build_dashboard_api.py
run_step "npm build" npm run build

echo "PASS: Alfred local bootstrap complete"
echo "DEV COMMAND: npm run dev -- --host 127.0.0.1"

if [[ "$SERVE" -eq 1 ]]; then
  echo "INFO: starting local Vite dev server"
  exec npm run dev -- --host 127.0.0.1
fi
