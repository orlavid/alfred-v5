#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.executive.executive_reasoning import build_executive_reasoning, render_executive_reasoning

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_executive_reasoning(EVIDENCE)
    output = OUT / "Executive_Reasoning.md"
    output.write_text(render_executive_reasoning(report))
    print(output)


if __name__ == "__main__":
    main()
