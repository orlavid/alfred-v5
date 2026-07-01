#!/usr/bin/env python3

from pathlib import Path

from executive.engine import execute
from executive.report import render

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    result = execute(EVIDENCE)

    output = OUT / "Executive_Review.md"
    output.write_text(render(result))
    print(output)


if __name__ == "__main__":
    main()
