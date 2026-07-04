"""Build Executive Understanding report."""

from __future__ import annotations

from pathlib import Path

from src.knowledge.executive_knowledge_builder import DEFAULT_EVIDENCE_ROOT, DEFAULT_VAULT_ROOT
from src.knowledge.executive_understanding import build_executive_understanding, render_executive_understanding

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"


def build_understanding_report(
    evidence_root: Path | None = None,
    *,
    vault_root: Path | None = None,
) -> str:
    effective_vault_root = vault_root or DEFAULT_VAULT_ROOT
    source_root = effective_vault_root if effective_vault_root.exists() else (evidence_root or DEFAULT_EVIDENCE_ROOT)
    report = build_executive_understanding(source_root)
    output = OUT / "Executive_Understanding.md"
    output.write_text(render_executive_understanding(report))
    return str(output)
