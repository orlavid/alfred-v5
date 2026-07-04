#!/usr/bin/env python3
"""Build a read-only migration dependency graph for Project Phoenix Gate 1."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "vps"


@dataclass(frozen=True)
class Asset:
    category: str
    path: str
    purpose: str
    approximate_size: str
    dependencies: tuple[str, ...]
    disposition: str


ASSETS = (
    Asset("storage", "/docker/obsidian-vault", "Canonical Obsidian knowledge vault.", "55M", ("docker mount", "Obsidian sync", "Hermes capture path"), "KEEP"),
    Asset("storage", "/opt/llamaindex-bakeoff/index", "Semantic retrieval index persisted on VPS.", "170M", ("/docker/obsidian-vault", "/opt/llamaindex-bakeoff/app.py", "Python environment"), "REPLACE"),
    Asset("storage", "/opt/second-brain", "Legacy Hermes runtime root.", "250M (estimated)", ("systemd services", "docker runtime", "Python scripts"), "REPLACE"),
    Asset("storage", "/opt/hermes-trading", "Legacy trading adjunct scripts.", "50M (estimated)", ("Python environment", "Telegram invocation"), "ARCHIVE"),
    Asset("runtime", "/etc/systemd/system/hermes-telegram.service", "Telegram bot service entrypoint.", "4K", ("/root/hermes-telegram.py", "docker.service", "/root/.openrouter.env"), "REPLACE"),
    Asset("runtime", "docker://hermes-agent-mctr-hermes-agent-1", "Primary Hermes agent container.", "9.84G image / 3.04G content", ("ghcr.io/hostinger/hvps-hermes-agent:latest", "/opt/second-brain", "/docker/obsidian-vault"), "REPLACE"),
    Asset("runtime", "tcp://127.0.0.1:8788", "LlamaIndex API listener.", "N/A", ("/opt/llamaindex-bakeoff/app.py", "/opt/llamaindex-bakeoff/index"), "REPLACE"),
    Asset("configuration", "/etc/systemd/system/hermes-telegram.service.d/20-authoritative-vault.conf", "Service override for authoritative vault path.", "4K", ("/etc/systemd/system/hermes-telegram.service", "/docker/obsidian-vault"), "REPLACE"),
    Asset("configuration", "/etc/systemd/system/hermes-telegram.service.d/30-openrouter-env.conf", "Service override for model API environment file.", "4K", ("/etc/systemd/system/hermes-telegram.service", "/root/.openrouter.env"), "REPLACE"),
    Asset("configuration", "/etc/cloudflared/config.yml", "Ingress routing for Alfred, v2, and API endpoints.", "4K", ("localhost:4865", "127.0.0.1:4880", "127.0.0.1:8788"), "ARCHIVE"),
    Asset("configuration", "/root/.openrouter.env", "Legacy model API secret environment file.", "4K", ("OpenRouter account", "hermes-telegram.service"), "UNKNOWN"),
    Asset("data", "/docker/obsidian-vault/07 Executive Briefings", "Generated executive briefings retained inside the canonical vault.", "10M (estimated)", ("/docker/obsidian-vault", "daily briefing jobs"), "KEEP"),
    Asset("data", "/docker/obsidian-vault/09 Governance", "Governance reports, board packs, watchlists, and decision intelligence.", "20M (estimated)", ("/docker/obsidian-vault", "/opt/second-brain/scripts"), "KEEP"),
    Asset("data", "/opt/second-brain/action-queue", "Queued human or agent actions awaiting execution.", "5M (estimated)", ("/opt/second-brain", "titan executor"), "KEEP"),
    Asset("data", "/opt/second-brain/playbooks/titan_actions.json", "Legacy executor playbook for Titan action runs.", "1M (estimated)", ("/opt/second-brain", "titan executor"), "ARCHIVE"),
    Asset("data", "/root/hermes-telegram.py", "Legacy Telegram orchestration script.", "40K", ("/opt/second-brain/scripts", "/docker/obsidian-vault", "/root/.openrouter.env"), "ARCHIVE"),
    Asset("data", "/opt/llamaindex-bakeoff/app.py", "Legacy retrieval API application.", "16K", ("/opt/llamaindex-bakeoff/index", "FastAPI", "Uvicorn"), "REPLACE"),
)


def render_dependency_graph() -> str:
    lines = [
        "# Hermes VPS Dependency Graph",
        "",
        "Prepared for Project Phoenix Gate 1 discovery.",
        "",
        "```mermaid",
        "graph TD",
    ]
    for index, asset in enumerate(ASSETS):
        node = f"A{index}"
        label = _escape_label(asset.path)
        lines.append(f'    {node}["{label}"]')
        for dep in asset.dependencies:
            dep_node = _dependency_node(dep)
            lines.append(f'    {node} --> {dep_node}["{_escape_label(dep)}"]')
    lines.extend(["```", "", "## Asset Summary", ""])
    for asset in ASSETS:
        lines.append(f"- `{asset.path}` | {asset.purpose} | {asset.disposition}")
    lines.append("")
    return "\n".join(lines)


def write_outputs() -> tuple[Path, Path]:
    OUT.mkdir(parents=True, exist_ok=True)
    graph_path = OUT / "DEPENDENCY_GRAPH.md"
    csv_path = OUT / "ASSET_REGISTER.csv"
    graph_path.write_text(render_dependency_graph())
    with csv_path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Category", "Path", "Purpose", "Approximate Size", "Dependencies", "Disposition"])
        for asset in ASSETS:
            writer.writerow(
                [
                    asset.category,
                    asset.path,
                    asset.purpose,
                    asset.approximate_size,
                    "; ".join(asset.dependencies),
                    asset.disposition,
                ]
            )
    return graph_path, csv_path


def _dependency_node(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return "D_" + (slug or "dependency")


def _escape_label(value: str) -> str:
    return value.replace('"', "'")


if __name__ == "__main__":
    graph_path, csv_path = write_outputs()
    print(graph_path)
    print(csv_path)
