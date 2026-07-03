#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from src.alfred.ask import ask_alfred, render_ask_alfred

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print('Usage: python build_ask_alfred.py "Your question"')
        return 1

    question = " ".join(args).strip()
    response = ask_alfred(question, EVIDENCE)
    rendered = render_ask_alfred(response)

    (OUT / "Ask_Alfred.md").write_text(rendered)
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
