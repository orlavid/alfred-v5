"""Objective extraction provider."""

from __future__ import annotations

from executive.knowledge.vault import VaultNote

from src.knowledge.providers.base import ExecutiveKnowledgeProvider, ProviderMatch


class ObjectiveProvider(ExecutiveKnowledgeProvider):
    domain = "objectives"

    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        return [ProviderMatch("objective", note) for note in notes if note.kind == "objective"]
