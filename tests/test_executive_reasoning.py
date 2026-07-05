from pathlib import Path
import subprocess
import sys

from src.executive.executive_reasoning import SECTION_HEADINGS


def test_build_executive_reasoning_generates_report():
    output = Path("output/Executive_Reasoning.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_executive_reasoning.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Executive Reasoning" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
    assert "## Top 10 Executive Actions" in content
    assert "- Priority:" in content or "_None found._" in content
    assert "- Action:" in content or "_None found._" in content
    assert "- Why it matters:" in content
    assert "- Supporting evidence:" in content
    assert "- Expected impact:" in content
    assert "- Confidence:" in content
