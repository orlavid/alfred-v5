from pathlib import Path
import json
import subprocess
import sys

from src.mining.alfred_archaeology import build_archaeology_report


def test_alfred_archaeology_classifies_executive_findings(tmp_path: Path):
    root = tmp_path / "legacy-alfred"
    root.mkdir()
    (root / "Objectives").mkdir()
    (root / "Objectives" / "2026 Objectives.md").write_text("# 2026 Objectives\nStrategic objective and governance checkpoint.\n")
    (root / "Projects").mkdir()
    (root / "Projects" / "Phoenix.md").write_text("# Project Phoenix\nProgramme initiative with vendor dependency and risk.\n")
    (root / "Governance.md").write_text("# Governance Board\nCommittee oversight and policy framework.\n")
    (root / "Ideas").mkdir()
    (root / "Ideas" / "Dashboard.md").write_text("# Dashboard Concepts\nExecutive KPI scorecard heatmap.\n")
    (root / "Archive").mkdir()
    (root / "Archive" / "Legacy Decisions.md").write_text("# Legacy Decisions\nArchived decision log.\n")
    (root / "logs").mkdir()
    (root / "logs" / "runtime.log").write_text("ignore me")

    report = build_archaeology_report(root)

    assert any(finding.section == "Objectives" for finding in report.findings)
    assert any(finding.section == "Projects" for finding in report.findings)
    assert any(finding.section == "Governance" for finding in report.findings)
    assert any(finding.classification == "Import" for finding in report.findings)
    assert any(finding.classification == "Review" for finding in report.findings)
    assert any(finding.classification == "Archive" for finding in report.findings)
    assert not any("runtime.log" in finding.source for finding in report.findings)


def test_build_archaeology_report_generates_outputs(tmp_path: Path):
    root = tmp_path / "legacy-alfred"
    root.mkdir()
    (root / "Objectives.md").write_text("# Objectives\nObjective and project coverage.\n")

    markdown_output = Path("output/Alfred_Archaeology_Report.md")
    json_output = Path("output/Alfred_Archaeology_Import_Candidates.json")
    if markdown_output.exists():
        markdown_output.unlink()
    if json_output.exists():
        json_output.unlink()

    result = subprocess.run(
        [sys.executable, "build_archaeology_report.py", "--source", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert markdown_output.exists()
    assert json_output.exists()
    content = markdown_output.read_text()
    assert "# Alfred Archaeology Report" in content
    assert "## Import Summary" in content
    payload = json.loads(json_output.read_text())
    assert "import_candidates" in payload
