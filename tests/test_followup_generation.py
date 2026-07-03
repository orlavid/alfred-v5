from pathlib import Path
import subprocess
import sys

from src.followups.followup_intelligence import SECTION_HEADINGS


def test_build_followups_generates_report():
    output = Path("output/Followup_Intelligence.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_followups.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Follow-up Intelligence" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
