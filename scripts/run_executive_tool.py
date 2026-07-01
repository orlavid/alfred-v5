#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def run(cmd):
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)

def main():
    print("== Alfred Executive Tool ==")
    print("1. Build Executive Review")
    print("2. Build Policy-Aware Preview Report")
    print("3. Build Both")
    choice = input("Choose [1/2/3]: ").strip() or "3"

    if choice == "1":
        run([sys.executable, "build_executive_review.py"])
        print("\nDone: output/Executive_Review.md")
    elif choice == "2":
        run([sys.executable, "scripts/render_policy_aware_preview_report.py"])
        print("\nDone: output/policy_aware_preview_report.md")
    elif choice == "3":
        run([sys.executable, "build_executive_review.py"])
        run([sys.executable, "scripts/render_policy_aware_preview_report.py"])
        print("\nDone:")
        print(" - output/Executive_Review.md")
        print(" - output/policy_aware_preview_report.md")
    else:
        print("Invalid choice")
        sys.exit(1)

if __name__ == "__main__":
    main()
