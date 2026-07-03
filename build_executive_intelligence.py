#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.executive.executive_intelligence import build_executive_intelligence, render_executive_intelligence

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_executive_intelligence(EVIDENCE)
    output = OUT / "Executive_Intelligence.md"
    output.write_text(render_executive_intelligence(report))
    print(output)


if __name__ == "__main__":
    main()
