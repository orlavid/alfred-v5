#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from src.mining.alfred_archaeology import (
    DEFAULT_ARCHAEOLOGY_SOURCE,
    build_archaeology_report,
    render_archaeology_report,
    render_import_candidates_json,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_ARCHAEOLOGY_SOURCE))
    args = parser.parse_args(argv)

    report = build_archaeology_report(Path(args.source))
    markdown_output = OUT / "Alfred_Archaeology_Report.md"
    json_output = OUT / "Alfred_Archaeology_Import_Candidates.json"
    markdown_output.write_text(render_archaeology_report(report))
    json_output.write_text(render_import_candidates_json(report))
    print(markdown_output)
    print(json_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
