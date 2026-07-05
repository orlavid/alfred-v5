#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from src.executive.executive_state import build_executive_state
from src.meeting.meeting_intelligence import build_meeting_brief, render_meeting_brief

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.strip()).strip("_") or "Meeting"


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if args:
        subject = " ".join(args).strip()
    else:
        state = build_executive_state(EVIDENCE)
        subject = (state.meetings[0].subject if state.meetings else "").strip()
        if not subject:
            output = OUT / "Meeting_Brief_No_Evidence.md"
            output.write_text("# Meeting Brief\n\n## Meeting\n\n- Subject: No active meeting identified.\n\n## Executive Summary\n\n- No evidence found.\n")
            print(output)
            return 0

    brief = build_meeting_brief(subject)

    output = OUT / f"Meeting_Brief_{_safe_name(subject)}.md"
    output.write_text(render_meeting_brief(brief))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
