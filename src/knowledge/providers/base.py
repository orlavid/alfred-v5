"""Provider base classes for executive knowledge extraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import re

from executive.knowledge.entity import VaultEntity
from executive.knowledge.vault import VaultNote

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9_/-]+)")


@dataclass(frozen=True)
class ProviderMatch:
    entity_type: str
    note: VaultNote


class ExecutiveKnowledgeProvider(ABC):
    domain: str

    @abstractmethod
    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        raise NotImplementedError

    def extract_entities(self, notes: list[VaultNote]) -> list[VaultEntity]:
        entities: list[VaultEntity] = []
        for match in self.extract_matches(notes):
            entities.append(
                VaultEntity(
                    id=match.note.path,
                    type=match.entity_type,
                    title=match.note.title,
                    path=match.note.path,
                    tags=_extract_tags(match.note.text),
                    links=_extract_links(match.note.text),
                )
            )
        return entities


def _extract_links(text: str) -> list[str]:
    return [match.split("|")[0].strip() for match in WIKILINK_RE.findall(text)]


def _extract_tags(text: str) -> list[str]:
    return sorted(set(TAG_RE.findall(text)))
