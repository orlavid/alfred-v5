#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.board.board_intelligence import build_board_intelligence, render_board_intelligence

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_board_intelligence(EVIDENCE)
    output = OUT / "Board_Intelligence.md"
    output.write_text(render_board_intelligence(report))
    print(output)


if __name__ == "__main__":
    main()
