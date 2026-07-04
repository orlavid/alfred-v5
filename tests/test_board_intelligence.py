from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

from src.board.board_registry import build_board_governance
from src.board.board_intelligence import build_board_intelligence_from_state
from src.executive.executive_state import ExecutiveState


def test_build_board_intelligence_from_state_assigns_reviews():
    board = build_board_governance()
    objective = SimpleNamespace(title="Objective A", status="AT RISK")
    project = SimpleNamespace(title="Project Atlas", status="AT RISK")
    state = ExecutiveState(
        board=board,
        objectives=(objective,),
        projects=(project,),
        decisions=({"title": "Decision 1"},),
        recommendations=("Escalate Project Atlas.",),
        executive_plans=(
            SimpleNamespace(project_title="Project Atlas", status="Draft"),
        ),
        risks=(),
    )

    report = build_board_intelligence_from_state(state)

    assert report.objective_assignments[0].board_member == "Sentinel"
    assert report.project_assignments[0].board_member == "Titan"
    assert report.ad_hoc_review.approval_required is True
    assert any("Proposed Executive Update" in item for item in report.ad_hoc_review.proposed_executive_updates)


def test_build_board_intelligence_generates_output():
    output = Path("output/Board_Intelligence.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_board_intelligence.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()
    content = output.read_text()
    assert "# Board Intelligence" in content
    assert "## Ad Hoc Board Review" in content
    assert "## Monthly Board Meeting" in content
