#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
RUNTIME_DIR="$INSTALL_ROOT/runtime"

rm -f "$RUNTIME_DIR/status.env"
echo "PASS: Alfred runtime markers cleared at $INSTALL_ROOT"
echo "INFO: No host services were stopped by this script."
