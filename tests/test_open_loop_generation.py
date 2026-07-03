from pathlib import Path
import subprocess
import sys

from src.openloops.open_loop_intelligence import SECTION_HEADINGS


def test_build_open_loops_generates_report():
    output = Path("output/Open_Loop_Intelligence.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_open_loops.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Open Loop Intelligence" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
