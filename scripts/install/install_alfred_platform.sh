#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
APP_DIR="$INSTALL_ROOT/app"
CONFIG_DIR="$INSTALL_ROOT/config"
DATA_DIR="$INSTALL_ROOT/data"
LOG_DIR="$INSTALL_ROOT/logs"
RUNTIME_DIR="$INSTALL_ROOT/runtime"
VENV_DIR="$INSTALL_ROOT/.venv"
DISCOVERY_JSON="$RUNTIME_DIR/environment_inventory.json"
DISCOVERY_YAML="$RUNTIME_DIR/environment_inventory.yaml"

REQUIRED_PATHS=(
  "build_everything.py"
  "requirements.txt"
  "package.json"
  "src"
  "scripts/install/configure_alfred.sh"
  "scripts/install/start_alfred.sh"
  "scripts/install/run_alfred_service.sh"
  "scripts/install/alfred.service"
  "tests"
)

pass() {
  echo "PASS: $1"
}

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

usage() {
  cat <<'EOF'
Usage:
  scripts/install/install_alfred_platform.sh --mode git --git-url <repo> [--git-ref <ref>]
  scripts/install/install_alfred_platform.sh --mode tarball --tarball <release.tar.gz>
  scripts/install/install_alfred_platform.sh --mode local --source-dir <directory>

Exactly one install mode is supported per run:
  git      Clone Alfred from an explicit Git repository.
  tarball  Extract Alfred from an explicit packaged release tarball.
  local    Copy Alfred from an explicit local source directory.

The installer never infers the Alfred source from its own location.
EOF
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "missing required command: $1"
}

real_path() {
  python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).expanduser().resolve())' "$1"
}

