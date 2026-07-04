from pathlib import Path
import subprocess
import sys

from src.knowledge.executive_understanding import classify_executive_note


def test_classify_executive_note_uses_frontmatter_tags_and_language():
    text = """---
type: objective
aliases:
  - Strategic Goal
tags: [objective, board-pack]
---
# Revenue Expansion

Strategic objective for the quarter with [[Project Atlas]] and executive review cadence.
"""

    result = classify_executive_note(Path("09 Governance/Objectives/Revenue Expansion.md"), text)

    assert result.entity_type == "objective"
    assert result.confidence == "HIGH"
    assert "frontmatter" in result.reasons
    assert "tags" in result.reasons
    assert "Strategic Goal" in result.aliases


def test_build_executive_understanding_generates_output():
    output = Path("output/Executive_Understanding.md")
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [sys.executable, "build_executive_understanding.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output.exists()
    content = output.read_text()
    assert "# Executive Understanding" in content
    assert "## Recognised Entities" in content
