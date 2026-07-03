from pathlib import Path
import subprocess
import sys


def test_build_ask_alfred_outputs_response():
    output = Path("output/Ask_Alfred.md")
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [sys.executable, "build_ask_alfred.py", "What should I do today?"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Executive Answer" in result.stdout
    assert "Supporting Evidence" in result.stdout
    assert "Confidence" in result.stdout
    assert "Recommended Next Actions" in result.stdout
    assert output.exists()

    content = output.read_text()
    assert "Executive Answer" in content
    assert "Supporting Evidence" in content
    assert "Confidence" in content
    assert "Recommended Next Actions" in content
