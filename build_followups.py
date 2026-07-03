#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.followups.followup_intelligence import build_followup_intelligence, render_followup_intelligence

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_followup_intelligence()
    output = OUT / "Followup_Intelligence.md"
    output.write_text(render_followup_intelligence(report))
    print(output)


if __name__ == "__main__":
    main()
