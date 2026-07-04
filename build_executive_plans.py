#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.planning.executive_planner import build_executive_plans, render_executive_plans

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_executive_plans(EVIDENCE)
    output = OUT / "Executive_Plans.md"
    output.write_text(render_executive_plans(report))
    print(output)


if __name__ == "__main__":
    main()
