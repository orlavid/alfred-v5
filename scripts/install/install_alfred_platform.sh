#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
APP_DIR="$INSTALL_ROOT/app"
CONFIG_DIR="$INSTALL_ROOT/config"
DATA_DIR="$INSTALL_ROOT/data"
LOG_DIR="$INSTALL_ROOT/logs"
RUNTIME_DIR="$INSTALL_ROOT/runtime"

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

copy_tree() {
  local source_dir="$1"
  local target_dir="$2"
  mkdir -p "$target_dir"
  rsync -a \
    --exclude '.git/' \
    --exclude '.venv/' \
    --exclude 'node_modules/' \
    --exclude 'dist/' \
    --exclude 'output/' \
    --exclude '__pycache__/' \
    "$source_dir/" "$target_dir/"
}

mkdir -p "$INSTALL_ROOT"
run_step "create install root" mkdir -p "$APP_DIR" "$CONFIG_DIR" "$DATA_DIR" "$LOG_DIR" "$RUNTIME_DIR"
run_step "copy Alfred application" copy_tree "$ROOT_DIR" "$APP_DIR"

if [[ ! -f "$CONFIG_DIR/config.yaml" ]]; then
  run_step "seed Alfred configuration" "$ROOT_DIR/scripts/install/configure_alfred.sh"
else
  pass "existing Alfred configuration preserved"
fi

cat > "$RUNTIME_DIR/BUILD_INFO" <<EOF
build_version=$(git -C "$ROOT_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)
installed_from=$ROOT_DIR
installed_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
install_root=$INSTALL_ROOT
EOF
pass "build info recorded"

echo "PASS: Alfred platform package installed into $INSTALL_ROOT"
echo "INFO: Review $CONFIG_DIR/config.yaml before starting Alfred."
