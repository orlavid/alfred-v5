from pathlib import Path
import json
import subprocess
import sys

from src.api.dashboard_api import get_dashboard_home


def test_get_dashboard_home_returns_expected_shape():
    payload = get_dashboard_home(Path("evidence/alfred-inventory"))

    assert list(payload.keys()) == [
        "burning_fires",
        "plan_today",
        "next_best_action",
        "operating_picture",
        "navigation_priorities",
        "interruption_policy",
        "generated_from",
    ]
    assert isinstance(payload["burning_fires"], list)
    assert isinstance(payload["plan_today"], list)
    assert isinstance(payload["next_best_action"], dict)
    assert isinstance(payload["operating_picture"], dict)
    assert isinstance(payload["navigation_priorities"], list)
    assert isinstance(payload["interruption_policy"], dict)
    assert payload["generated_from"]["runtime_model"] == "ExecutiveState"
    assert "Executive Reasoning" in payload["generated_from"]["sources"]


def test_build_dashboard_api_generates_json_output():
    output = Path("output/Dashboard_Home.json")
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [sys.executable, "build_dashboard_api.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output.exists()

    payload = json.loads(output.read_text())
    assert "burning_fires" in payload
    assert "plan_today" in payload
    assert "next_best_action" in payload
    assert "operating_picture" in payload
    assert "navigation_priorities" in payload
    assert "interruption_policy" in payload
    assert "generated_from" in payload
