#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from src.meeting.meeting_intelligence import MeetingIntelligence


ROOT = Path(__file__).parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python build_meeting_brief.py <meeting/person/company/project>")
        return 2

    query = " ".join(sys.argv[1:]).strip()
    engine = MeetingIntelligence(EVIDENCE)
    brief = engine.build(query)
    markdown = engine.render_markdown(brief)

    safe_name = "".join(
        character if character.isalnum() or character in ("-", "_") else "_"
        for character in query
    ).strip("_")
    output = OUT / f"Meeting_Brief_{safe_name}.md"
    output.write_text(markdown)

    print(output)
    return 0


if __name__ == "__main__":
