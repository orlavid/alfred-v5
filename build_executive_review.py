#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

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
    output = OUT / "Executive_Review.md"
    review = (
        "# Executive Review\n\n"
        f"Generated: {datetime.now().isoformat()}\n\n"
        "## Executive Summary\n\n"
        "First Executive Review prototype generated from Recovery Point Alpha evidence.\n\n"
        "## Platform Evidence\n\n"
        "### Services\n\n"
        "```text\n" + read("system/services.txt") + "\n```\n\n"
        "### Telegram\n\n"
        "```text\n" + read("telegram/status.txt") + "\n```\n\n"
        "### Obsidian\n\n"
        "```text\n" + read("obsidian/vault_summary.txt") + "\n```\n\n"
        "### LlamaIndex\n\n"
        "```text\n" + read("llamaindex/index_summary.txt") + "\n```\n\n"
        "## Next Improvement\n\n"
        "Replace raw evidence with structured executive intelligence.\n"
    )

    output.write_text(review)
    print(output)


if __name__ == "__main__":
    main()
