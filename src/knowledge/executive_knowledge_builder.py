"""Obsidian-first executive knowledge builder for Alfred."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
import json
import re
from typing import Iterable

from executive.knowledge.entity import VaultEntity
from executive.knowledge.extractor import extract_links, extract_tags
from executive.knowledge.graph import build_graph
from executive.knowledge.resolver import build_entity_resolution, build_resolution_index, resolve_link_with_index
from executive.knowledge.vault import VaultNote, load_vault
from src.knowledge.providers import extract_provider_entities

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_ROOT = ROOT / "evidence" / "alfred-inventory"
DEFAULT_VAULT_ROOT = ROOT / ".vault-not-configured"
STALE_AFTER_DAYS = 30

SECTION_HEADINGS = [
    "Executive Summary",
    "Entity Inventory",
    "Objectives",
    "Projects",
    "Companies",
    "People",
    "Decisions",
    "Meetings",
    "Risks",
    "Policies",
    "Daily Logs",
    "Executive Briefings",
    "Relationship Graph",
    "Orphans",
    "Stale Evidence",
    "Recommended Actions",
]

DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2}|20\d{6})\b")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

ENTITY_TYPES = (
    "objective",
    "project",
    "company",
    "person",
    "decision",
    "meeting",
    "risk",
    "policy",
    "daily_log",
    "executive_briefing",
)


@dataclass(frozen=True)
class KnowledgeEntity:
    id: str
    entity_type: str
    title: str
    path: str
    source_reference: str
    confidence: str
    relationships: tuple[str, ...]
    orphan: bool
    stale_evidence: bool
    last_evidence_date: str | None


@dataclass(frozen=True)
class KnowledgeRelationship:
    source: str
    target: str
    relationship_type: str


@dataclass(frozen=True)
class ExecutiveKnowledgeModel:
    source_mode: str
    source_root: str
    entity_inventory: dict[str, int]
    entities: tuple[KnowledgeEntity, ...]
    raw_entities: tuple[dict, ...]
    canonical_entities: tuple[dict, ...]
    aliases: tuple[dict, ...]
    relationship_graph: tuple[KnowledgeRelationship, ...]
    orphans: tuple[KnowledgeEntity, ...]
    stale_evidence: tuple[KnowledgeEntity, ...]
    executive_summary: list[str]
    recommended_actions: list[str]


def build_executive_knowledge(
    evidence_root: Path | None = None,
    *,
    vault_root: Path | None = None,
    today: date | None = None,
) -> ExecutiveKnowledgeModel:
    effective_today = today or date.today()
    live_vault_root = vault_root or DEFAULT_VAULT_ROOT
    if load_vault(live_vault_root):
        return _build_from_live_vault(live_vault_root, effective_today)
    return _build_from_evidence_inventory(evidence_root or DEFAULT_EVIDENCE_ROOT, effective_today)


def render_executive_knowledge(report: ExecutiveKnowledgeModel) -> str:
    parts = ["# Executive Knowledge Builder", ""]
    parts.extend(["## Executive Summary", ""])
    parts.extend(_render_bullets(report.executive_summary))
    parts.extend(["", "## Entity Inventory", ""])
    parts.extend(_render_bullets([f"{entity_type}: {report.entity_inventory.get(entity_type, 0)}" for entity_type in ENTITY_TYPES]))
    for section, entity_type in (
        ("Objectives", "objective"),
        ("Projects", "project"),
        ("Companies", "company"),
        ("People", "person"),
        ("Decisions", "decision"),
        ("Meetings", "meeting"),
        ("Risks", "risk"),
        ("Policies", "policy"),
        ("Daily Logs", "daily_log"),
        ("Executive Briefings", "executive_briefing"),
    ):
        parts.extend(["", f"## {section}", ""])
        entities = [entity for entity in report.entities if entity.entity_type == entity_type]
        parts.extend(_render_entities(entities))
    parts.extend(["", "## Relationship Graph", ""])
    parts.extend(_render_relationships(report.relationship_graph))
    parts.extend(["", "## Orphans", ""])
    parts.extend(_render_entities(report.orphans))
    parts.extend(["", "## Stale Evidence", ""])
    parts.extend(_render_entities(report.stale_evidence))
    parts.extend(["", "## Recommended Actions", ""])
    parts.extend(_render_bullets(report.recommended_actions))
    parts.append("")
    return "\n".join(parts)


def render_executive_knowledge_json(report: ExecutiveKnowledgeModel) -> str:
    payload = {
        "source_mode": report.source_mode,
        "source_root": report.source_root,
        "entity_inventory": report.entity_inventory,
        "entities": [asdict(entity) for entity in report.entities],
        "canonical_entities": list(report.canonical_entities),
        "aliases": list(report.aliases),
        "relationships": [asdict(edge) for edge in report.relationship_graph],
        "relationship_graph": [asdict(edge) for edge in report.relationship_graph],
        "orphans": [asdict(entity) for entity in report.orphans],
        "stale_evidence": [asdict(entity) for entity in report.stale_evidence],
        "executive_summary": report.executive_summary,
        "recommended_actions": report.recommended_actions,
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _build_from_live_vault(vault_root: Path, today: date) -> ExecutiveKnowledgeModel:
    entities = list(extract_provider_entities(vault_root))
    resolution_model = build_entity_resolution(entities)
    resolution_index = resolution_model.index
    graph = build_graph(entities, resolution_index)
    entity_lookup = {entity.id: entity for entity in entities}
    neighbours = _build_neighbours(graph["edges"])
    knowledge_entities = _build_knowledge_entities_from_vault(entities, neighbours, today)
    relationships = _build_relationships(graph["edges"], entity_lookup)
    return _assemble_model("live_vault", vault_root, knowledge_entities, relationships, resolution_model)


def _build_from_evidence_inventory(evidence_root: Path, today: date) -> ExecutiveKnowledgeModel:
    if not evidence_root.exists():
        return ExecutiveKnowledgeModel(
            source_mode="evidence_inventory",
            source_root=str(evidence_root),
            entity_inventory={entity_type: 0 for entity_type in ENTITY_TYPES},
            entities=(),
            raw_entities=(),
            canonical_entities=(),
            aliases=(),
            relationship_graph=(),
            orphans=(),
            stale_evidence=(),
            executive_summary=[f"No live vault was available and the evidence inventory path does not exist: {evidence_root}."],
            recommended_actions=["Provide a vault root or evidence inventory before rebuilding executive knowledge."],
        )

    notes = _load_evidence_notes(evidence_root)
    entities = _build_entities_from_notes(notes)
    resolution_model = build_entity_resolution(entities)
    resolution_index = resolution_model.index
    relationships = _build_inventory_relationships(entities, notes, resolution_index)
    neighbours = _build_neighbours([asdict(edge) for edge in relationships])
    knowledge_entities = _build_knowledge_entities_from_vault(entities, neighbours, today)
    return _assemble_model("evidence_inventory", evidence_root, knowledge_entities, relationships, resolution_model)


def _load_evidence_notes(evidence_root: Path) -> list[VaultNote]:
    notes: list[VaultNote] = []
    for path in sorted(evidence_root.rglob("*")):
        if path.is_dir() or path.suffix.lower() not in {".md", ".txt", ".json", ".yml", ".yaml"}:
            continue
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        rel = path.relative_to(evidence_root)
        notes.append(
            VaultNote(
                path=str(rel),
                title=path.stem,
                folder=rel.parts[0] if rel.parts else "",
                text=text,
                kind=_classify_evidence_path(rel, text),
            )
        )
    return notes


def _classify_evidence_path(path: Path, text: str) -> str:
    lowered = f"{str(path).lower()}\n{text.lower()}"
    if "objective" in lowered or "okr" in lowered or "goal" in lowered:
        return "objective"
    if "project" in lowered or "programme" in lowered or "initiative" in lowered:
        return "project"
    if "compan" in lowered or "supplier" in lowered or "vendor" in lowered:
        return "company"
    if "people" in lowered or "stakeholder" in lowered or "owner" in lowered:
        return "person"
    if "decision" in lowered or "approval" in lowered:
        return "decision"
    if "meeting" in lowered or "agenda" in lowered or "minutes" in lowered:
        return "meeting"
    if "risk" in lowered or "issue" in lowered or "escalation" in lowered:
        return "risk"
    if "policy" in lowered or "framework" in lowered or "standard" in lowered:
        return "policy"
    if "daily" in lowered or "log" in lowered:
        return "daily_log"
    if "briefing" in lowered or "executive review" in lowered:
        return "executive_briefing"
    return "note"


def _build_entities_from_notes(notes: list[VaultNote]) -> list[VaultEntity]:
    entities: list[VaultEntity] = []
    for note in notes:
        if note.kind not in ENTITY_TYPES:
            continue
        entities.append(
            VaultEntity(
                id=note.path,
                type=note.kind,
                title=note.title,
                path=note.path,
                tags=extract_tags(note.text),
                links=extract_links(note.text),
            )
        )
    return sorted(entities, key=lambda item: (item.type, item.title.lower(), item.path))


def _build_inventory_relationships(
    entities: list[VaultEntity],
    notes: list[VaultNote],
    resolution_index,
) -> tuple[KnowledgeRelationship, ...]:
    entity_lookup = {entity.id: entity for entity in entities}
    note_lookup = {note.path: note for note in notes}
    relationships: list[KnowledgeRelationship] = []
    seen = set()

    for entity in entities:
        note = note_lookup.get(entity.path)
        if note is None:
            continue
        for link in entity.links:
            target = resolve_link_with_index(link, resolution_index)
            if target is None or target.id not in entity_lookup:
                continue
            key = (entity.id, target.id, "links_to")
            if key in seen:
                continue
            seen.add(key)
            relationships.append(KnowledgeRelationship(entity.id, target.id, "links_to"))

        for other in entities:
            if other.id == entity.id:
                continue
            if _normalise(other.title) in _normalise(note.text):
                key = (entity.id, other.id, "mentions")
                if key in seen:
                    continue
                seen.add(key)
                relationships.append(KnowledgeRelationship(entity.id, other.id, "mentions"))

    return tuple(sorted(relationships, key=lambda item: (item.source, item.target, item.relationship_type))[:400])


def _build_knowledge_entities_from_vault(
    entities: list[VaultEntity],
    neighbours: dict[str, tuple[str, ...]],
    today: date,
) -> tuple[KnowledgeEntity, ...]:
    records: list[KnowledgeEntity] = []
    for entity in entities:
        if entity.type not in ENTITY_TYPES:
            continue
        last_date = _latest_date_from_strings(entity.path, entity.title)
        stale = last_date is not None and (today - last_date).days >= STALE_AFTER_DAYS
        linked = neighbours.get(entity.id, ())
        records.append(
            KnowledgeEntity(
                id=entity.id,
                entity_type=entity.type,
                title=entity.title,
                path=entity.path,
                source_reference=entity.path,
                confidence=_derive_entity_confidence(entity, linked),
                relationships=tuple(linked),
                orphan=len(linked) == 0,
                stale_evidence=stale,
                last_evidence_date=last_date.isoformat() if last_date else None,
            )
        )
    return tuple(sorted(records, key=lambda item: (item.entity_type, item.title.lower(), item.path)))


def _build_relationships(edges: list[dict], entity_lookup: dict[str, VaultEntity]) -> tuple[KnowledgeRelationship, ...]:
    relationships = []
    seen = set()
    for edge in edges:
        if edge["source"] not in entity_lookup or edge["target"] not in entity_lookup:
            continue
        key = (edge["source"], edge["target"], edge["type"])
        if key in seen:
            continue
        seen.add(key)
        relationships.append(KnowledgeRelationship(edge["source"], edge["target"], edge["type"]))
    return tuple(sorted(relationships, key=lambda item: (item.source, item.target, item.relationship_type))[:400])


def _assemble_model(
    source_mode: str,
    source_root: Path,
    entities: tuple[KnowledgeEntity, ...],
    relationships: tuple[KnowledgeRelationship, ...],
    resolution_model,
) -> ExecutiveKnowledgeModel:
    entity_inventory = {entity_type: 0 for entity_type in ENTITY_TYPES}
    for entity in entities:
        entity_inventory[entity.entity_type] = entity_inventory.get(entity.entity_type, 0) + 1
    orphans = tuple(entity for entity in entities if entity.orphan)
    stale_evidence = tuple(entity for entity in entities if entity.stale_evidence)
    summary = [
        f"Source mode: {source_mode}.",
        f"Source root: {source_root}.",
        f"Entities built: {len(entities)}; relationships built: {len(relationships)}.",
        f"Orphans: {len(orphans)}; stale evidence flags: {len(stale_evidence)}.",
    ]
    actions = _build_recommended_actions(orphans, stale_evidence, entity_inventory, source_mode)
    return ExecutiveKnowledgeModel(
        source_mode=source_mode,
        source_root=str(source_root),
        entity_inventory=entity_inventory,
        entities=entities,
        raw_entities=tuple(
            {
                "id": entity.id,
                "type": entity.type,
                "title": entity.title,
                "path": entity.path,
                "aliases": list(getattr(entity, "aliases", [])),
                "links": list(getattr(entity, "links", [])),
                "tags": list(getattr(entity, "tags", [])),
            }
            for entity in sorted(resolution_model.index[next(iter(resolution_model.index))], key=lambda item: (item.type, item.title.lower(), item.path))
        ) if resolution_model.index else (),
        canonical_entities=tuple(asdict(entity) for entity in resolution_model.canonical_entities),
        aliases=tuple(asdict(alias) for alias in resolution_model.aliases),
        relationship_graph=relationships,
        orphans=orphans[:50],
        stale_evidence=stale_evidence[:50],
        executive_summary=summary,
        recommended_actions=actions,
    )


def _build_recommended_actions(
    orphans: tuple[KnowledgeEntity, ...],
    stale_evidence: tuple[KnowledgeEntity, ...],
    entity_inventory: dict[str, int],
    source_mode: str,
) -> list[str]:
    actions = []
    if source_mode == "evidence_inventory":
        actions.append("No evidence found in a live vault; evidence inventory mode is active.")
    if orphans:
        actions.append(f"Review the {len(orphans)} orphaned entities and add links or ownership context in Obsidian.")
    if stale_evidence:
        actions.append(f"Refresh or confirm the {len(stale_evidence)} entities with stale dated evidence.")
    if entity_inventory.get("objective", 0) == 0:
        actions.append("Create or tag objective notes in Obsidian so executive strategy is represented canonically.")
    if entity_inventory.get("meeting", 0) == 0:
        actions.append("Capture meeting notes or agendas in Obsidian so relationship and decision evidence stays current.")
    return actions[:5] or ["Executive knowledge is current; continue recomputing derived intelligence from Obsidian."]


def _build_neighbours(edges: list[dict]) -> dict[str, tuple[str, ...]]:
    neighbours: dict[str, set[str]] = {}
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        neighbours.setdefault(source, set()).add(target)
        neighbours.setdefault(target, set()).add(source)
    return {
        entity_id: tuple(sorted(linked))
        for entity_id, linked in sorted(neighbours.items())
    }


def _derive_entity_confidence(entity: VaultEntity, linked: tuple[str, ...]) -> str:
    score = 1
    if linked:
        score += 1
    if entity.links:
        score += 1
    if entity.tags:
        score += 1
    if entity.type in {"objective", "project", "decision", "meeting", "risk"}:
        score += 1
    if score >= 4:
        return "HIGH"
    if score >= 2:
        return "MEDIUM"
    return "LOW"


def _latest_date_from_strings(*values: str) -> date | None:
    candidates: list[date] = []
    for value in values:
        for match in DATE_RE.findall(value):
            try:
                if "-" in match:
                    candidates.append(date.fromisoformat(match))
                else:
                    candidates.append(date.fromisoformat(f"{match[:4]}-{match[4:6]}-{match[6:]}"))
            except ValueError:
                continue
    return max(candidates) if candidates else None


def _render_bullets(values: Iterable[str]) -> list[str]:
    rendered = [f"- {value}" for value in values if value]
    return rendered or ["_None found._"]


def _render_entities(values: Iterable[KnowledgeEntity]) -> list[str]:
    entities = list(values)
    if not entities:
        return ["_None found._"]
    return [
        f"- {entity.title} | Confidence: {entity.confidence} | Orphan: {'YES' if entity.orphan else 'NO'} | "
        f"Stale: {'YES' if entity.stale_evidence else 'NO'} | Source: {entity.source_reference}"
        for entity in entities[:25]
    ]


def _render_relationships(values: Iterable[KnowledgeRelationship]) -> list[str]:
    relationships = list(values)
    if not relationships:
        return ["_None found._"]
    return [
        f"- {edge.source} -> {edge.target} ({edge.relationship_type})"
        for edge in relationships[:50]
    ]


def _normalise(value: str) -> str:
    value = value.lower()
    value = WIKILINK_RE.sub(lambda match: match.group(1).split("|")[0].strip().lower(), value)
    return re.sub(r"[^a-z0-9]+", "", value)
