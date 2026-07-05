"""Shared Obsidian provider helpers and generic executive extraction."""

from __future__ import annotations

from pathlib import Path

from executive.knowledge.vault import VaultNote, load_vault

from src.knowledge.providers.base import ExecutiveKnowledgeProvider, ProviderMatch

EXECUTIVE_EXCLUDED_PATHS = {
    "output",
    "docs/migration",
    "system",
    "trees",
    "python",
    "analysis",
    ".git",
    ".obsidian",
    ".smart-env",
    "node_modules",
    "__pycache__",
}

GENERIC_ENTITY_TYPES = {
    "company",
    "person",
    "decision",
    "meeting",
    "risk",
    "policy",
    "executive_briefing",
}


class ObsidianProvider(ExecutiveKnowledgeProvider):
    domain = "obsidian"

    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        matches: list[ProviderMatch] = []
        for note in notes:
            if note.kind in GENERIC_ENTITY_TYPES:
                matches.append(ProviderMatch(note.kind, note))
        return matches


def load_obsidian_notes(vault_root: Path) -> list[VaultNote]:
    return load_vault(vault_root)
