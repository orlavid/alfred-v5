from pathlib import Path
import subprocess
import sys

from src.executive.executive_intelligence import SECTION_HEADINGS


def test_build_executive_intelligence_generates_report():
    output = Path("output/Executive_Intelligence.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_executive_intelligence.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Executive Intelligence" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
