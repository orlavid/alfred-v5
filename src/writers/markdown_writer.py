"""Markdown output writer."""

from __future__ import annotations

from pathlib import Path
from typing import Dict


class MarkdownWriter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write(self, handbook: Dict[str, str]) -> None:
        combined = []

        for filename, content in handbook.items():
            (self.output_dir / filename).write_text(content.strip() + "\n")
            combined.append(content.strip())

        (self.output_dir / "Alfred_Engineering_Handbook_Recovery_Point_Alpha.md").write_text(
            "\n\n---\n\n".join(combined) + "\n"
        )
