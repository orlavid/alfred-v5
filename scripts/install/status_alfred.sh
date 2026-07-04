#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
CONFIG_FILE="$INSTALL_ROOT/config/config.yaml"
APP_DIR="$INSTALL_ROOT/app"
RUNTIME_DIR="$INSTALL_ROOT/runtime"
STATUS_FILE="$RUNTIME_DIR/status.env"

get_config_value() {
  local key="$1"
  awk -F': ' -v lookup="$key" '
    $1 == lookup {
      print $2
      exit
    }
  ' "$CONFIG_FILE" | sed 's/^ *//'
}

report_line() {
  printf "%-24s %s\n" "$1" "$2"
}

[[ -f "$CONFIG_FILE" ]] || { echo "FAIL: missing $CONFIG_FILE" >&2; exit 1; }

BUILD_VERSION="$(grep '^build_version=' "$INSTALL_ROOT/runtime/BUILD_INFO" 2>/dev/null | cut -d'=' -f2- || echo unknown)"
PYTHON_EXEC="$(get_config_value "  executable" | head -n 1)"
NODE_EXEC="$(command -v node 2>/dev/null || echo missing)"
VAULT_PATH="$(awk '/^  vault:/ {print $2; exit}' "$CONFIG_FILE")"
EXEC_STATE_FILE="$(awk '/^  executive_state_output:/ {print $2; exit}' "$CONFIG_FILE")"
DASHBOARD_FILE="$(awk '/^  api_output:/ {print $2; exit}' "$CONFIG_FILE")"
PIPELINE_FILE="$(awk '/^  pipeline_output:/ {print $2; exit}' "$CONFIG_FILE")"
UI_BUILD_FILE="$APP_DIR/dist/index.html"

if [[ -f "$EXEC_STATE_FILE" ]]; then
  EXEC_STATE_FRESHNESS="present"
else
  EXEC_STATE_FRESHNESS="missing"
fi

if [[ -f "$DASHBOARD_FILE" ]]; then
  DASHBOARD_STATUS="present"
else
  DASHBOARD_STATUS="missing"
fi

if [[ -f "$UI_BUILD_FILE" ]]; then
  UI_STATUS="built"
else
  UI_STATUS="not_built"
fi

OPTIONAL_SERVICES="$(awk '
  /llamaindex:/ {llama=$2}
  /llm_wiki_enrichment:/ {wiki=$2}
  /deep_research:/ {deep=$2}
  END {printf "llamaindex=%s, llm_wiki=%s, deep_research=%s", llama, wiki, deep}
' "$CONFIG_FILE")"

echo "Alfred Platform Status"
echo
report_line "Build version" "$BUILD_VERSION"
report_line "Python" "${PYTHON_EXEC:-missing}"
report_line "Node" "$NODE_EXEC"
report_line "Vault configured" "${VAULT_PATH:-missing}"
report_line "ExecutiveState freshness" "$EXEC_STATE_FRESHNESS"
report_line "Dashboard API" "$DASHBOARD_STATUS"
report_line "UI status" "$UI_STATUS"
report_line "Optional services" "$OPTIONAL_SERVICES"
report_line "Pipeline output" "$( [[ -f "$PIPELINE_FILE" ]] && echo present || echo missing )"

if [[ -f "$STATUS_FILE" ]]; then
  echo
  cat "$STATUS_FILE"
fi
