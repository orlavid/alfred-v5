"""Follow-up extraction provider."""

from __future__ import annotations

from executive.knowledge.vault import VaultNote

from src.knowledge.providers.base import ExecutiveKnowledgeProvider, ProviderMatch


class FollowupProvider(ExecutiveKnowledgeProvider):
    domain = "followups"

    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        return [ProviderMatch("follow_up", note) for note in notes if note.kind == "follow_up"]
