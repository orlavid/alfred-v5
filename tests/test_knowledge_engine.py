from pathlib import Path

from src.executive.knowledge_engine import build_executive_state


def test_build_executive_state_returns_normalised_state():
    state = build_executive_state(Path("evidence/alfred-inventory"))

    assert state.board is not None
    assert isinstance(state.executive_health, dict)
    assert "status" in state.executive_health
    assert isinstance(state.priorities, tuple)
    assert isinstance(state.objectives, tuple)
    assert isinstance(state.companies, tuple)
    assert isinstance(state.decisions, tuple)
    assert isinstance(state.meetings, tuple)
    if state.meetings:
        assert isinstance(state.meetings[0].subject, str)
        assert state.meetings[0].subject
    assert hasattr(state.followups, "overdue")
    assert hasattr(state.open_loops, "critical_open_loops")
    assert isinstance(state.projects, tuple)
    assert isinstance(state.suppliers, tuple)
    assert isinstance(state.people, tuple)
    assert isinstance(state.recommendations, tuple)
    assert state.confidence in {"HIGH", "MEDIUM", "LOW"}
    assert isinstance(state.engine_result, dict)
    assert isinstance(state.vault, dict)
    assert isinstance(state.entities, tuple)
    assert isinstance(state.neighbours, dict)
