#!/usr/bin/env python3

from __future__ import annotations

from src.operations.environment_discovery import build_environment_inventory, write_environment_inventory


def main() -> None:
    inventory = build_environment_inventory()
    markdown_path, json_path = write_environment_inventory(inventory)
    print(markdown_path)
    print(json_path)


if __name__ == "__main__":
    main()
