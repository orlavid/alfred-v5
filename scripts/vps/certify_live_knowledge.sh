#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="${1:-$(script_log_path "certify_live_knowledge")}"
CONFIG_FILE="${ALFRED_CONFIG_FILE:-${ALFRED_INSTALL_ROOT:-/opt/alfred}/config/config.yaml}"

: > "$LOG_FILE"

log_line "$LOG_FILE" "Live knowledge certification started."
log_line "$LOG_FILE" "This gate proves Alfred is reading configured Obsidian evidence rather than placeholder data."

require_command "$LOG_FILE" python3
require_file "$LOG_FILE" "$CONFIG_FILE"

APP_DIR="$(yaml_value "$CONFIG_FILE" "  app")"
PYTHON_EXEC="$(yaml_value "$CONFIG_FILE" "  executable")"
VAULT_PATH="$(awk '/^  vault:/ {print $2; exit}' "$CONFIG_FILE")"
OUTPUT_DIR="$(awk '/^  output:/ {print $2; exit}' "$CONFIG_FILE")"

require_non_empty "$LOG_FILE" "app dir" "$APP_DIR"
require_non_empty "$LOG_FILE" "python executable" "$PYTHON_EXEC"
require_non_empty "$LOG_FILE" "vault path" "$VAULT_PATH"
require_non_empty "$LOG_FILE" "output path" "$OUTPUT_DIR"
require_directory "$LOG_FILE" "$APP_DIR"
require_directory "$LOG_FILE" "$VAULT_PATH"

if is_dry_run; then
  log_line "$LOG_FILE" "DRY-RUN: would rebuild pipeline and inspect live-knowledge artefacts under $OUTPUT_DIR"
  exit 0
fi

cd "$APP_DIR"
run_logged "$LOG_FILE" "rebuild executive pipeline" "$PYTHON_EXEC" build_executive_pipeline.py
run_logged "$LOG_FILE" "rebuild follow-up intelligence" "$PYTHON_EXEC" build_followups.py
run_logged "$LOG_FILE" "rebuild open-loop intelligence" "$PYTHON_EXEC" build_open_loops.py

KNOWLEDGE_JSON="$OUTPUT_DIR/Executive_Knowledge.json"
GRAPH_JSON="$OUTPUT_DIR/Knowledge_Graph.json"
STATE_SUMMARY="$OUTPUT_DIR/ExecutiveState_Summary.md"

require_file "$LOG_FILE" "$KNOWLEDGE_JSON"
require_file "$LOG_FILE" "$GRAPH_JSON"
require_file "$LOG_FILE" "$STATE_SUMMARY"

CERT_OUTPUT="$("$PYTHON_EXEC" - "$KNOWLEDGE_JSON" "$GRAPH_JSON" "$STATE_SUMMARY" "$VAULT_PATH" <<'PY'
import json
import sys
from pathlib import Path

from src.followups.followup_intelligence import build_followup_intelligence
from src.openloops.open_loop_intelligence import build_open_loop_intelligence

knowledge = json.loads(Path(sys.argv[1]).read_text())
graph = json.loads(Path(sys.argv[2]).read_text())
state_summary = Path(sys.argv[3]).read_text()
vault_root = Path(sys.argv[4])
followups = build_followup_intelligence(vault_root)
open_loops = build_open_loop_intelligence(vault_root)

inventory = knowledge.get("entity_inventory", {})
graph_stats = graph.get("statistics", {})

counts = {
    "objectives": inventory.get("objective", 0),
    "projects": inventory.get("project", 0),
    "companies": inventory.get("company", 0),
    "people": inventory.get("person", 0),
    "decisions": inventory.get("decision", 0),
    "daily_logs": inventory.get("daily_log", 0),
    "open_loops": open_loops.open_loop_count,
    "followups": followups.followup_count,
    "knowledge_graph_nodes": graph_stats.get("node_count", 0),
    "knowledge_graph_edges": graph_stats.get("edge_count", 0),
    "executive_state_generated": 1 if "# ExecutiveState Summary" in state_summary else 0,
}

zero_sensitive = [
    "objectives",
    "projects",
    "people",
    "knowledge_graph_nodes",
    "knowledge_graph_edges",
    "executive_state_generated",
]

for key, value in counts.items():
    print(f"{key}={value}")

if any(counts[key] == 0 for key in zero_sensitive):
    raise SystemExit(2)
PY
)" || fail_line "$LOG_FILE" "live knowledge certification counts were unexpectedly zero"

while IFS= read -r line; do
  [[ -n "$line" ]] && log_line "$LOG_FILE" "CERT: $line"
done <<< "$CERT_OUTPUT"

log_line "$LOG_FILE" "PASS: live knowledge certification completed."
