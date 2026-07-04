#!/bin/bash
set -euo pipefail

INSTALL_ROOT="${ALFRED_INSTALL_ROOT:-/opt/alfred}"
CONFIG_DIR="$INSTALL_ROOT/config"
CONFIG_FILE="$CONFIG_DIR/config.yaml"

mkdir -p "$CONFIG_DIR"

if [[ -f "$CONFIG_FILE" ]]; then
  echo "PASS: existing configuration preserved at $CONFIG_FILE"
  exit 0
fi

cat > "$CONFIG_FILE" <<EOF
deployment:
  profile: VPS
  build_version: unknown
paths:
  install_root: $INSTALL_ROOT
  app: $INSTALL_ROOT/app
  config: $INSTALL_ROOT/config
  data: $INSTALL_ROOT/data
  logs: $INSTALL_ROOT/logs
  runtime: $INSTALL_ROOT/runtime
  vault: ${ALFRED_OBSIDIAN_VAULT:-$HOME/Documents/My Vault/My Vault}
python:
  executable: ${ALFRED_PYTHON:-$INSTALL_ROOT/app/.venv/bin/python}
node:
  executable: ${ALFRED_NODE:-$(command -v node 2>/dev/null || echo node)}
  npm: ${ALFRED_NPM:-$(command -v npm 2>/dev/null || echo npm)}
services:
  dashboard_api: enabled
  ui: enabled
  optional:
    llamaindex: not_installed
    llm_wiki_enrichment: not_installed
    deep_research: not_installed
runtime:
  host: 127.0.0.1
  ui_port: 4173
  api_output: $INSTALL_ROOT/app/output/Dashboard_Home.json
  executive_state_output: $INSTALL_ROOT/app/output/ExecutiveState_Summary.md
  pipeline_output: $INSTALL_ROOT/app/output/Executive_Pipeline_Report.md
EOF

echo "PASS: wrote $CONFIG_FILE"
