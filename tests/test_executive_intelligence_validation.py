from pathlib import Path
import subprocess
import sys

from src.operations.executive_intelligence_validation import (
    build_executive_intelligence_validation,
)


def test_executive_intelligence_validation_passes_on_representative_vault(tmp_path: Path):
    vault = _build_live_vault(tmp_path / "vault")

    report = build_executive_intelligence_validation(vault_root=vault)

    assert report.overall_status == "GREEN"
    assert report.metrics.scenarios_total == 9
    assert report.metrics.scenarios_passed == report.metrics.scenarios_total
    assert report.metrics.criteria_total >= 20
    assert report.first_behavioural_issue is None


def test_executive_intelligence_validation_reports_first_failure(tmp_path: Path):
    vault = _build_live_vault(tmp_path / "vault")

    report = build_executive_intelligence_validation(vault_root=vault, meeting_subject="Project Phoenix Review")

    assert report.overall_status == "GREEN"
    assert report.first_behavioural_issue is None
    statuses = {scenario.scenario_id: scenario.status for scenario in report.scenarios}
    assert all(status == "PASS" for status in statuses.values())


def test_supplier_entities_survive_into_behavioural_state(tmp_path: Path):
    from src.executive.executive_state import build_executive_state

    vault = _build_live_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")

    assert any(item.title == "Acme Capital" for item in state.companies)
    assert any(item.title == "Acme Capital" and item.is_supplier for item in state.suppliers)


def test_build_executive_intelligence_validation_generates_reports():
    markdown_output = Path("output/Executive_Intelligence_Validation.md")
    json_output = Path("output/Executive_Intelligence_Validation.json")
    if markdown_output.exists():
        markdown_output.unlink()
    if json_output.exists():
        json_output.unlink()

    result = subprocess.run(
        [sys.executable, "build_executive_intelligence_validation.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert markdown_output.exists()
    assert json_output.exists()
    assert "# Executive Intelligence Validation" in markdown_output.read_text()


def _build_live_vault(vault: Path) -> Path:
    (vault / "01 Daily Logs").mkdir(parents=True)
    (vault / "02 People").mkdir(parents=True)
    (vault / "03 Projects").mkdir(parents=True)
    (vault / "04 Companies").mkdir(parents=True)
    (vault / "04 Decisions").mkdir(parents=True)
    (vault / "05 Meetings").mkdir(parents=True)
    (vault / "06 Risks").mkdir(parents=True)
    (vault / "07 Open Loops").mkdir(parents=True)
    (vault / "08 Follow Ups").mkdir(parents=True)
    (vault / "09 Objectives").mkdir(parents=True)
    (vault / "10 Briefings").mkdir(parents=True)

    (vault / "09 Objectives" / "Objective Alpha.md").write_text(
        "# Objective Alpha\nStrategic objective linked to [[Project Phoenix]].\n"
    )
    (vault / "03 Projects" / "Project Phoenix.md").write_text(
        "# Project Phoenix\nProgramme initiative for [[Objective Alpha]] with owner [[Jane Smith]] and supplier [[Acme Capital]].\n"
    )
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\nOwner for [[Project Phoenix]].\n")
    (vault / "04 Companies" / "Acme Capital.md").write_text("# Acme Capital\nSupplier and company for [[Project Phoenix]].\n")
    (vault / "04 Decisions" / "Decision 1.md").write_text("# Decision 1\nApproval for [[Project Phoenix]].\n")
    (vault / "05 Meetings" / "Project Phoenix Review.md").write_text("# Project Phoenix Review\nAgenda for [[Project Phoenix]] and [[Acme Capital]].\n")
    (vault / "06 Risks" / "Risk Register.md").write_text("# Risk Register\nRisk escalation linked to [[Project Phoenix]].\n")
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text(
        "## LOOP-1\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\nIssue: Await approval on Project Phoenix.\n"
    )
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text(
        "## Follow-Up Actions\n- Follow up with Acme Capital today on Project Phoenix.\n"
    )
    (vault / "01 Daily Logs" / "2026-07-04 Daily.md").write_text(
        "# 2026-07-04 Daily\nReviewed [[Project Phoenix]] and escalated supplier follow-up.\n"
    )
    (vault / "10 Briefings" / "Weekly Executive Briefing.md").write_text(
        "# Weekly Executive Briefing\nExecutive briefing for [[Project Phoenix]].\n"
    )
    return vault
