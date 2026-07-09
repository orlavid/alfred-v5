#!/usr/bin/env python3

from __future__ import annotations

from src.operations.executive_intelligence_validation import (
    build_executive_intelligence_validation,
    write_executive_intelligence_validation,
)


def main() -> int:
    report = build_executive_intelligence_validation()
    markdown_path, json_path = write_executive_intelligence_validation(report)
    print(markdown_path)
    print(json_path)
    if report.first_behavioural_issue:
        print(report.first_behavioural_issue)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
