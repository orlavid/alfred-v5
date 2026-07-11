#!/usr/bin/env python3

from __future__ import annotations

from src.operations.semantic_equivalence_validation import (
    build_semantic_equivalence_validation,
    write_semantic_equivalence_validation,
)


def main() -> int:
    report = build_semantic_equivalence_validation()
    markdown_path, json_path = write_semantic_equivalence_validation(report)
    print(markdown_path)
    print(json_path)
    return 0 if report.overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
