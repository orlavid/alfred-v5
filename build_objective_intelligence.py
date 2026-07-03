#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.objectives.objective_intelligence import build_objective_intelligence, render_objective_intelligence

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_objective_intelligence(EVIDENCE)
    output = OUT / "Objective_Intelligence.md"
    output.write_text(render_objective_intelligence(report))
    print(output)


if __name__ == "__main__":
    main()
