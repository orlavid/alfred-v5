#!/usr/bin/env python3

from __future__ import annotations

import sys

from src.pipeline.live_knowledge_certification import (
    build_live_knowledge_certification,
    write_live_knowledge_certification,
)


def main() -> int:
    report = build_live_knowledge_certification()
    output = write_live_knowledge_certification(report)
    print(output)
    if report.status == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
