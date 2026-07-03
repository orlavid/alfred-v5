#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from src.meeting.meeting_intelligence import build_meeting_brief, render_meeting_brief

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.strip()).strip("_") or "Meeting"


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: python build_meeting_brief.py <Meeting Subject>")
        return 1

    subject = " ".join(args).strip()
    brief = build_meeting_brief(subject)

    output = OUT / f"Meeting_Brief_{_safe_name(subject)}.md"
    output.write_text(render_meeting_brief(brief))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
