#!/usr/bin/env python3

from __future__ import annotations

from src.pipeline.executive_pipeline import build_executive_pipeline, write_executive_pipeline_report


def main() -> None:
    report = build_executive_pipeline()
    output = write_executive_pipeline_report(report)
    print(output)


if __name__ == "__main__":
    main()
