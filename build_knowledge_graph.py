#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from src.knowledge.knowledge_graph import (
    build_knowledge_graph,
    render_knowledge_graph,
    render_knowledge_graph_json,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)


def main() -> None:
    report = build_knowledge_graph()
    markdown_output = OUT / "Knowledge_Graph.md"
    json_output = OUT / "Knowledge_Graph.json"
    markdown_output.write_text(render_knowledge_graph(report))
    json_output.write_text(render_knowledge_graph_json(report))
    print(markdown_output)
    print(json_output)


if __name__ == "__main__":
    main()
