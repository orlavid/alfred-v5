"""Adapter for proven legacy executive knowledge acquisition behaviour."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import TYPE_CHECKING

from executive.engine import execute
from executive.knowledge.resolver import build_resolution_index, normalise_name, resolve_link_with_index
from executive.knowledge.vault import VaultNote, load_vault
from src.followups.followup_intelligence import FollowupIntelligence, build_followup_intelligence
from src.obsidian.live_vault import resolve_live_vault_path
from src.openloops.open_loop_intelligence import OpenLoopIntelligence, build_open_loop_intelligence

if TYPE_CHECKING:
    from src.knowledge.executive_knowledge_builder import ExecutiveKnowledgeModel
    from src.knowledge.knowledge_graph import KnowledgeGraphModel


@dataclass(frozen=True)
class LegacyKnowledgeAdapter:
    evidence_root: Path
    vault_root: Path
    notes: tuple[VaultNote, ...]
    engine_result: dict[str, Any]
    knowledge_model: ExecutiveKnowledgeModel
    relationship_graph: KnowledgeGraphModel
    followups: FollowupIntelligence
    open_loops: OpenLoopIntelligence

    @property
    def vault(self) -> dict[str, Any]:
        return self.engine_result["knowledge"]["vault"]

    @property
    def entities(self) -> tuple[Any, ...]:
        return tuple(self.vault.get("entities", []))

    @property
    def resolution_index(self) -> dict[str, Any]:
        return build_resolution_index(self.entities)

    def get_objectives(self) -> tuple[Any, ...]:
        return tuple(sorted(self.vault.get("objectives", {}).get("insights", []), key=_title_key))

    def get_projects(self) -> tuple[Any, ...]:
        return tuple(sorted(self.vault.get("projects", {}).get("insights", []), key=_title_key))

    def get_people(self) -> tuple[Any, ...]:
        return tuple(sorted(self.vault.get("people", {}).get("insights", []), key=_title_key))

    def get_companies(self) -> tuple[Any, ...]:
        return tuple(sorted(self.vault.get("companies", {}).get("insights", []), key=_title_key))

    def get_followups(self) -> FollowupIntelligence:
        return self.followups

    def get_open_loops(self) -> OpenLoopIntelligence:
        return self.open_loops

    def get_decisions(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            sorted(
                self.vault.get("decisions", {}).get("top_decisions", []),
                key=lambda item: (-item.get("importance", 0), item.get("title", "").lower()),
            )
        )

    def get_risks(self) -> tuple[dict[str, Any], ...]:
        return tuple(self.vault.get("risk", {}).get("high_risk", []))

    def get_priorities(self) -> tuple[dict[str, Any], ...]:
        return tuple(self.vault.get("priorities", {}).get("top_priorities", []))

    def get_policies(self) -> tuple[Any, ...]:
        return tuple(
            sorted(
                (entity for entity in self.knowledge_model.entities if entity.entity_type == "policy"),
                key=lambda entity: (entity.title.lower(), entity.path),
            )
        )

    def get_neighbours(self) -> dict[str, tuple[str, ...]]:
        return _build_neighbours(self.vault.get("graph", {}).get("edges", []))

    def get_company(self, name: str) -> Any | None:
        return self._lookup_named_item(name, self.get_companies(), entity_type="company")

    def get_person(self, name: str) -> Any | None:
        return self._lookup_named_item(name, self.get_people(), entity_type="person")

    def get_project(self, name: str) -> Any | None:
        return self._lookup_named_item(name, self.get_projects(), entity_type="project")

    def search(self, query: str, *, limit: int = 10) -> list[dict[str, Any]]:
        query_text = query.strip()
        if not query_text:
            return []
        terms = [normalise_name(part) for part in query_text.split() if normalise_name(part)]
        results: list[dict[str, Any]] = []

        for note in self.notes:
            score = _note_search_score(note, query_text, terms)
            if score <= 0:
                continue
            results.append(
                {
                    "title": note.title,
                    "path": note.path,
                    "kind": note.kind,
                    "score": score,
                    "provider": "legacy_adapter.search",
                    "source_note": note.path,
                    "snippet": _note_snippet(note, query_text),
                }
            )

        results.sort(key=lambda item: (-item["score"], item["path"], item["title"].lower()))
        return results[:limit]

    def semantic_search(self, query: str, *, limit: int = 10) -> list[dict[str, Any]]:
        seed_results = self.search(query, limit=limit * 2)
        if not query.strip():
            return []

        resolved = resolve_link_with_index(query, self.resolution_index)
        neighbours = self.get_neighbours()
        entity_lookup = {entity.id: entity for entity in self.entities}
        related_paths: dict[str, int] = {}

        if resolved is not None:
            related_paths[resolved.path] = 120
            for related_id in neighbours.get(resolved.id, ()):
                related_entity = entity_lookup.get(related_id)
                if related_entity is None:
                    continue
                related_paths[related_entity.path] = max(related_paths.get(related_entity.path, 0), 80)

        enriched: list[dict[str, Any]] = []
        seen_paths: set[str] = set()

        for item in seed_results:
            bonus = related_paths.get(item["path"], 0)
            enriched.append(
                {
                    **item,
                    "score": item["score"] + bonus,
                    "provider": "legacy_adapter.semantic_search",
                    "semantic_match": bonus > 0,
                }
            )
            seen_paths.add(item["path"])

        if related_paths:
            note_lookup = {note.path: note for note in self.notes}
            for path, bonus in sorted(related_paths.items(), key=lambda current: (-current[1], current[0])):
                if path in seen_paths or path not in note_lookup:
                    continue
                note = note_lookup[path]
                enriched.append(
                    {
                        "title": note.title,
                        "path": note.path,
                        "kind": note.kind,
                        "score": bonus,
                        "provider": "legacy_adapter.semantic_search",
                        "source_note": note.path,
                        "snippet": _note_snippet(note, query),
                        "semantic_match": True,
                    }
                )

        enriched.sort(key=lambda item: (-item["score"], item["path"], item["title"].lower()))
        return enriched[:limit]

    def _lookup_named_item(self, name: str, items: tuple[Any, ...], *, entity_type: str) -> Any | None:
        query = name.strip()
        if not query:
            return None

        resolved = resolve_link_with_index(query, self.resolution_index)
        resolved_title = getattr(resolved, "title", None)
        resolved_path = getattr(resolved, "path", None)

        for item in items:
            if resolved_path is not None and getattr(item, "path", None) == resolved_path:
                return item
        for item in items:
            if resolved_title is not None and getattr(item, "title", "").lower() == resolved_title.lower():
                return item
        for item in items:
            if normalise_name(getattr(item, "title", "")) == normalise_name(query):
                return item

        return next(
            (
                entity
                for entity in self.entities
                if getattr(entity, "type", None) == entity_type and normalise_name(entity.title) == normalise_name(query)
            ),
            None,
        )


def build_legacy_knowledge_adapter(
    evidence_root: Path,
    *,
    vault_root: Path | None = None,
) -> LegacyKnowledgeAdapter:
    from src.knowledge.executive_knowledge_builder import build_executive_knowledge
    from src.knowledge.knowledge_graph import build_knowledge_graph_from_model

    effective_vault_root = resolve_live_vault_path(vault_root)
    notes = tuple(load_vault(effective_vault_root))
    engine_result = execute(evidence_root, vault_root=effective_vault_root)
    knowledge_model = build_executive_knowledge(evidence_root, vault_root=effective_vault_root)
    relationship_graph = build_knowledge_graph_from_model(knowledge_model)
    followups = build_followup_intelligence(vault_root=effective_vault_root)
    open_loops = build_open_loop_intelligence(vault_root=effective_vault_root)
    return LegacyKnowledgeAdapter(
        evidence_root=evidence_root,
        vault_root=effective_vault_root,
        notes=notes,
        engine_result=engine_result,
        knowledge_model=knowledge_model,
        relationship_graph=relationship_graph,
        followups=followups,
        open_loops=open_loops,
    )


def _title_key(item: Any) -> tuple[str, str]:
    return (getattr(item, "title", "").lower(), getattr(item, "path", ""))


def _build_neighbours(edges: list[dict[str, Any]]) -> dict[str, tuple[str, ...]]:
    neighbours: dict[str, set[str]] = {}
    for edge in edges:
        source = edge.get("source")
        target = edge.get("target")
        if not source or not target:
            continue
        neighbours.setdefault(source, set()).add(target)
        neighbours.setdefault(target, set()).add(source)
    return {
        key: tuple(sorted(values))
        for key, values in sorted(neighbours.items(), key=lambda item: item[0])
    }


def _note_search_score(note: VaultNote, query: str, terms: list[str]) -> int:
    if not terms:
        return 0
    lowered_query = query.lower()
    title = note.title.lower()
    path = note.path.lower()
    text = note.text.lower()

    score = 0
    if title == lowered_query:
        score += 160
    elif lowered_query in title:
        score += 110
    if lowered_query in path:
        score += 70
    if lowered_query in text:
        score += 40

    normalised_title = normalise_name(note.title)
    normalised_path = normalise_name(note.path)
    normalised_text = normalise_name(note.text[:4000])
    for term in terms:
        if term and term in normalised_title:
            score += 30
        elif term and term in normalised_path:
            score += 20
        elif term and term in normalised_text:
            score += 10

    if note.kind in {"objective", "project", "person", "company", "decision", "meeting", "risk", "open_loop", "follow_up"}:
        score += 5
    return score


def _note_snippet(note: VaultNote, query: str) -> str:
    lowered_query = query.lower().strip()
    for line in note.text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if lowered_query and lowered_query in cleaned.lower():
            return cleaned[:220]
    for line in note.text.splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned[:220]
    return note.title
