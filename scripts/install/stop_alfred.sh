#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
RUNTIME_DIR="$INSTALL_ROOT/runtime"

if command -v systemctl >/dev/null 2>&1; then
  systemctl stop alfred.service >/dev/null 2>&1 || true
fi
rm -f "$RUNTIME_DIR/status.env"
echo "PASS: Alfred runtime markers cleared at $INSTALL_ROOT"
echo "INFO: Alfred service was stopped if present; Hermes and other host services were untouched."
