#!/usr/bin/env python3

from pathlib import Path

from src.operations.runtime_certification import (
    build_runtime_certification,
    write_runtime_certification,
)


def main() -> None:
    report = build_runtime_certification()
    output_dir = Path("/opt/alfred/app/output") if Path("/opt/alfred/app").exists() else Path("output")
    markdown_path, json_path = write_runtime_certification(report, output_dir)
    print(markdown_path)
    print(json_path)


if __name__ == "__main__":
    main()
