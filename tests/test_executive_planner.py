from datetime import date
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

from src.executive.knowledge_engine import ExecutiveState
from src.planning.executive_planner import build_executive_plans_from_state


def test_build_executive_plans_from_state_creates_draft_plans():
    objective = SimpleNamespace(
        id="09 Governance/Objectives/Objective A.md",
        type="objective",
        title="Objective A",
        path="09 Governance/Objectives/Objective A.md",
    )
    project = SimpleNamespace(
        id="03 Projects/Project Atlas.md",
        type="project",
        title="Project Atlas",
        path="03 Projects/Project Atlas.md",
        status="AT RISK",
        recommendation="Clarify scope and ownership.",
    )
    person = SimpleNamespace(
        id="02 People/Phillip.md",
        type="person",
        title="Phillip",
        path="02 People/Phillip.md",
    )
    decision = SimpleNamespace(
        id="04 Decisions/Decision 1.md",
        type="decision",
        title="Decision 1",
        path="04 Decisions/Decision 1.md",
    )
    state = ExecutiveState(
        objectives=(objective,),
        projects=(project,),
        people=(person,),
        entities=(objective, project, person, decision),
        neighbours={
            project.path: (objective.id, person.id, decision.id),
            objective.id: (project.path,),
            person.id: (project.path,),
            decision.id: (project.path,),
        },
        project_health={"at_risk": 1},
    )

    report = build_executive_plans_from_state(state, today=date(2026, 7, 4))

    assert len(report.plans) == 1
    plan = report.plans[0]
    assert plan.project_title == "Project Atlas"
    assert plan.status == "Draft"
    assert "Objective A" in plan.goal
    assert plan.suggested_owners == ("Phillip",)
    assert "Decision 1" in plan.dependencies
    assert plan.can_edit is True
    assert plan.can_approve is True
    assert plan.can_reject is True


def test_build_executive_plans_generates_output():
    output = Path("output/Executive_Plans.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_executive_plans.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()
    content = output.read_text()
    assert "# Executive Plans" in content
    assert "## Summary" in content
    assert "- Status: Draft" in content
