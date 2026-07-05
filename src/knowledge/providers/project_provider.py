"""Project extraction provider."""

from __future__ import annotations

from executive.knowledge.vault import VaultNote

from src.knowledge.providers.base import ExecutiveKnowledgeProvider, ProviderMatch


class ProjectProvider(ExecutiveKnowledgeProvider):
    domain = "projects"

    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        return [ProviderMatch("project", note) for note in notes if note.kind == "project"]
