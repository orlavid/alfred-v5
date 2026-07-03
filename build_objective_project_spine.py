#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.objectives.objective_project_spine import (
    build_objective_project_spine,
    render_objective_project_spine,
)

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_objective_project_spine(EVIDENCE)
    output = OUT / "Objective_Project_Spine.md"
    output.write_text(render_objective_project_spine(report))
    print(output)


if __name__ == "__main__":
    main()