ensure_valid_structure() {
  local source_dir="$1"
  for path in "${REQUIRED_PATHS[@]}"; do
    [[ -e "$source_dir/$path" ]] || fail "invalid Alfred source: missing $path in $source_dir"
  done
  [[ -f "$source_dir/scripts/install/install_alfred_platform.sh" ]] || fail "invalid Alfred source: installer script missing"
  pass "validated Alfred source structure at $source_dir"
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

ensure_runtime_venv() {
  local python_bin
  python_bin="${ALFRED_BOOTSTRAP_PYTHON:-$(command -v python3)}"
  [[ -n "$python_bin" ]] || fail "unable to locate python3 for runtime bootstrap"

  if [[ ! -x "$VENV_DIR/bin/python" ]]; then
    "$python_bin" -m venv "$VENV_DIR" || fail "unable to create runtime virtual environment at $VENV_DIR"
  fi

  "$VENV_DIR/bin/python" -m pip install --upgrade pip >/dev/null 2>&1 || fail "unable to upgrade pip in $VENV_DIR"
  "$VENV_DIR/bin/python" -m pip install -r "$APP_DIR/requirements.txt" >/dev/null 2>&1 || fail "unable to install Alfred Python requirements"

  ln -sfn "../.venv" "$APP_DIR/.venv"
  export ALFRED_PYTHON="$VENV_DIR/bin/python"
  pass "runtime virtual environment prepared at $VENV_DIR"
}

apply_environment_discovery() {
  local app_dir="$1"
  local install_root="$2"
  local checked_json="$3"
  local checked_yaml="$4"

  "$VENV_DIR/bin/python" - "$app_dir" "$install_root" "$checked_json" "$checked_yaml" "$CONFIG_DIR/config.yaml" <<'PY'
from pathlib import Path
import json
import os
import sys

app_dir = Path(sys.argv[1])
install_root = Path(sys.argv[2])
inventory_json = Path(sys.argv[3])
inventory_yaml = Path(sys.argv[4])
config_file = Path(sys.argv[5])

sys.path.insert(0, str(app_dir))

from src.operations.environment_discovery import build_environment_inventory, render_detected_environment_yaml

inventory = build_environment_inventory(root=app_dir, install_root=install_root, trigger="startup")
inventory_json.write_text(json.dumps(inventory.as_dict(), indent=2, sort_keys=True))
inventory_yaml.write_text(render_detected_environment_yaml(inventory))

auto = inventory.auto_configured
exports = {}
if "vault_path" in auto and not os.environ.get("ALFRED_OBSIDIAN_VAULT"):
    exports["ALFRED_OBSIDIAN_VAULT"] = auto["vault_path"].value
if "python_executable" in auto and not os.environ.get("ALFRED_PYTHON"):
    exports["ALFRED_PYTHON"] = auto["python_executable"].value
if "node_executable" in auto and not os.environ.get("ALFRED_NODE"):
    exports["ALFRED_NODE"] = auto["node_executable"].value
if "npm_executable" in auto and not os.environ.get("ALFRED_NPM"):
    exports["ALFRED_NPM"] = auto["npm_executable"].value

for key, value in exports.items():
    print(f"EXPORT::{key}={value}")

if config_file.exists():
    original = config_file.read_text().rstrip() + "\n"
    marker = "detected_environment:"
    if marker in original:
        original = original.split(marker, 1)[0].rstrip() + "\n"
    config_file.write_text(original + render_detected_environment_yaml(inventory))

for action in inventory.required_actions:
    print(f"ACTION::{action}")
PY
}

normalise_runtime_config() {
  "$VENV_DIR/bin/python" - "$CONFIG_DIR/config.yaml" "$VENV_DIR/bin/python" <<'PY'
from pathlib import Path
import sys

config_path = Path(sys.argv[1])
python_path = sys.argv[2]
lines = config_path.read_text().splitlines()
updated = []
in_python = False
replaced = False

for line in lines:
    if line.startswith("python:"):
        in_python = True
        updated.append(line)
        continue
    if in_python and not line.startswith("  "):
        in_python = False
    if in_python and line.strip().startswith("executable:"):
        updated.append(f"  executable: {python_path}")
        replaced = True
        continue
    updated.append(line)

if not replaced:
    output = []
    inserted = False
    for line in updated:
        output.append(line)
        if line.startswith("python:"):
            output.append(f"  executable: {python_path}")
            inserted = True
    if inserted:
        updated = output

config_path.write_text("\n".join(updated) + "\n")
PY
}

normalise_extracted_root() {
  local extracted_dir="$1"
  local entries
  entries="$(find "$extracted_dir" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
  if [[ "$entries" == "1" ]] && [[ ! -e "$extracted_dir/build_everything.py" ]]; then
    find "$extracted_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1
  else
    echo "$extracted_dir"
  fi
}

parse_args() {
  MODE=""
  GIT_URL=""
  GIT_REF=""
  TARBALL_PATH=""
  SOURCE_DIR=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --mode)
        MODE="${2:-}"
        shift 2
        ;;
      --git-url)
        GIT_URL="${2:-}"
        shift 2
        ;;
      --git-ref)
        GIT_REF="${2:-}"
        shift 2
        ;;
      --tarball)
        TARBALL_PATH="${2:-}"
        shift 2
        ;;
      --source-dir)
        SOURCE_DIR="${2:-}"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        fail "unknown argument: $1"
        ;;
    esac
  done

  [[ -n "$MODE" ]] || fail "install mode is required. Use --mode git|tarball|local."

  case "$MODE" in
    git)
      [[ -n "$GIT_URL" ]] || fail "--git-url is required for --mode git"
      [[ -z "$TARBALL_PATH" && -z "$SOURCE_DIR" ]] || fail "git mode only accepts --git-url and optional --git-ref"
      ;;
    tarball)
      [[ -n "$TARBALL_PATH" ]] || fail "--tarball is required for --mode tarball"
      [[ -z "$GIT_URL" && -z "$GIT_REF" && -z "$SOURCE_DIR" ]] || fail "tarball mode only accepts --tarball"
      ;;
    local)
      [[ -n "$SOURCE_DIR" ]] || fail "--source-dir is required for --mode local"
      [[ -z "$GIT_URL" && -z "$GIT_REF" && -z "$TARBALL_PATH" ]] || fail "local mode only accepts --source-dir"
      ;;
    *)
      fail "unsupported install mode: $MODE"
      ;;
  esac
}

prepare_source() {
  local staging_dir="$1"
  local prepared_root=""

  case "$MODE" in
    git)
      require_command git
      git clone --depth 1 "$GIT_URL" "$staging_dir/source" >/dev/null 2>&1 || fail "unable to clone Git source: $GIT_URL"
      if [[ -n "$GIT_REF" ]]; then
        git -C "$staging_dir/source" checkout "$GIT_REF" >/dev/null 2>&1 || fail "unable to checkout git ref: $GIT_REF"
      fi
      prepared_root="$staging_dir/source"
      SOURCE_REFERENCE="$GIT_URL${GIT_REF:+@$GIT_REF}"
      ;;
    tarball)
      require_command tar
      [[ -f "$TARBALL_PATH" ]] || fail "tarball not found: $TARBALL_PATH"
      mkdir -p "$staging_dir/extracted"
      tar -xf "$TARBALL_PATH" -C "$staging_dir/extracted" || fail "unable to extract tarball: $TARBALL_PATH"
      prepared_root="$(normalise_extracted_root "$staging_dir/extracted")"
      SOURCE_REFERENCE="$(real_path "$TARBALL_PATH")"
      ;;
    local)
      [[ -d "$SOURCE_DIR" ]] || fail "source directory not found: $SOURCE_DIR"
      prepared_root="$(real_path "$SOURCE_DIR")"
      SOURCE_REFERENCE="$prepared_root"
      ;;
  esac

  PREPARED_SOURCE_ROOT="$prepared_root"
}

