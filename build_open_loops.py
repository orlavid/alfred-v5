#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.executive.executive_state import build_executive_state
from src.openloops.open_loop_intelligence import render_open_loop_intelligence

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    # Deprecated direct retrieval path: open-loop output now renders from ExecutiveState.
    report = build_executive_state(EVIDENCE).open_loops
    output = OUT / "Open_Loop_Intelligence.md"
    output.write_text(render_open_loop_intelligence(report))
    print(output)


if __name__ == "__main__":
    main()
