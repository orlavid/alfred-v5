from pathlib import Path

from src.api.dashboard_api import get_dashboard_home


def _seed_decision_vault(root: Path) -> Path:
    vault = root / "vault"
    (vault / "04 Decisions").mkdir(parents=True)
    (vault / "03 Projects").mkdir(parents=True)
    (vault / "09 Governance" / "Objectives").mkdir(parents=True)
    (vault / "02 People").mkdir(parents=True)

    (vault / "04 Decisions" / "Decision 1.md").write_text(
        "# Decision 1\n"
        "Status: OPEN\n"
        "Owner: Jane Smith\n"
        "Created: 2026-07-10\n"
        "Approval for [[Project Phoenix]] and [[Operational Governance]].\n"
    )
    (vault / "03 Projects" / "Project Phoenix.md").write_text("# Project Phoenix\n[[Decision 1]]\n")
    (vault / "09 Governance" / "Objectives" / "2026 Executive Objectives.md").write_text(
        "# 2026 Executive Objectives\n\n## Objectives\n\n- Operational Governance\n"
    )
    (vault / "09 Governance" / "Objectives" / "Operational Governance.md").write_text("# Operational Governance\n[[Decision 1]]\n")
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\n")
    return vault


def test_decision_payload_includes_register_and_detail(tmp_path):
    vault = _seed_decision_vault(tmp_path)

    payload = get_dashboard_home(tmp_path / "evidence", vault_root=vault)

    assert payload["decisions"]["counts"]["total"] == 1
    assert len(payload["decisions"]["items"]) == 1
    item = payload["decisions"]["items"][0]
    detail = payload["decisions"]["details"][item["decision_id"]]

    assert item["title"] == "Decision 1"
    assert item["route"].startswith("/decisions/")
    assert detail["owner"] == "Jane Smith"
    assert detail["current_status"] == "OPEN"
    assert detail["decision_date"] == "2026-07-10"
    assert detail["evidence_sources"]
    assert detail["provenance"]["decision"]


def test_decision_payload_preserves_full_collection(tmp_path):
    vault = tmp_path / "vault"
    (vault / "04 Decisions").mkdir(parents=True)
    for index in range(1, 7):
        (vault / "04 Decisions" / f"Decision {index}.md").write_text(
            f"# Decision {index}\nStatus: OPEN\nApprove item {index}.\n"
        )

    payload = get_dashboard_home(tmp_path / "evidence", vault_root=vault)

    assert payload["decisions"]["counts"]["total"] == len(payload["decisions"]["items"])
    assert len(payload["decisions"]["items"]) == 6


def test_decision_payload_excludes_non_register_noise(tmp_path):
    vault = tmp_path / "vault"
    (vault / "04 Decisions").mkdir(parents=True)
    (vault / "01 Daily Logs").mkdir(parents=True)
    (vault / "10 Briefings").mkdir(parents=True)

    (vault / "04 Decisions" / "Decision 1.md").write_text("# Decision 1\nStatus: OPEN\nApprove supplier change.\n")
    (vault / "04 Decisions" / "Decision Template.md").write_text("# Decision Template\nStatus: DRAFT\n")
    (vault / "01 Daily Logs" / "2026-07-12.md").write_text("# 2026-07-12\nDecision: revisit the forecast model.\n")
    (vault / "10 Briefings" / "Decision Summary.md").write_text("# Decision Summary\nA generated summary.\n")

    payload = get_dashboard_home(tmp_path / "evidence", vault_root=vault)

    assert payload["decisions"]["counts"]["source_notes"] == 1
    assert [item["title"] for item in payload["decisions"]["items"]] == ["Decision 1"]
    assert all(item["source_path"].startswith("04 Decisions/") for item in payload["decisions"]["items"])
