#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.executive.executive_state import build_executive_state
from src.followups.followup_intelligence import render_followup_intelligence

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    # Deprecated direct retrieval path: follow-up output now renders from ExecutiveState.
    report = build_executive_state(EVIDENCE).followups
    output = OUT / "Followup_Intelligence.md"
    output.write_text(render_followup_intelligence(report))
    print(output)


if __name__ == "__main__":
    main()
