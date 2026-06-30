#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
EVIDENCE = ROOT / "evidence" / "alfred-inventory"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def read(rel: str, limit: int = 50000) -> str:
    path = EVIDENCE / rel
    if not path.exists():
        return "_Missing evidence._"
    return path.read_text(errors="ignore")[:limit]


review = f"""# Executive Review

Generated: {datetime.now().isoformat()}

## Executive Summary

This is the first Executive Review prototype generated from Recovery Point Alpha engineering evidence.

## Current Platform State

### Services

```text
{read("system/services.txt")}
```

### Timers

```text
{read("system/timers.txt")}
```

### Listening Ports

```text
{read("system/listening_ports.txt")}
```

## Telegram

```text
{read("telegram/status.txt")}
```

## Obsidian Vault

```text
{read("obsidian/vault_summary.txt")}
```

## LlamaIndex

```text
{read("llamaindex/index_summary.txt")}
```

## Initial Assessment

- Platform evidence is available.
- Telegram evidence is available.
- Obsidian vault evidence is available.
- LlamaIndex evidence is available.

## Next Improvement

Replace raw evidence sections with structured executive intelligence:

- What changed
- What needs attention
- Follow-ups
- Open loops
- Meetings
- Objectives
- Risks
- Recommended actions
"""

(OUT / "Executive_Review.md").write_text(review)
print("Executive review generated:")
print(OUT / "Executive_Review.md")
