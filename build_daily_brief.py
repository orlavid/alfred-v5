#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.daily.daily_brief import build_daily_brief, render_daily_brief

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    brief = build_daily_brief(EVIDENCE)
    output = OUT / "Daily_Brief.md"
    output.write_text(render_daily_brief(brief))
    print(output)


if __name__ == "__main__":
    main()
