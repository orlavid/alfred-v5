from pathlib import Path
import subprocess
import sys

from src.daily.daily_brief import SECTION_HEADINGS


def test_build_daily_brief_generates_report():
    output = Path("output/Daily_Brief.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_daily_brief.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Good Morning Phillip" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
    assert "Confidence:" in content
