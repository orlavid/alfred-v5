from pathlib import Path

from src.api.dashboard_api import get_dashboard_home
from src.management.objectives import (
    accept_smart_proposal,
    add_management_note,
    add_milestone,
    create_smart_proposal,
    reject_smart_proposal,
    update_objective_fields,
)


def _seed_objective_vault(root: Path) -> Path:
    vault = root / "vault"
    (vault / "09 Governance" / "Objectives").mkdir(parents=True)
    (vault / "03 Projects").mkdir(parents=True)
    (vault / "09 Governance" / "Decisions").mkdir(parents=True)
    (vault / "08 Follow Ups").mkdir(parents=True)
    (vault / "07 Open Loops").mkdir(parents=True)
    (vault / "05 Meetings").mkdir(parents=True)
    (vault / "02 People").mkdir(parents=True)

    (vault / "09 Governance" / "Objectives" / "2026 Executive Objectives.md").write_text(
        "# 2026 Executive Objectives\n\n"
        "## Objectives\n\n"
        "- Operational Governance\n"
    )
    (vault / "09 Governance" / "Objectives" / "Operational Governance.md").write_text(
        "# Operational Governance\n"
        "Type: Objective\n"
        "Status: Supported\n"
        "Last Activity: 2026-07-01\n"
    )
    (vault / "03 Projects" / "Governance Programme.md").write_text(
        "# Governance Programme\n"
        "Status: Active\n"
        "Owner: Jane Smith\n"
        "[[Operational Governance]]\n"
    )
    (vault / "09 Governance" / "Decisions" / "Governance Approval.md").write_text(
        "# Governance Approval\n[[Operational Governance]]\n"
    )
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text(
        "# Follow Up Actions\n\n## Follow-Up Actions\n\n- Confirm governance checkpoint this week\n"
    )
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text(
        "# Open Loop Register\n\n## LOOP-001\nIssue: Governance decision pending\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\n"
    )
    (vault / "05 Meetings" / "Governance Review.md").write_text("# Governance Review\nAgenda for [[Operational Governance]].\n")
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\nOwner.\n")
    return vault


def test_objective_management_state_persists_into_dashboard_payload(tmp_path, monkeypatch):
    store_path = tmp_path / "data" / "objective_management_state.json"
    monkeypatch.setenv("ALFRED_OBJECTIVE_MANAGEMENT_STORE", str(store_path))
    vault = _seed_objective_vault(tmp_path)

    initial = get_dashboard_home(tmp_path / "evidence", vault_root=vault)
    objective_id = initial["objectives"]["items"][0]["objective_id"]

    update_objective_fields(
        objective_id,
        {
            "owner": "Phillip Doheny",
            "priority": "HIGH",
            "target_date": "2026-09-30",
            "success_measures": ["Board approvals on time", "Review cadence in place"],
        },
        reason="Objective ownership and target agreed.",
    )
    add_management_note(objective_id, "Confirmed ownership and target date with Phillip.", reason="Management check-in.")
    add_milestone(objective_id, title="Approve governance calendar", due_date="2026-07-31", reason="Immediate governance action.")

    payload = get_dashboard_home(tmp_path / "evidence", vault_root=vault)
    detail = payload["objectives"]["details"][objective_id]
    item = payload["objectives"]["items"][0]

    assert detail["owner"] == "Phillip Doheny"
    assert detail["priority"] == "HIGH"
    assert detail["target_date"] == "2026-09-30"
    assert detail["success_measures"] == ["Board approvals on time", "Review cadence in place"]
    assert detail["management_notes"][0]["text"] == "Confirmed ownership and target date with Phillip."
    assert detail["milestones"][0]["title"] == "Approve governance calendar"
    assert detail["audit_history"]
    assert item["owner"] == "Phillip Doheny"
    assert "Target date is not defined." not in detail["missing_information"]


def test_objective_smart_proposal_can_be_generated_accepted_and_rejected(tmp_path, monkeypatch):
    store_path = tmp_path / "data" / "objective_management_state.json"
    monkeypatch.setenv("ALFRED_OBJECTIVE_MANAGEMENT_STORE", str(store_path))
    vault = _seed_objective_vault(tmp_path)

    initial = get_dashboard_home(tmp_path / "evidence", vault_root=vault)
    objective_id = initial["objectives"]["items"][0]["objective_id"]
    detail = initial["objectives"]["details"][objective_id]

    create_smart_proposal(objective_id, detail, reason="Run SMART enrichment for governance objective.")
    proposal_payload = get_dashboard_home(tmp_path / "evidence", vault_root=vault)
    proposal = proposal_payload["objectives"]["details"][objective_id]["smart_enrichment_proposal"]

    assert proposal is not None
    assert proposal["status"] == "PENDING"

    accept_smart_proposal(objective_id, selected_fields=["next_review_date"], reason="Accept only review cadence.")
    accepted = get_dashboard_home(tmp_path / "evidence", vault_root=vault)
    accepted_detail = accepted["objectives"]["details"][objective_id]

    assert accepted_detail["smart_enrichment_proposal"]["status"] == "ACCEPTED"
    assert accepted_detail["next_review_date"] != "Not defined"

    create_smart_proposal(objective_id, accepted_detail, reason="Re-run enrichment.")
    reject_smart_proposal(objective_id, reason="Reject follow-on proposal.")
    rejected = get_dashboard_home(tmp_path / "evidence", vault_root=vault)

    assert rejected["objectives"]["details"][objective_id]["smart_enrichment_proposal"]["status"] == "REJECTED"