prevent_self_copy_loop() {
  local source_root="$1"
  local install_root_real
  local app_dir_real
  install_root_real="$(real_path "$INSTALL_ROOT")"
  app_dir_real="$(real_path "$APP_DIR")"

  if [[ "$source_root" == "$install_root_real" ]]; then
    fail "source directory resolves to the install root; refusing self-copy"
  fi

  case "$app_dir_real" in
    "$source_root"|"$source_root"/*)
      fail "install destination is inside the source tree; refusing recursive self-copy"
      ;;
  esac

  case "$source_root" in
    "$app_dir_real"|"$app_dir_real"/*)
      fail "source directory is inside the install destination; refusing self-copy loop"
      ;;
  esac

  pass "validated source and destination separation"
}

main() {
  parse_args "$@"
  require_command rsync
  require_command python3

  local staging_dir
  staging_dir="$(mktemp -d)"
  trap '[[ -n "${staging_dir:-}" ]] && rm -rf "$staging_dir"' EXIT

  prepare_source "$staging_dir"
  ensure_valid_structure "$PREPARED_SOURCE_ROOT"
  prevent_self_copy_loop "$PREPARED_SOURCE_ROOT"

  mkdir -p "$INSTALL_ROOT"
  mkdir -p "$APP_DIR" "$CONFIG_DIR" "$DATA_DIR" "$LOG_DIR" "$RUNTIME_DIR" "$VENV_DIR"
  pass "created install root"

  copy_tree "$PREPARED_SOURCE_ROOT" "$APP_DIR"
  pass "copied Alfred application from explicit source"
  ensure_runtime_venv

  local discovery_output
  discovery_output="$(apply_environment_discovery "$APP_DIR" "$INSTALL_ROOT" "$DISCOVERY_JSON" "$DISCOVERY_YAML")"
  while IFS= read -r line; do
    case "$line" in
      EXPORT::*)
        export "${line#EXPORT::}"
        ;;
      ACTION::*)
        echo "INFO: Next action: ${line#ACTION::}"
        ;;
    esac
  done <<< "$discovery_output"

  if [[ ! -f "$CONFIG_DIR/config.yaml" ]]; then
    bash "$APP_DIR/scripts/install/configure_alfred.sh"
    pass "seeded Alfred configuration"
  else
    pass "existing Alfred configuration preserved"
  fi

  "$VENV_DIR/bin/python" - "$APP_DIR" "$INSTALL_ROOT" "$DISCOVERY_JSON" "$DISCOVERY_YAML" "$CONFIG_DIR/config.yaml" <<'PY'
from pathlib import Path
import sys
import json

app_dir = Path(sys.argv[1])
install_root = Path(sys.argv[2])
inventory_json = Path(sys.argv[3])
inventory_yaml = Path(sys.argv[4])
config_file = Path(sys.argv[5])

sys.path.insert(0, str(app_dir))

from src.operations.environment_discovery import build_environment_inventory, render_detected_environment_yaml

inventory = build_environment_inventory(root=app_dir, install_root=install_root, trigger="startup")
inventory_json.write_text(json.dumps(inventory.as_dict(), indent=2, sort_keys=True))
inventory_yaml.write_text(render_detected_environment_yaml(inventory))
original = config_file.read_text().rstrip() + "\n"
marker = "detected_environment:"
if marker in original:
    original = original.split(marker, 1)[0].rstrip() + "\n"
config_file.write_text(original + render_detected_environment_yaml(inventory))
PY
  pass "recorded detected environment in config"
  normalise_runtime_config
  pass "normalised runtime configuration"

  cat > "$RUNTIME_DIR/BUILD_INFO" <<EOF
build_version=${ALFRED_BUILD_COMMIT:-$(git -C "$PREPARED_SOURCE_ROOT" rev-parse HEAD 2>/dev/null || echo unknown)}
build_tree_state=${ALFRED_BUILD_TREE_STATE:-$([[ -z "$(git -C "$PREPARED_SOURCE_ROOT" status --short 2>/dev/null)" ]] && echo clean || echo dirty)}
installed_from=$SOURCE_REFERENCE
installed_mode=$MODE
installed_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
install_root=$INSTALL_ROOT
python_executable=$ALFRED_PYTHON
EOF
  pass "build info recorded"

  echo "PASS: Alfred platform package installed into $INSTALL_ROOT"
  echo "INFO: Review $CONFIG_DIR/config.yaml before starting Alfred."
  echo "INFO: Re-run discovery with python -c 'from src.operations.environment_discovery import build_environment_inventory, write_environment_inventory; write_environment_inventory(build_environment_inventory())'"
}

main "$@"
