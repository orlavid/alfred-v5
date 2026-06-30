#!/usr/bin/env python3

"""
Alfred Engineering Handbook Generator

Recovery Point Alpha

Entry point.
"""

from pathlib import Path

from src.builders.loader import EvidenceLoader
from src.builders.chapter_builder import ChapterBuilder
from src.writers.markdown_writer import MarkdownWriter
from src.writers.docx_writer import DocxWriter


ROOT = Path(__file__).parent

EVIDENCE = ROOT / "evidence" / "alfred-inventory"

OUTPUT = ROOT / "output"

OUTPUT.mkdir(exist_ok=True)


def main():

    print()

    print("=" * 60)
    print(" Alfred Engineering Handbook Generator")
    print("=" * 60)

    loader = EvidenceLoader(EVIDENCE)

    evidence = loader.load()

    builder = ChapterBuilder(evidence)

    handbook = builder.build()

    MarkdownWriter(OUTPUT).write(handbook)

    DocxWriter(OUTPUT).write(handbook)

    print()

    print("Complete.")

    print()

    print("Output")

    print(OUTPUT)


if __name__ == "__main__":
    main()
