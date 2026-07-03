import subprocess

def test_validator_usage():
    result = subprocess.run(
        ["python", "tools/patches/validate_patch.py"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Usage:" in result.stdout
