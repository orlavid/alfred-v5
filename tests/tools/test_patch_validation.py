import subprocess

def run(*args):
    return subprocess.run(args, capture_output=True, text=True)

def test_validator_usage():
    result = run(
        "python",
        "tools/patches/validate_patch.py",
    )

    assert result.returncode == 1
    assert "Usage:" in result.stdout

def test_build_pipeline():
    result = run(
        "python",
        "build_everything.py",
    )

    assert result.returncode == 0
