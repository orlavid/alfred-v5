"""Open-loop extraction provider."""

from __future__ import annotations

from executive.knowledge.vault import VaultNote

from src.knowledge.providers.base import ExecutiveKnowledgeProvider, ProviderMatch


class OpenLoopProvider(ExecutiveKnowledgeProvider):
    domain = "open_loops"

    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        return [ProviderMatch("open_loop", note) for note in notes if note.kind == "open_loop"]
