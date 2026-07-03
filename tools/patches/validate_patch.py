#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

def run(cmd):
    result = subprocess.run(cmd, text=True, capture_output=True)
    return result.returncode, result.stdout, result.stderr

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_patch.py <patch>")
        sys.exit(1)

    patch = Path(sys.argv[1])

    if not patch.exists():
        print(f"FAIL: {patch} not found")
        sys.exit(1)

    rc, out, err = run(["git", "apply", "--check", str(patch)])

    if rc != 0:
        print("FAIL")
        print(err.strip())
        sys.exit(rc)

    print("PASS")
    print("Patch applies cleanly.")

if __name__ == "__main__":
    main()
