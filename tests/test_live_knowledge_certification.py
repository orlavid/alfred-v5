from pathlib import Path
import subprocess
import sys

from src.pipeline.live_knowledge_certification import build_live_knowledge_certification


def test_build_live_knowledge_certification_passes_with_live_vault(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
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
    (vault / "04 Companies" / "Barclays.md").write_text("# Barclays\nSupplier and company for [[Project Phoenix]].\n")
    (vault / "04 Decisions" / "Decision 1.md").write_text("# Decision 1\nApproval for [[Project Phoenix]].\n")
    (vault / "05 Meetings" / "Barclays Meeting.md").write_text("# Barclays Meeting\nAgenda for Barclays and [[Jane Smith]].\n")
    (vault / "06 Risks" / "Risk Register.md").write_text("# Risk Register\nRisk escalation linked to [[Project Phoenix]].\n")
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text(
        "## LOOP-1\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\nIssue: Await approval for Project Phoenix\n"
    )
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text(
        "## Follow-Up Actions\n- Follow up with Barclays today on Project Phoenix.\n"
    )
    (vault / "01 Daily Logs" / "2026-07-04 Daily.md").write_text("# 2026-07-04 Daily\nReviewed [[Project Phoenix]].\n")
    (vault / "10 Briefings" / "Weekly Executive Briefing.md").write_text(
        "# Weekly Executive Briefing\nExecutive briefing for [[Project Phoenix]].\n"
    )

    monkeypatch.setenv("ALFRED_LIVE_VAULT_PATH", str(vault))

    report = build_live_knowledge_certification(Path("evidence/alfred-inventory"))

    assert report.status in {"PASS", "WARNING"}
    assert report.source_mode == "live_vault"
    assert report.metrics["Objectives discovered"] >= 1
    assert report.metrics["Projects discovered"] >= 1
    assert report.metrics["People discovered"] >= 1
    assert report.metrics["Companies discovered"] >= 1
    assert report.metrics["Meetings discovered"] >= 1
    assert report.metrics["Daily Logs discovered"] >= 1
    assert report.metrics["Decisions discovered"] >= 1
    assert report.metrics["Risks discovered"] >= 1
    assert report.metrics["Open Loops discovered"] >= 1
    assert report.metrics["Follow-ups discovered"] >= 1
    assert report.metrics["Executive Briefings discovered"] >= 1
    assert report.metrics["ExecutiveState generated"] is True
    assert report.metrics["Daily Brief generated"] is True
    assert report.metrics["Dashboard API generated"] is True


def test_build_live_knowledge_certification_generates_report():
    output = Path("output/LIVE_KNOWLEDGE_CERTIFICATION.md")
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [sys.executable, "build_live_knowledge_certification.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode in {0, 1}
    assert output.exists()
    content = output.read_text()
    assert "# Live Knowledge Certification" in content
    assert "## Certification Summary" in content
