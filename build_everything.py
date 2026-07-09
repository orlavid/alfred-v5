#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

STEPS = [
    ("Engineering Handbook", [sys.executable, "build_handbook.py"]),
    ("Architecture", [sys.executable, "build_architecture.py"]),
    ("Executive Knowledge Builder", [sys.executable, "build_executive_knowledge.py"]),
    ("Knowledge Graph", [sys.executable, "build_knowledge_graph.py"]),
    ("Executive Review", [sys.executable, "build_executive_review.py"]),
    ("Meeting Intelligence", [sys.executable, "build_meeting_brief.py"]),
    ("Follow-up Intelligence", [sys.executable, "build_followups.py"]),
    ("Open Loop Intelligence", [sys.executable, "build_open_loops.py"]),
    ("Executive Intelligence", [sys.executable, "build_executive_intelligence.py"]),
    ("Objective Intelligence", [sys.executable, "build_objective_intelligence.py"]),
    ("Objective Project Spine", [sys.executable, "build_objective_project_spine.py"]),
    ("Executive Reasoning", [sys.executable, "build_executive_reasoning.py"]),
    ("Ask Alfred", [sys.executable, "build_ask_alfred.py", "What should I do today?"]),
    ("Daily Briefing", [sys.executable, "build_daily_brief.py"]),
    ("Dashboard API", [sys.executable, "build_dashboard_api.py"]),
    ("Executive Pipeline", [sys.executable, "build_executive_pipeline.py"]),
    ("Live Knowledge Certification", [sys.executable, "build_live_knowledge_certification.py"]),
    ("Knowledge Certification", [sys.executable, "build_knowledge_certification.py"]),
    ("Executive Intelligence Validation", [sys.executable, "build_executive_intelligence_validation.py"]),
    ("Knowledge Mining", [sys.executable, "build_knowledge_mining_report.py"]),
    ("Alfred Archaeology", [sys.executable, "build_archaeology_report.py"]),
    ("Knowledge Housekeeping", [sys.executable, "build_knowledge_housekeeping.py"]),
    ("Board Governance", [sys.executable, "build_board_governance.py"]),
    ("Executive State", [sys.executable, "build_executive_state.py"]),
    ("Environment Inventory", [sys.executable, "build_environment_inventory.py"]),
    ("Operational Readiness", [sys.executable, "build_operational_readiness.py"]),
    ("Production Validation", [sys.executable, "build_production_validation.py"]),
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
