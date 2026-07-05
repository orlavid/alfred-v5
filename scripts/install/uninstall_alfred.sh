#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
APP_DIR="$INSTALL_ROOT/app"
LOG_DIR="$INSTALL_ROOT/logs"
RUNTIME_DIR="$INSTALL_ROOT/runtime"

rm -rf "$APP_DIR" "$LOG_DIR" "$RUNTIME_DIR"
mkdir -p "$INSTALL_ROOT"

cat <<EOF
PASS: Alfred application runtime removed from $INSTALL_ROOT
SAFE PRESERVATION:
- $INSTALL_ROOT/config retained
- $INSTALL_ROOT/data retained
- Obsidian vault untouched
- Cloudflare untouched
- Telegram untouched
- External user data untouched
EOF
