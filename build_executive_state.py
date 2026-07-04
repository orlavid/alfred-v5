#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.executive.executive_state import build_executive_state, render_executive_state_summary

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    state = build_executive_state(EVIDENCE)
    output = OUT / "ExecutiveState_Summary.md"
    output.write_text(render_executive_state_summary(state))
    print(output)


if __name__ == "__main__":
    main()
