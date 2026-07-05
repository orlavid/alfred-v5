from pathlib import Path
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
