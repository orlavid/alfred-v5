from pathlib import Path
import json
import subprocess
import sys

from src.board.board_registry import SECTION_HEADINGS, build_board_governance


def test_build_board_governance_returns_expected_registry():
    report = build_board_governance()

    assert len(report.board_members) == 11
    assert report.board_members[0].name == "Phillip"
    assert report.board_members[0].role == "Chairman"
    assert report.board_members[-1].name == "Victoria"
    assert all(member.portrait_placeholder.startswith("PORTRAIT_PENDING_") for member in report.board_members)
    assert all(member.status == "ACTIVE" for member in report.board_members)


def test_build_board_governance_generates_outputs():
    markdown_output = Path("output/Board_Governance.md")
    json_output = Path("output/Board_Registry.json")
    if markdown_output.exists():
        markdown_output.unlink()
    if json_output.exists():
        json_output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_board_governance.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert markdown_output.exists()
    assert json_output.exists()

    content = markdown_output.read_text()
    assert "# Board Governance" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content

    payload = json.loads(json_output.read_text())
    assert len(payload["board_members"]) == 11
    assert payload["board_members"][0]["name"] == "Phillip"
    assert payload["board_members"][1]["name"] == "Alfred"
