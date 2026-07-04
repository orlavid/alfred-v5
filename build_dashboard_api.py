#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import json

from src.api.dashboard_api import get_dashboard_home

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
PUBLIC = ROOT / "web" / "public" / "api"
OUT.mkdir(exist_ok=True)
PUBLIC.mkdir(parents=True, exist_ok=True)


def main() -> None:
    payload = get_dashboard_home()
    output = OUT / "Dashboard_Home.json"
    public_output = PUBLIC / "dashboard-home.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True))
    public_output.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(output)


if __name__ == "__main__":
    main()
