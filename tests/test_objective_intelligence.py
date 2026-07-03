from datetime import date
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

from src.objectives.objective_intelligence import (
    SECTION_HEADINGS,
    build_objective_intelligence_from_state,
)
from src.executive.knowledge_engine import ExecutiveState


def test_build_objective_intelligence_from_state_links_records():
    objective = SimpleNamespace(
        title="2026 Executive Objectives",
        path="09 Governance/Objectives/2026 Executive Objectives.md",
        linked_entities=0,
        status="AT RISK",
        recommendation="Review objective linkage; no supporting projects, decisions, people or evidence are connected.",
    )
    project_entity = SimpleNamespace(
        id="03 Projects/Objective Delivery.md",
        type="project",
        title="Objective Delivery",
        path="03 Projects/Objective Delivery.md",
    )
    decision_entity = SimpleNamespace(
        id="09 Governance/Decisions/Objective Approval.md",
        type="decision",
        title="Objective Approval",
        path="09 Governance/Decisions/Objective Approval.md",
    )
    note_entity = SimpleNamespace(
        id="07 AI Memory/Reporting Evidence/2026-05-01 Evidence Bundle.md",
        type="note",
        title="2026-05-01 Evidence Bundle",
        path="07 AI Memory/Reporting Evidence/2026-05-01 Evidence Bundle.md",
    )
    followup = SimpleNamespace(
        title="2026 Executive Objectives",
        path="09 Governance/Objectives/2026 Executive Objectives.md",
        summary="Review objective milestone plan.",
        due_date="2026-05-15",
        priority="HIGH",
    )

    state = ExecutiveState(
        executive_health={"status": "AMBER", "score": 80, "failed": 4},
        priorities=[],
        objectives=[objective],
        meetings=[],
        followups=SimpleNamespace(
            overdue=[followup],
            due_today=[],
            due_this_week=[],
            waiting_on_others=[],
            high_priority=[followup],
        ),
        open_loops=SimpleNamespace(critical_open_loops=[]),
        projects=[],
        suppliers=[],
        people=[],
        risks=[],
        recommendations=[],
        confidence="HIGH",
        engine_result={},
        vault={
            "objectives": {"supported": 0},
            "decisions": {
                "top_decisions": [
                    {"title": "Objective Approval", "importance": 120, "projects": 1, "objectives": 1}
                ]
            },
        },
        entities=[project_entity, decision_entity, note_entity],
        neighbours={
            objective.path: (
                decision_entity.id,
                note_entity.id,
                project_entity.id,
            )
        },
    )

    report = build_objective_intelligence_from_state(state, today=date(2026, 7, 3))

    assert any(item.title == "2026 Executive Objectives" for item in report.objectives_at_risk)
    assert any(item.title == "Objective Delivery" for item in report.projects_supporting_objectives)
    assert any(item.title == "Objective Approval" for item in report.decisions_linked_to_objectives)
    assert any(item.title == "2026 Executive Objectives" for item in report.followups_linked_to_objectives)
    assert any(item.title == "2026 Executive Objectives" for item in report.objectives_with_stale_evidence)
    strategic = report.strategic_objectives[0]
    assert strategic.status == "At Risk"
    assert strategic.confidence == "HIGH"
    assert strategic.supporting_projects == ("Objective Delivery",)
    assert strategic.linked_decisions == ("Objective Approval",)
    assert strategic.stale_evidence is True
    assert "Review objective linkage" in strategic.recommended_next_action


def test_build_objective_intelligence_generates_report():
    output = Path("output/Objective_Intelligence.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_objective_intelligence.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Objective Intelligence" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
    assert "- Status:" in content
    assert "- Confidence:" in content
    assert "- Supporting Projects:" in content
    assert "- Linked Decisions:" in content
    assert "- Stale Evidence:" in content
    assert "- Recommended Next Action:" in content
