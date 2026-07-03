#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.curation.knowledge_curator import build_knowledge_housekeeping, render_knowledge_housekeeping

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_knowledge_housekeeping(OUT)
    output = OUT / "Knowledge_Housekeeping_Report.md"
    output.write_text(render_knowledge_housekeeping(report))
    print(output)


if __name__ == "__main__":
    main()
