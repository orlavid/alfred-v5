#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.openloops.open_loop_intelligence import build_open_loop_intelligence, render_open_loop_intelligence

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_open_loop_intelligence()
    output = OUT / "Open_Loop_Intelligence.md"
    output.write_text(render_open_loop_intelligence(report))
    print(output)


if __name__ == "__main__":
    main()
