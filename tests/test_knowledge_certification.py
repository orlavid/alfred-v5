from pathlib import Path
import subprocess
import sys

from src.operations.knowledge_certification import build_knowledge_certification


def test_knowledge_certification_passes_with_live_vault_evidence(tmp_path):
    vault = _build_live_vault(tmp_path / "vault", waiting_open_loop=True)

    report = build_knowledge_certification(vault_root=vault)
    statuses = {check.name: check.status for check in report.checks}

    assert report.overall_status == "GREEN"
    assert report.markdown_files_processed >= 11
    assert statuses["ExecutiveState live-vault population"] == "PASS"
    assert statuses["Objectives evidence coverage"] == "PASS"
    assert statuses["Projects evidence coverage"] == "PASS"
    assert statuses["Follow-up evidence coverage"] == "PASS"
    assert statuses["Open-loop evidence coverage"] == "PASS"
    assert statuses["Daily Brief evidence coverage"] == "PASS"


def test_knowledge_certification_fails_when_vault_is_missing(tmp_path):
    report = build_knowledge_certification(vault_root=tmp_path / "missing-vault")

    assert report.overall_status == "RED"
    assert report.checks[0].name == "Live vault accessibility"
    assert report.checks[0].status == "FAIL"


def test_build_knowledge_certification_generates_reports():
    markdown_output = Path("output/Knowledge_Certification.md")
    json_output = Path("output/Knowledge_Certification.json")
    if markdown_output.exists():
        markdown_output.unlink()
    if json_output.exists():
        json_output.unlink()

    result = subprocess.run(
        [sys.executable, "build_knowledge_certification.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert markdown_output.exists()
    assert json_output.exists()
    assert "# Knowledge Certification" in markdown_output.read_text()


def _build_live_vault(vault: Path, *, waiting_open_loop: bool) -> Path:
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
        "# Project Phoenix\nProgramme initiative for [[Objective Alpha]] with owner [[Jane Smith]].\n"
    )
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\nOwner for [[Project Phoenix]].\n")
    (vault / "04 Companies" / "Acme Capital.md").write_text("# Acme Capital\nSupplier and company for [[Project Phoenix]].\n")
    (vault / "04 Decisions" / "Decision 1.md").write_text("# Decision 1\nApproval for [[Project Phoenix]].\n")
    (vault / "05 Meetings" / "Project Phoenix Review.md").write_text("# Project Phoenix Review\nAgenda for Acme Capital and [[Jane Smith]].\n")
    (vault / "06 Risks" / "Risk Register.md").write_text("# Risk Register\nRisk escalation linked to [[Project Phoenix]].\n")
    issue = "Waiting for approval on Project Phoenix" if waiting_open_loop else "Await approval for Project Phoenix"
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text(
        f"## LOOP-1\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\nIssue: {issue}\n"
    )
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text(
        "## Follow-Up Actions\n- Follow up with Acme Capital today on Project Phoenix.\n"
    )
    (vault / "01 Daily Logs" / "2026-07-04 Daily.md").write_text("# 2026-07-04 Daily\nReviewed [[Project Phoenix]].\n")
    (vault / "10 Briefings" / "Weekly Executive Briefing.md").write_text(
        "# Weekly Executive Briefing\nExecutive briefing for [[Project Phoenix]].\n"
    )
    return vault
