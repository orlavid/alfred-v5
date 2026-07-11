from pathlib import Path
import inspect
import json
import subprocess
import sys

from src.api.dashboard_api import get_dashboard_home


def test_get_dashboard_home_returns_expected_shape():
    payload = get_dashboard_home(Path("evidence/alfred-inventory"))

    assert "burning_fires" in payload
    assert "plan_today" in payload
    assert "next_best_action" in payload
    assert "operating_picture" in payload
    assert "navigation_priorities" in payload
    assert "interruption_policy" in payload
    assert "generated_from" in payload
    assert "objectives" in payload
    assert "projects" in payload
    assert "meetings" in payload
    assert "board" in payload
    assert "ask_alfred" in payload
    assert "daily_brief" in payload
    assert "knowledge" in payload
    assert "admin_configuration" in payload
    assert isinstance(payload["burning_fires"], list)
    assert isinstance(payload["plan_today"], list)
    assert isinstance(payload["next_best_action"], dict)
    assert isinstance(payload["operating_picture"], dict)
    assert isinstance(payload["navigation_priorities"], list)
    assert isinstance(payload["interruption_policy"], dict)
    assert payload["generated_from"]["runtime_model"] == "ExecutiveState"
    assert "Executive Reasoning" in payload["generated_from"]["sources"]
    assert payload["board"]["members"]
    assert payload["ask_alfred"]["responses"]
    assert payload["admin_configuration"]["actions"]
    assert payload["admin_configuration"]["overview"]["environment_score"] >= 0
    assert payload["generated_from"]["production_mode"] is True
    if payload["burning_fires"]:
        assert {"origin", "confidence", "source_notes", "provider"} <= payload["burning_fires"][0].keys()
    if payload["plan_today"]:
        assert {"origin", "confidence", "source_notes", "provider"} <= payload["plan_today"][0].keys()
    assert {"origin", "confidence", "source_notes", "provider"} <= payload["next_best_action"].keys()


def test_dashboard_empty_vault_returns_explicit_no_evidence(tmp_path):
    payload = get_dashboard_home(tmp_path / "missing-evidence", vault_root=tmp_path / "missing-vault")

    assert payload["next_best_action"]["action"] == "No evidence found"
    assert payload["meetings"]["subject"] == "No active meeting identified."


def test_build_dashboard_api_generates_json_output():
    output = Path("output/Dashboard_Home.json")
    public_output = Path("web/public/api/dashboard-home.json")
    if output.exists():
        output.unlink()
    if public_output.exists():
        public_output.unlink()

    result = subprocess.run(
        [sys.executable, "build_dashboard_api.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output.exists()
    assert public_output.exists()

    payload = json.loads(output.read_text())
    assert "burning_fires" in payload
    assert "plan_today" in payload
    assert "next_best_action" in payload
    assert "operating_picture" in payload
    assert "navigation_priorities" in payload
    assert "interruption_policy" in payload
    assert "generated_from" in payload
    assert "board" in payload
    assert "admin_configuration" in payload


def test_dashboard_consumes_executive_state_only():
    import src.api.dashboard_api as dashboard_api_module

    source = inspect.getsource(dashboard_api_module)

    assert "build_executive_state(" in source
    assert "build_executive_knowledge(" not in source
    assert "load_vault(" not in source


def test_dashboard_does_not_depend_on_direct_followup_or_open_loop_builders():
    import src.api.dashboard_api as dashboard_api_module

    source = inspect.getsource(dashboard_api_module)

    assert "build_followup_intelligence(" not in source
    assert "build_open_loop_intelligence(" not in source


def test_objective_management_payload_includes_summary_and_detail_fields(tmp_path):
    vault = tmp_path / "vault"
    (vault / "09 Governance" / "Objectives").mkdir(parents=True)
    (vault / "03 Projects").mkdir(parents=True)
    (vault / "09 Governance" / "Decisions").mkdir(parents=True)
    (vault / "08 Follow Ups").mkdir(parents=True)
    (vault / "07 Open Loops").mkdir(parents=True)

    (vault / "09 Governance" / "Objectives" / "2026 Executive Objectives.md").write_text(
        "# 2026 Executive Objectives\n\n"
        "## Objectives\n\n"
        "- Operational Governance\n"
    )
    (vault / "09 Governance" / "Objectives" / "Operational Governance.md").write_text(
        "# Operational Governance\n"
        "Type: Objective\n"
        "Status: Supported\n"
        "Last Activity: 2026-07-01\n"
    )
    (vault / "03 Projects" / "Governance Programme.md").write_text(
        "# Governance Programme\n"
        "Status: Active\n"
        "Owner: Jane Smith\n"
        "[[Operational Governance]]\n"
    )
    (vault / "09 Governance" / "Decisions" / "Governance Approval.md").write_text(
        "# Governance Approval\n"
        "[[Operational Governance]]\n"
    )
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text(
        "# Follow Up Actions\n\n"
        "## Follow-Up Actions\n\n"
        "- Confirm governance checkpoint this week\n"
    )
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text(
        "# Open Loop Register\n\n"
        "## LOOP-001\n"
        "Issue: Governance decision pending\n"
        "Status: OPEN\n"
        "Priority: HIGH\n"
        "Owner: Jane Smith\n"
    )

    payload = get_dashboard_home(tmp_path / "evidence", vault_root=vault)

    assert payload["objectives"]["items"]
    item = next(item for item in payload["objectives"]["items"] if item["title"] == "Operational Governance")
    detail = payload["objectives"]["details"][item["objective_id"]]

    assert item["title"] == "Operational Governance"
    assert item["route"].startswith("/objectives/")
    assert item["supporting_project_count"] >= 1
    assert "current_status" in detail
    assert "smart_assessment" in detail
    assert detail["evidence_sources"]
    assert detail["provenance"]["objective"]
