"""Provider-backed Obsidian extraction for Alfred executive knowledge."""

from __future__ import annotations

from pathlib import Path

from executive.knowledge.entity import VaultEntity

from src.knowledge.providers.base import ExecutiveKnowledgeProvider
from src.knowledge.providers.daily_log_provider import DailyLogProvider
from src.knowledge.providers.followup_provider import FollowupProvider
from src.knowledge.providers.objective_provider import ObjectiveProvider
from src.knowledge.providers.obsidian_provider import load_obsidian_notes, ObsidianProvider
from src.knowledge.providers.open_loop_provider import OpenLoopProvider
from src.knowledge.providers.project_provider import ProjectProvider

ENTITY_PROVIDER_DOMAINS = ("objectives", "projects", "daily_logs", "obsidian")
ALL_PROVIDER_DOMAINS = ENTITY_PROVIDER_DOMAINS + ("followups", "open_loops")


def get_knowledge_providers() -> tuple[ExecutiveKnowledgeProvider, ...]:
    return (
        ObjectiveProvider(),
        ProjectProvider(),
        DailyLogProvider(),
        FollowupProvider(),
        OpenLoopProvider(),
        ObsidianProvider(),
    )


def extract_provider_entities(
    vault_root: Path,
    *,
    domains: tuple[str, ...] = ENTITY_PROVIDER_DOMAINS,
) -> tuple[VaultEntity, ...]:
    notes = load_obsidian_notes(vault_root)
    providers = [provider for provider in get_knowledge_providers() if provider.domain in domains]
    entities: list[VaultEntity] = []
    seen: set[tuple[str, str]] = set()

    for provider in providers:
        for entity in provider.extract_entities(notes):
            key = (entity.path, entity.type)
            if key in seen:
                continue
            seen.add(key)
            entities.append(entity)

    return tuple(sorted(entities, key=lambda item: (item.type, item.path.lower(), item.title.lower())))
