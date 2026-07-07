#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
CONFIG_FILE="$INSTALL_ROOT/config/config.yaml"
APP_DIR="$INSTALL_ROOT/app"
LOG_DIR="$INSTALL_ROOT/logs"
RUNTIME_DIR="$INSTALL_ROOT/runtime"
VENV_PYTHON="$INSTALL_ROOT/.venv/bin/python"
SERVICE_UNIT_SOURCE="$INSTALL_ROOT/app/scripts/install/alfred.service"
SERVICE_UNIT_TARGET="/etc/systemd/system/alfred.service"

[[ -f "$CONFIG_FILE" ]] || { echo "FAIL: missing $CONFIG_FILE" >&2; exit 1; }
mkdir -p "$LOG_DIR" "$RUNTIME_DIR"

cd "$APP_DIR"

[[ -x "$VENV_PYTHON" ]] || { echo "FAIL: missing runtime python: $VENV_PYTHON" >&2; exit 1; }
PYTHON="$VENV_PYTHON"

"$PYTHON" build_dashboard_api.py > "$LOG_DIR/dashboard_api.log" 2>&1
echo "dashboard_api_built_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")" > "$RUNTIME_DIR/status.env"

if command -v npm >/dev/null 2>&1; then
  npm run build > "$LOG_DIR/ui_build.log" 2>&1
  echo "ui_built_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "$RUNTIME_DIR/status.env"
fi

if command -v systemctl >/dev/null 2>&1; then
  cp "$SERVICE_UNIT_SOURCE" "$SERVICE_UNIT_TARGET"
  systemctl daemon-reload
  systemctl enable alfred.service >/dev/null 2>&1 || true
  systemctl restart alfred.service
  echo "service_unit=$SERVICE_UNIT_TARGET" >> "$RUNTIME_DIR/status.env"
  echo "service_started_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "$RUNTIME_DIR/status.env"
fi

echo "PASS: Alfred runtime prepared at $INSTALL_ROOT"
echo "INFO: Alfred service uses $VENV_PYTHON"
