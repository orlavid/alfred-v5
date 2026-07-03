from pathlib import Path

from src.executive.knowledge_engine import build_executive_state


def test_build_executive_state_returns_normalised_state():
    state = build_executive_state(Path("evidence/alfred-inventory"))

    assert isinstance(state.executive_health, dict)
    assert "status" in state.executive_health
    assert isinstance(state.priorities, list)
    assert isinstance(state.objectives, list)
    assert isinstance(state.meetings, list)
    assert len(state.meetings) == 1
    assert state.meetings[0].subject == "Barclays"
    assert hasattr(state.followups, "overdue")
    assert hasattr(state.open_loops, "critical_open_loops")
    assert isinstance(state.projects, list)
    assert isinstance(state.suppliers, list)
    assert isinstance(state.people, list)
    assert isinstance(state.recommendations, list)
    assert state.confidence in {"HIGH", "MEDIUM", "LOW"}
    assert isinstance(state.engine_result, dict)
    assert isinstance(state.vault, dict)
    assert isinstance(state.entities, list)
    assert isinstance(state.neighbours, dict)
