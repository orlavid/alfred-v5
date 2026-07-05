"""Daily-log extraction provider."""

from __future__ import annotations

from executive.knowledge.vault import VaultNote

from src.knowledge.providers.base import ExecutiveKnowledgeProvider, ProviderMatch


class DailyLogProvider(ExecutiveKnowledgeProvider):
    domain = "daily_logs"

    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        return [ProviderMatch("daily_log", note) for note in notes if note.kind == "daily_log"]
