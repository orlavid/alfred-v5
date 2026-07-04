#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.knowledge.executive_knowledge_builder import (
    DEFAULT_EVIDENCE_ROOT,
    build_executive_knowledge,
    render_executive_knowledge,
    render_executive_knowledge_json,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_executive_knowledge(DEFAULT_EVIDENCE_ROOT)
    markdown_output = OUT / "Executive_Knowledge.md"
    json_output = OUT / "Executive_Knowledge.json"
    markdown_output.write_text(render_executive_knowledge(report))
    json_output.write_text(render_executive_knowledge_json(report))
    print(markdown_output)
    print(json_output)


if __name__ == "__main__":
    main()
