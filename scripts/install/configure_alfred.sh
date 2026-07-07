#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
CONFIG_DIR="$INSTALL_ROOT/config"
CONFIG_FILE="$CONFIG_DIR/config.yaml"
PROFILE="${ALFRED_DEPLOYMENT_PROFILE:-VPS}"
VAULT_PATH="${ALFRED_OBSIDIAN_VAULT:-}"
OUTPUT_PATH="${ALFRED_OUTPUT_PATH:-$INSTALL_ROOT/app/output}"
LLAMAINDEX_STATUS="${ALFRED_LLAMAINDEX_STATUS:-not_installed}"
LLM_WIKI_STATUS="${ALFRED_LLM_WIKI_STATUS:-not_installed}"
DEEP_RESEARCH_STATUS="${ALFRED_DEEP_RESEARCH_STATUS:-not_installed}"
LLM_PROVIDER="${ALFRED_LLM_PROVIDER:-placeholder}"
LLM_MODEL="${ALFRED_LLM_MODEL:-placeholder}"
LLM_API_BASE="${ALFRED_LLM_API_BASE:-placeholder}"
LLM_API_KEY_ENV="${ALFRED_LLM_API_KEY_ENV:-ALFRED_LLM_API_KEY}"

mkdir -p "$CONFIG_DIR"

if [[ -f "$CONFIG_FILE" ]]; then
  echo "PASS: existing configuration preserved at $CONFIG_FILE"
  exit 0
fi

if [[ -z "$VAULT_PATH" ]]; then
  echo "FAIL: ALFRED_OBSIDIAN_VAULT must be set before creating $CONFIG_FILE" >&2
  exit 1
fi

cat > "$CONFIG_FILE" <<EOF
deployment:
  profile: $PROFILE
  build_version: unknown
paths:
  install_root: $INSTALL_ROOT
  app: $INSTALL_ROOT/app
  config: $INSTALL_ROOT/config
  data: $INSTALL_ROOT/data
  logs: $INSTALL_ROOT/logs
  runtime: $INSTALL_ROOT/runtime
  vault: $VAULT_PATH
  output: $OUTPUT_PATH
python:
  executable: ${ALFRED_PYTHON:-$INSTALL_ROOT/.venv/bin/python}
node:
  executable: ${ALFRED_NODE:-$(command -v node 2>/dev/null || echo node)}
  npm: ${ALFRED_NPM:-$(command -v npm 2>/dev/null || echo npm)}
services:
  dashboard_api: enabled
  ui: enabled
  optional:
    llamaindex: $LLAMAINDEX_STATUS
    llm_wiki_enrichment: $LLM_WIKI_STATUS
    deep_research: $DEEP_RESEARCH_STATUS
models:
  provider: $LLM_PROVIDER
  model: $LLM_MODEL
api:
  base_url: $LLM_API_BASE
  key_env_var: $LLM_API_KEY_ENV
runtime:
  host: 127.0.0.1
  ui_port: 4173
  api_output: $OUTPUT_PATH/Dashboard_Home.json
  executive_state_output: $OUTPUT_PATH/ExecutiveState_Summary.md
  pipeline_output: $OUTPUT_PATH/Executive_Pipeline_Report.md
EOF

echo "PASS: wrote $CONFIG_FILE"
