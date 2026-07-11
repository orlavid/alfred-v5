#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT_DIR/scripts/install/deploy_common.sh"

LOG_FILE="$(script_log_path "deploy_validation")"
: > "$LOG_FILE"

CONFIG_FILE="$ALFRED_INSTALL_ROOT/config/config.yaml"
[[ -f "$CONFIG_FILE" ]] || fail_line "$LOG_FILE" "missing $CONFIG_FILE"
[[ -f "$ROOT_DIR/docs/deployment/EXECUTIVE_ACCEPTANCE_TESTS.md" ]] || fail_line "$LOG_FILE" "missing executive acceptance tests document"

APP_DIR="$(yaml_value "$CONFIG_FILE" "  app")"
PYTHON_EXEC="$(yaml_value "$CONFIG_FILE" "  executable")"
API_OUTPUT="$(awk '/^  api_output:/ {print $2; exit}' "$CONFIG_FILE")"
EXEC_STATE_OUTPUT="$(awk '/^  executive_state_output:/ {print $2; exit}' "$CONFIG_FILE")"
PIPELINE_OUTPUT="$(awk '/^  pipeline_output:/ {print $2; exit}' "$CONFIG_FILE")"

[[ -d "$APP_DIR" ]] || fail_line "$LOG_FILE" "missing Alfred app dir: $APP_DIR"
[[ -x "$PYTHON_EXEC" ]] || fail_line "$LOG_FILE" "missing Alfred python executable: $PYTHON_EXEC"

cd "$APP_DIR"

run_logged "$LOG_FILE" "build dashboard api" "$PYTHON_EXEC" build_dashboard_api.py
run_logged "$LOG_FILE" "build executive state" "$PYTHON_EXEC" build_executive_state.py
run_logged "$LOG_FILE" "build executive pipeline" "$PYTHON_EXEC" build_executive_pipeline.py
run_logged "$LOG_FILE" "build daily brief" "$PYTHON_EXEC" build_daily_brief.py
run_logged "$LOG_FILE" "certify live knowledge" "$ROOT_DIR/scripts/vps/certify_live_knowledge.sh" "$LOG_FILE.knowledge"
run_logged "$LOG_FILE" "build knowledge certification" "$PYTHON_EXEC" build_knowledge_certification.py
run_logged "$LOG_FILE" "build semantic equivalence validation" "$PYTHON_EXEC" build_semantic_equivalence_validation.py
run_logged "$LOG_FILE" "build operational readiness" "$PYTHON_EXEC" build_operational_readiness.py
run_logged "$LOG_FILE" "build UI" npm run build
run_logged "$LOG_FILE" "ask Alfred: focus today" "$PYTHON_EXEC" build_ask_alfred.py "What should I focus on today?"
run_logged "$LOG_FILE" "ask Alfred: top objectives" "$PYTHON_EXEC" build_ask_alfred.py "What are my top objectives?"
run_logged "$LOG_FILE" "ask Alfred: prepare for Barclays" "$PYTHON_EXEC" build_ask_alfred.py "Prepare me for Barclays."
run_logged "$LOG_FILE" "ask Alfred: what changed yesterday" "$PYTHON_EXEC" build_ask_alfred.py "What changed yesterday?"
run_logged "$LOG_FILE" "ask Alfred: projects at risk" "$PYTHON_EXEC" build_ask_alfred.py "Which projects are at risk?"
run_logged "$LOG_FILE" "ask Alfred: follow-ups requiring action" "$PYTHON_EXEC" build_ask_alfred.py "What follow-ups need action?"
run_logged "$LOG_FILE" "report Alfred status" "$ROOT_DIR/scripts/install/status_alfred.sh"

[[ -f "$API_OUTPUT" ]] || fail_line "$LOG_FILE" "dashboard api output missing: $API_OUTPUT"
[[ -f "$EXEC_STATE_OUTPUT" ]] || fail_line "$LOG_FILE" "executive state output missing: $EXEC_STATE_OUTPUT"
[[ -f "$PIPELINE_OUTPUT" ]] || fail_line "$LOG_FILE" "pipeline output missing: $PIPELINE_OUTPUT"
[[ -f "$APP_DIR/output/Daily_Brief.md" ]] || fail_line "$LOG_FILE" "daily brief output missing"
[[ -f "$APP_DIR/output/Ask_Alfred.md" ]] || fail_line "$LOG_FILE" "Ask Alfred output missing"
[[ -f "$APP_DIR/output/Knowledge_Certification.md" ]] || fail_line "$LOG_FILE" "knowledge certification markdown output missing"
[[ -f "$APP_DIR/output/Knowledge_Certification.json" ]] || fail_line "$LOG_FILE" "knowledge certification json output missing"
[[ -f "$APP_DIR/output/Semantic_Equivalence_Validation.md" ]] || fail_line "$LOG_FILE" "semantic equivalence markdown output missing"
[[ -f "$APP_DIR/output/Semantic_Equivalence_Validation.json" ]] || fail_line "$LOG_FILE" "semantic equivalence json output missing"
[[ -f "$APP_DIR/dist/index.html" ]] || fail_line "$LOG_FILE" "ui build output missing"

grep -q "Overall Health: GREEN" "$APP_DIR/output/Operational_Readiness_Report.md" || fail_line "$LOG_FILE" "operational readiness is not GREEN"

log_line "$LOG_FILE" "PASS: Validation gates completed."
