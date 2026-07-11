#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
APP_DIR="$INSTALL_ROOT/app"
CONFIG_FILE="$INSTALL_ROOT/config/config.yaml"
VENV_PYTHON="$INSTALL_ROOT/.venv/bin/python"
HOST="$(awk '/^  host:/ {print $2; exit}' "$CONFIG_FILE" 2>/dev/null || echo 127.0.0.1)"
PORT="$(awk '/^  ui_port:/ {print $2; exit}' "$CONFIG_FILE" 2>/dev/null || echo 4173)"

[[ -f "$CONFIG_FILE" ]] || { echo "FAIL: missing $CONFIG_FILE" >&2; exit 1; }
[[ -x "$VENV_PYTHON" ]] || { echo "FAIL: missing runtime python: $VENV_PYTHON" >&2; exit 1; }
[[ -f "$APP_DIR/dist/index.html" ]] || { echo "FAIL: missing built UI at $APP_DIR/dist/index.html" >&2; exit 1; }

cd "$APP_DIR"
exec "$VENV_PYTHON" -m src.runtime.app_server
