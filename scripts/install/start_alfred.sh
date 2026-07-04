#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
CONFIG_FILE="$INSTALL_ROOT/config/config.yaml"
APP_DIR="$INSTALL_ROOT/app"
LOG_DIR="$INSTALL_ROOT/logs"
RUNTIME_DIR="$INSTALL_ROOT/runtime"

[[ -f "$CONFIG_FILE" ]] || { echo "FAIL: missing $CONFIG_FILE" >&2; exit 1; }
mkdir -p "$LOG_DIR" "$RUNTIME_DIR"

cd "$APP_DIR"

if [[ -x ".venv/bin/python" ]]; then
  PYTHON=".venv/bin/python"
else
  PYTHON="$(command -v python3 || command -v python)"
fi

"$PYTHON" build_dashboard_api.py > "$LOG_DIR/dashboard_api.log" 2>&1
echo "dashboard_api_built_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")" > "$RUNTIME_DIR/status.env"

if command -v npm >/dev/null 2>&1; then
  npm run build > "$LOG_DIR/ui_build.log" 2>&1
  echo "ui_built_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "$RUNTIME_DIR/status.env"
fi

echo "PASS: Alfred package prepared at $INSTALL_ROOT"
echo "INFO: Start long-running app processes only after profile-specific supervision is configured."
