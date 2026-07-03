#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from src.mining.knowledge_miner import (
    DEFAULT_LEGACY_ROOT,
    build_knowledge_mining_report,
    render_knowledge_mining_report,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    legacy_root = Path(args[0]) if args else DEFAULT_LEGACY_ROOT

    report = build_knowledge_mining_report(legacy_root)
    output = OUT / "Knowledge_Mining_Report.md"
    output.write_text(render_knowledge_mining_report(report))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
