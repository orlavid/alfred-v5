from pathlib import Path
import subprocess
import sys

from src.mining.knowledge_miner import build_knowledge_mining_report


def test_knowledge_miner_extracts_executive_artefacts(tmp_path: Path):
    root = tmp_path / "legacy"
    root.mkdir()
    (root / "Objectives.md").write_text("# Strategic Objectives\nTop objective for the year.\n")
    (root / "Projects").mkdir()
    (root / "Projects" / "Project Phoenix.md").write_text("# Project Phoenix\nKey project initiative.\n")
    (root / "Suppliers").mkdir()
    (root / "Suppliers" / "SoftCat.md").write_text("# SoftCat\nSupplier relationship and risk.\n")
    (root / "People").mkdir()
    (root / "People" / "Jane Doe.md").write_text("# Jane Doe\nStakeholder owner for governance.\n")
    (root / "Dashboard Ideas.md").write_text("# Dashboard Ideas\nKPI dashboard and executive scorecard.\n")
    (root / "logs").mkdir()
    (root / "logs" / "latest.log").write_text("technical noise")

    report = build_knowledge_mining_report(root)

    sections = {artefact.section for artefact in report.artefacts}
    assert "Objectives" in sections
    assert "Projects" in sections
    assert "Companies" in sections
    assert "People" in sections
    assert "Dashboard Ideas" in sections
    assert all("logs/latest.log" not in item for item in report.discarded_technical_debt)


def test_build_knowledge_mining_report_generates_output():
    output = Path("output/Knowledge_Mining_Report.md")
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [sys.executable, "build_knowledge_mining_report.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output.exists()
    content = output.read_text()
    assert "# Executive Knowledge Inventory" in content
    assert "## Import Summary" in content
