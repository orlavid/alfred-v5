from pathlib import Path
import subprocess
import sys

from src.executive.executive_state import build_executive_state


def test_build_executive_state_exposes_canonical_runtime_model():
    state = build_executive_state(Path("evidence/alfred-inventory"))

    assert state.board is not None
    assert len(state.board.board_members) >= 1
    assert isinstance(state.objectives, tuple)
    assert isinstance(state.projects, tuple)
    assert isinstance(state.companies, tuple)
    assert isinstance(state.people, tuple)
    assert isinstance(state.meetings, tuple)
    if state.meetings:
        assert isinstance(state.meetings[0].subject, str)
        assert state.meetings[0].subject
    assert isinstance(state.decisions, tuple)
    assert isinstance(state.risks, tuple)
    assert isinstance(state.policies, tuple)
    assert hasattr(state.followups, "overdue")
    assert hasattr(state.open_loops, "critical_open_loops")
    assert isinstance(state.executive_health, dict)
    assert isinstance(state.objective_health, dict)
    assert isinstance(state.project_health, dict)
    assert state.relationship_graph is not None
    assert isinstance(state.recommendations, tuple)
    assert state.confidence in {"HIGH", "MEDIUM", "LOW"}
    assert isinstance(state.summary, tuple)


def test_build_executive_state_generates_summary_report():
    output = Path("output/ExecutiveState_Summary.md")
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [sys.executable, "build_executive_state.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output.exists()

    content = output.read_text()
    assert "# ExecutiveState Summary" in content
    assert "## Summary" in content
    assert "## Board" in content
    assert "## Entity Coverage" in content
    assert "## Health" in content
    assert "## Recommendations" in content
    assert "## Confidence" in content
