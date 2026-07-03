from pathlib import Path
import subprocess
import sys

from src.meeting.meeting_intelligence import SECTION_HEADINGS


def test_build_meeting_brief_generates_barclays_report():
    output = Path("output/Meeting_Brief_Barclays.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_meeting_brief.py", "Barclays"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
