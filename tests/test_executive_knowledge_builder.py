from datetime import date
from pathlib import Path
import json
import subprocess
import sys

from src.knowledge.executive_knowledge_builder import (
    build_executive_knowledge,
    render_executive_knowledge_json,
)


def test_executive_knowledge_builder_uses_evidence_inventory_when_vault_missing(tmp_path: Path):
    evidence_root = tmp_path / "evidence"
    evidence_root.mkdir()
    (evidence_root / "Objectives.md").write_text("# Objectives\nStrategic objective with [[Project Alpha]].\n")
    (evidence_root / "Project Alpha.md").write_text("# Project Alpha\nProgramme initiative linked to supplier and risk.\n")
    (evidence_root / "Risk Register.md").write_text("# Risk Register\nRisk escalation and policy exception.\n")
    (evidence_root / "Weekly Board Briefing.md").write_text("# Weekly Board Briefing\nExecutive briefing for the week.\n")

    report = build_executive_knowledge(evidence_root, vault_root=tmp_path / "missing-vault", today=date(2026, 7, 4))

    assert report.source_mode == "evidence_inventory"
    assert report.entity_inventory["objective"] >= 1
    assert report.entity_inventory["project"] >= 1
    assert report.entity_inventory["risk"] >= 1
    assert report.entity_inventory["executive_briefing"] >= 1
    assert report.relationship_graph
    payload = json.loads(render_executive_knowledge_json(report))
    assert "entities" in payload
    assert "relationship_graph" in payload


def test_build_executive_knowledge_generates_outputs():
    markdown_output = Path("output/Executive_Knowledge.md")
    json_output = Path("output/Executive_Knowledge.json")
    if markdown_output.exists():
        markdown_output.unlink()
    if json_output.exists():
        json_output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_executive_knowledge.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert markdown_output.exists()
    assert json_output.exists()
    content = markdown_output.read_text()
    assert "# Executive Knowledge Builder" in content
    assert "## Relationship Graph" in content
    payload = json.loads(json_output.read_text())
    assert "entity_inventory" in payload
    assert "recommended_actions" in payload
