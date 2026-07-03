from datetime import date
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

from src.executive.knowledge_engine import ExecutiveState
from src.objectives.objective_project_spine import (
    SECTION_HEADINGS,
    build_objective_project_spine_from_state,
)


def test_build_objective_project_spine_from_state_reports_traceability():
    objective_a = SimpleNamespace(
        id="09 Governance/Objectives/Objective A.md",
        type="objective",
        title="Objective A",
        path="09 Governance/Objectives/Objective A.md",
        linked_entities=2,
        status="SUPPORTED",
        recommendation="Objective has supporting vault evidence.",
    )
    objective_b = SimpleNamespace(
        id="09 Governance/Objectives/Objective B.md",
        type="objective",
        title="Objective B",
        path="09 Governance/Objectives/Objective B.md",
        linked_entities=0,
        status="AT RISK",
        recommendation="Review objective linkage; no supporting projects, decisions, people or evidence are connected.",
    )
    project_linked = SimpleNamespace(
        id="03 Projects/Project Linked.md",
        type="project",
        title="Project Linked",
        path="03 Projects/Project Linked.md",
    )
    project_orphan = SimpleNamespace(
        id="03 Projects/Project Orphan.md",
        type="project",
        title="Project Orphan",
        path="03 Projects/Project Orphan.md",
    )
    decision = SimpleNamespace(
        id="09 Governance/Decisions/Decision 1.md",
        type="decision",
        title="Decision 1",
        path="09 Governance/Decisions/Decision 1.md",
    )
    followup = SimpleNamespace(
        title="Objective A",
        path="09 Governance/Objectives/Objective A.md",
        summary="Review objective A checkpoint.",
        due_date="2026-05-20",
        priority="HIGH",
    )

    state = ExecutiveState(
        executive_health={"status": "AMBER", "score": 80, "failed": 4},
        priorities=[],
        objectives=[objective_a, objective_b],
        meetings=[],
        followups=SimpleNamespace(
            overdue=[followup],
            due_today=[],
            due_this_week=[],
            waiting_on_others=[],
            high_priority=[followup],
        ),
        open_loops=SimpleNamespace(critical_open_loops=[]),
        projects=[
            SimpleNamespace(path=project_linked.path, title=project_linked.title, status="SUPPORTED", recommendation="Project has supporting vault evidence."),
            SimpleNamespace(path=project_orphan.path, title=project_orphan.title, status="AT RISK", recommendation="Project has no graph linkage; review whether it is current, duplicated, or missing relationships."),
        ],
        suppliers=[],
        people=[],
        risks=[],
        recommendations=[],
        confidence="HIGH",
        engine_result={},
        vault={"decisions": {"top_decisions": [{"title": "Decision 1", "importance": 100, "projects": 1, "objectives": 1}]}},
        entities=[objective_a, objective_b, project_linked, project_orphan, decision],
        neighbours={
            objective_a.path: (project_linked.id, decision.id),
            project_linked.id: (objective_a.path, decision.id),
            decision.id: (objective_a.path, project_linked.id),
        },
    )

    report = build_objective_project_spine_from_state(state, today=date(2026, 7, 3))

    assert any(item.title == "Objective A" and "Project Linked" in item.detail for item in report.objective_to_project_traceability)
    assert any(item.title == "Project Orphan" for item in report.orphan_projects)
    assert any(item.title == "Objective B" for item in report.objectives_without_projects)
    assert any(item.title == "Objective A" and "Score" in item.detail for item in report.objective_health_scores)
    assert any(item.title == "Objective B" and "Cadence confidence: LOW" in item.detail for item in report.objective_review_cadence)


def test_build_objective_project_spine_generates_report():
    output = Path("output/Objective_Project_Spine.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_objective_project_spine.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Objective Project Spine" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
