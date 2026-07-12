from pathlib import Path

from executive.knowledge.entity_contract import CanonicalExecutiveEntityContract
from executive.knowledge.projects import ProjectInsight
from src.api import dashboard_api
from src.api.dashboard_api import get_dashboard_home
from src.executive.executive_state import ExecutiveState
from src.management.projects import add_management_note, add_milestone, update_project_fields


def _seed_project_vault(root: Path) -> Path:
    vault = root / "vault"
    (vault / "03 Projects").mkdir(parents=True)
    (vault / "09 Governance" / "Objectives").mkdir(parents=True)
    (vault / "09 Governance" / "Decisions").mkdir(parents=True)
    (vault / "08 Follow Ups").mkdir(parents=True)
    (vault / "07 Open Loops").mkdir(parents=True)
    (vault / "05 Meetings").mkdir(parents=True)
    (vault / "02 People").mkdir(parents=True)

    (vault / "03 Projects" / "Project Phoenix.md").write_text(
        "# Project Phoenix\n"
        "Type: Project\n"
        "Status: Supported\n"
        "Owner: Jane Smith\n"
        "Last Activity: 2026-07-10\n"
        "[[Operational Governance]]\n"
    )
    (vault / "09 Governance" / "Objectives" / "2026 Executive Objectives.md").write_text(
        "# 2026 Executive Objectives\n\n"
        "## Objectives\n\n"
        "- Operational Governance\n"
    )
    (vault / "09 Governance" / "Objectives" / "Operational Governance.md").write_text("# Operational Governance\nType: Objective\n")
    (vault / "09 Governance" / "Decisions" / "Phoenix Approval.md").write_text("# Phoenix Approval\n[[Project Phoenix]]\n")
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text("# Follow Up Actions\n\n## Follow-Up Actions\n\n- Confirm Phoenix checkpoint this week\n")
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text("# Open Loop Register\n\n## LOOP-001\nIssue: Phoenix dependency pending\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\n")
    (vault / "05 Meetings" / "Phoenix Review.md").write_text("# Phoenix Review\nAgenda for [[Project Phoenix]].\n")
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\nOwner.\n")
    return vault


def test_project_management_state_persists_into_dashboard_payload(tmp_path, monkeypatch):
    store_path = tmp_path / "data" / "project_management_state.json"
    monkeypatch.setenv("ALFRED_PROJECT_MANAGEMENT_STORE", str(store_path))
    vault = _seed_project_vault(tmp_path)

    initial = get_dashboard_home(tmp_path / "evidence", vault_root=vault)
    project_id = initial["projects"]["items"][0]["project_id"]

    update_project_fields(
        project_id,
        {
            "owner": "Phillip Doheny",
            "priority": "HIGH",
            "target_date": "2026-09-30",
            "success_measures": ["Board approval achieved", "Delivery plan reviewed"],
        },
        reason="Project ownership and target agreed.",
    )
    add_management_note(project_id, "Confirmed ownership and target date with Phillip.", reason="Management check-in.")
    add_milestone(project_id, title="Approve project plan", due_date="2026-07-31", reason="Immediate project action.")

    payload = get_dashboard_home(tmp_path / "evidence", vault_root=vault)
    detail = payload["projects"]["details"][project_id]
    item = payload["projects"]["items"][0]

    assert detail["owner"] == "Phillip Doheny"
    assert detail["priority"] == "HIGH"
    assert detail["target_date"] == "2026-09-30"
    assert detail["success_measures"] == ["Board approval achieved", "Delivery plan reviewed"]
    assert detail["management_notes"][0]["text"] == "Confirmed ownership and target date with Phillip."
    assert detail["milestones"][0]["title"] == "Approve project plan"
    assert detail["audit_history"]
    assert item["owner"] == "Phillip Doheny"
    assert item["route"] == f"/projects/{project_id}"


def test_projects_page_preserves_full_project_collection(monkeypatch):
    canonical_entities = tuple(
        CanonicalExecutiveEntityContract(
            entity_id=f"project-{index}",
            entity_type="project",
            canonical_name=f"Project {index:02d}",
            aliases=(),
            owner=None,
            delegates=(),
            status="SUPPORTED",
            priority=None,
            risk_level=None,
            confidence="MEDIUM",
            created=None,
            last_activity="2026-07-10",
            due_date=None,
            review_date=None,
            related_objectives=(),
            related_projects=(),
            related_people=(),
            related_meetings=(),
            dependencies=(),
            evidence_paths=(f"03 Projects/Project {index:02d}.md",),
            evidence_count=1,
            supporting_notes=(),
            missing_fields=(),
            provenance={},
            primary_path=f"03 Projects/Project {index:02d}.md",
        )
        for index in range(1, 15)
    )
    projects = tuple(
        ProjectInsight(
            title=f"Project {index:02d}",
            path=f"03 Projects/Project {index:02d}.md",
            linked_entities=3,
            status="SUPPORTED",
            recommendation="Project has supporting vault evidence.",
        )
        for index in range(1, 15)
    )
    state = ExecutiveState(
        canonical_entities=canonical_entities,
        projects=projects,
        project_health={"total": 14, "supported": 14, "at_risk": 0, "watch": 0},
        decisions=(),
        meetings=(),
        people=(),
        companies=(),
        work_items=(),
        entities=(),
        neighbours={},
    )

    payload = dashboard_api._build_projects_page(state)

    assert len(payload["items"]) == 14
    assert payload["items"][0]["route"].startswith("/projects/")
