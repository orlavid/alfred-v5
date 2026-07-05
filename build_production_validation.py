#!/usr/bin/env python3

from __future__ import annotations

from src.operations.production_validation import build_production_validation, write_production_validation


def main() -> int:
    report = build_production_validation()
    output = write_production_validation(report)
    print(output)
    return 0 if report.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
