#!/usr/bin/env python3

from src.operations.doctor import build_operational_readiness, write_operational_readiness


def main() -> None:
    report = build_operational_readiness()
    markdown_path, json_path = write_operational_readiness(report)
    print(markdown_path)
    print(json_path)


if __name__ == "__main__":
    main()
