#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

STEPS = [
    ("Engineering Handbook", [sys.executable, "build_handbook.py"]),
    ("Architecture", [sys.executable, "build_architecture.py"]),
    ("Executive Review", [sys.executable, "build_executive_review.py"]),
    ("Meeting Intelligence", [sys.executable, "build_meeting_brief.py", "Barclays"]),
    ("Follow-up Intelligence", [sys.executable, "build_followups.py"]),
    ("Open Loop Intelligence", [sys.executable, "build_open_loops.py"]),
    ("Executive Intelligence", [sys.executable, "build_executive_intelligence.py"]),
    ("Executive Reasoning", [sys.executable, "build_executive_reasoning.py"]),
    ("Ask Alfred", [sys.executable, "build_ask_alfred.py", "What should I do today?"]),
    ("Daily Briefing", [sys.executable, "build_daily_brief.py"]),
    ("Knowledge Mining", [sys.executable, "build_knowledge_mining_report.py"]),
    ("Knowledge Housekeeping", [sys.executable, "build_knowledge_housekeeping.py"]),
]


def run_step(name: str, cmd: list[str]) -> None:
    print(f"\n{'=' * 60}")
    print(f"BUILD: {name}")
    print(f"{'=' * 60}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"\nFAILED: {name}")
        sys.exit(result.returncode)
    print(f"SUCCESS: {name}")


if __name__ == "__main__":
    for name, cmd in STEPS:
        run_step(name, cmd)

    print("\n" + "=" * 60)
    print("ALL BUILDS COMPLETED SUCCESSFULLY")
    print("=" * 60)
