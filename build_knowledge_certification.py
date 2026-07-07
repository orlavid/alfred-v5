#!/usr/bin/env python3

from __future__ import annotations

from src.operations.knowledge_certification import (
    build_knowledge_certification,
    write_knowledge_certification,
)


def main() -> int:
    report = build_knowledge_certification()
    markdown_path, json_path = write_knowledge_certification(report)
    print(markdown_path)
    print(json_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
