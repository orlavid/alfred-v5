#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
from executive.parser import parse_services
from executive.health import platform_health
from executive.risks import build_risks
from executive.report import render

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

def read(rel: str, limit: int = 20000) -> str:
    path = EVIDENCE / rel
    if not path.exists():
        return "*Missing evidence.*"
    return path.read_text(errors="ignore")[:limit]


def main() -> None:
    services = parse_services(EVIDENCE)
    health = platform_health(services)
    risks = build_risks(services)
    output = OUT / "Executive_Review.md"
    review = render(health, risks)

    output.write_text(review)
    print(output)


if __name__ == "__main__":
    main()
