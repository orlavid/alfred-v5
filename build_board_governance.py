#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.board.board_registry import (
    build_board_governance,
    render_board_governance,
    render_board_registry_json,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_board_governance()
    markdown_output = OUT / "Board_Governance.md"
    json_output = OUT / "Board_Registry.json"
    markdown_output.write_text(render_board_governance(report))
    json_output.write_text(render_board_registry_json(report))
    print(markdown_output)
    print(json_output)


if __name__ == "__main__":
    main()
