from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import re
from typing import Iterable

from executive.knowledge.entity_contract import (
    CanonicalExecutiveEntityContract,
    extract_explicit_field,
    iso_today,
    latest_date_signal,
    normalise_unknown,
    risk_bucket,
    stable_date,
)
from executive.knowledge.resolver import resolve_link_with_index

PREFERRED_EXECUTIVE_TYPES = {
    "objective",
    "project",
    "decision",
    "risk",
    "company",
    "person",
    "meeting",
    "follow_up",
    "open_loop",
}
NOISY_ENTITY_PREFIXES = (
    "00 Inbox/Captures/",
    "07 AI Memory/Entities/",
)
EXCLUDED_TITLE_PREFIXES = (
    "historical capture",
    "capture - ",
)
GENERIC_YEAR_RE = re.compile(r"^(?:19|20)\d{2}$")
WEAK_FILENAME_RE = re.compile(r"^[a-z0-9]+(?:[-_][a-z0-9]+)+$")
WEAK_FILENAME_TOKENS = {
    "ai",
    "archive",
    "capture",
    "copy",
    "draft",
    "entity",
    "export",
    "file",
    "fragment",
    "import",
    "memory",
    "new",
    "note",
    "notes",
    "snapshot",
    "temp",
    "tmp",
    "untitled",
    "v1",
    "v2",
    "v3",
}


CanonicalExecutiveEntity = CanonicalExecutiveEntityContract


@dataclass(frozen=True)
class RejectedExecutiveEntity:
    title: str
    entity_type: str
    path: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ExecutiveEntityQualityResult:
    canonical_entities: tuple[CanonicalExecutiveEntity, ...]
    rejected_entities: tuple[RejectedExecutiveEntity, ...]


def build_executive_entity_quality(
    entities: Iterable,
    resolution_model,
    *,
    graph: dict | None = None,
    objective_analysis: dict | None = None,
    project_analysis: dict | None = None,
    company_analysis: dict | None = None,
    people_analysis: dict | None = None,
    decision_analysis: dict | None = None,
    risk_analysis: dict | None = None,
    ownership: dict | None = None,
) -> ExecutiveEntityQualityResult:
    grouped: dict[str, list] = defaultdict(list)
    entity_lookup = {entity.id: entity for entity in entities}
    neighbour_ids = _build_neighbour_ids(graph or {})
    context = _build_context_indexes(
        objective_analysis or {},
        project_analysis or {},
        company_analysis or {},
        people_analysis or {},
        decision_analysis or {},
        risk_analysis or {},
        ownership or {},
    )

    for entity in entities:
        canonical = resolve_link_with_index(entity.title, resolution_model.index) or entity
        grouped[canonical.id].append(entity)

    canonical_entities: list[CanonicalExecutiveEntity] = []
    rejected_entities: list[RejectedExecutiveEntity] = []

    for canonical_id in sorted(grouped):
        group = sorted(grouped[canonical_id], key=lambda entity: (entity.path, entity.title))
        canonical = resolve_link_with_index(group[0].title, resolution_model.index) or group[0]
        reasons = _quality_rejections(canonical, group)

        if reasons:
            rejected_entities.append(
                RejectedExecutiveEntity(
                    title=canonical.title,
                    entity_type=canonical.type,
                    path=canonical.path,
                    reasons=tuple(reasons),
                )
            )
            continue

        canonical_entities.append(
            _build_contract(
                canonical,
                group,
                resolution_model.index,
                entity_lookup,
                neighbour_ids,
                context,
            )
        )

    return ExecutiveEntityQualityResult(
        canonical_entities=tuple(canonical_entities),
        rejected_entities=tuple(sorted(rejected_entities, key=lambda item: (item.entity_type, item.title, item.path))),
    )


def _build_context_indexes(
    objective_analysis: dict,
    project_analysis: dict,
    company_analysis: dict,
    people_analysis: dict,
    decision_analysis: dict,
    risk_analysis: dict,
    ownership: dict,
) -> dict[str, dict]:
    return {
        "objectives": {item.title: item for item in objective_analysis.get("insights", []) if getattr(item, "title", None)},
        "projects": {item.title: item for item in project_analysis.get("insights", []) if getattr(item, "title", None)},
        "companies": {item.title: item for item in company_analysis.get("insights", []) if getattr(item, "title", None)},
        "people": {item.title: item for item in people_analysis.get("insights", []) if getattr(item, "title", None)},
        "decisions": {item["title"]: item for item in decision_analysis.get("top_decisions", []) if item.get("title")},
        "risks": {item["title"]: item for item in risk_analysis.get("all", []) if item.get("title")},
        "ownership": {item["project"]: item for item in ownership.get("projects", []) if item.get("project")},
    }


def _build_contract(canonical, grouped_entities, resolution_index, entity_lookup, neighbour_ids, context) -> CanonicalExecutiveEntity:
    alias_values = sorted(
        {
            alias.strip()
            for entity in grouped_entities
            for alias in [entity.title, *getattr(entity, "aliases", [])]
            if alias.strip() and alias.strip() != canonical.title
        }
    )
    evidence_paths = tuple(sorted({entity.path for entity in grouped_entities}))
    supporting_notes = tuple(sorted({entity.title for entity in grouped_entities}))
    related = _related_entities(canonical, grouped_entities, resolution_index, entity_lookup, neighbour_ids)

    owner_value, owner_paths = extract_explicit_field("owner", grouped_entities)
    delegate_value, delegate_paths = extract_explicit_field("delegates", grouped_entities)
    status_value, status_paths = extract_explicit_field("status", grouped_entities)
    priority_value, priority_paths = extract_explicit_field("priority", grouped_entities)
    risk_value, risk_paths = extract_explicit_field("risk_level", grouped_entities)
    due_value, due_paths = extract_explicit_field("due_date", grouped_entities)
    review_value, review_paths = extract_explicit_field("review_date", grouped_entities)
    created_value, created_paths = extract_explicit_field("created", grouped_entities)
    activity_value, activity_paths = extract_explicit_field("last_activity", grouped_entities)

    owner = normalise_unknown(owner_value) if isinstance(owner_value, str) else None
    delegates = delegate_value if isinstance(delegate_value, tuple) else ()

    if owner is None and canonical.type == "project":
        ownership_record = context["ownership"].get(canonical.title)
        inferred_owner = normalise_unknown(ownership_record.get("owner")) if ownership_record else None
        if inferred_owner is not None and ownership_record.get("confidence", 0) >= 1.0:
            owner = inferred_owner
            owner_paths = _paths_for_related_names(related["people"], entity_lookup, resolution_index)

    status = normalise_unknown(status_value) if isinstance(status_value, str) else _derived_status(canonical, context)
    risk_level = normalise_unknown(risk_value) if isinstance(risk_value, str) else _derived_risk_level(canonical, context)
    priority = normalise_unknown(priority_value) if isinstance(priority_value, str) else None

    last_activity = activity_value if isinstance(activity_value, str) else latest_date_signal(
        [
            canonical.title,
            canonical.path,
            *[getattr(entity, "source_text", "") for entity in grouped_entities],
        ]
    )
    created = created_value if isinstance(created_value, str) else stable_date([canonical.title, canonical.path])
    due_date = due_value if isinstance(due_value, str) else None
    review_date = review_value if isinstance(review_value, str) else None
    last_verified = review_date or last_activity

    provenance = {
        "canonical_name": evidence_paths,
        "aliases": evidence_paths if alias_values else (),
        "owner": owner_paths,
        "delegates": delegate_paths,
        "status": status_paths or ((canonical.path,) if status else ()),
        "priority": priority_paths,
        "risk_level": risk_paths or ((canonical.path,) if risk_level else ()),
        "due_date": due_paths,
        "review_date": review_paths,
        "created": created_paths or ((canonical.path,) if created else ()),
        "last_activity": activity_paths or ((canonical.path,) if last_activity else ()),
        "related_objectives": _paths_for_related_names(related["objectives"], entity_lookup, resolution_index),
        "related_projects": _paths_for_related_names(related["projects"], entity_lookup, resolution_index),
        "related_people": _paths_for_related_names(related["people"], entity_lookup, resolution_index),
        "related_meetings": _paths_for_related_names(related["meetings"], entity_lookup, resolution_index),
        "dependencies": _paths_for_related_names(related["dependencies"], entity_lookup, resolution_index),
    }

    missing_fields = tuple(
        field_name
        for field_name, value in (
            ("owner", owner),
            ("delegates", delegates if delegates else None),
            ("status", status),
            ("priority", priority),
            ("risk_level", risk_level),
            ("created", created),
            ("last_activity", last_activity),
            ("due_date", due_date),
            ("review_date", review_date),
            ("related_objectives", related["objectives"] if related["objectives"] else None),
            ("related_projects", related["projects"] if related["projects"] else None),
            ("related_people", related["people"] if related["people"] else None),
            ("related_meetings", related["meetings"] if related["meetings"] else None),
            ("dependencies", related["dependencies"] if related["dependencies"] else None),
        )
        if value is None or value == () or value == []
    )

    return CanonicalExecutiveEntity(
        entity_id=canonical.id,
        entity_type=canonical.type,
        canonical_name=canonical.title,
        aliases=tuple(alias_values),
        owner=owner,
        delegates=tuple(delegates),
        status=status,
        priority=priority,
        risk_level=risk_level,
        confidence=_quality_confidence(grouped_entities),
        created=created,
        last_activity=last_activity,
        due_date=due_date,
        review_date=review_date,
        related_objectives=related["objectives"],
        related_projects=related["projects"],
        related_people=related["people"],
        related_meetings=related["meetings"],
        dependencies=related["dependencies"],
        evidence_paths=evidence_paths,
        evidence_count=len(evidence_paths),
        supporting_notes=supporting_notes,
        missing_fields=missing_fields,
        provenance={key: tuple(value) for key, value in provenance.items() if value},
        last_verified=last_verified,
        primary_path=canonical.path,
        provider=canonical.type,
        extensions={
            "evidence_titles": supporting_notes,
            "source_entity_ids": tuple(sorted({entity.id for entity in grouped_entities})),
        },
    )


def _related_entities(canonical, grouped_entities, resolution_index, entity_lookup, neighbour_ids) -> dict[str, tuple[str, ...]]:
    related_by_type: dict[str, set[str]] = defaultdict(set)
    entity_ids = {entity.id for entity in grouped_entities}

    for entity_id in entity_ids:
        for neighbour_id in neighbour_ids.get(entity_id, set()):
            neighbour = entity_lookup.get(neighbour_id)
            if neighbour is None:
                continue
            resolved = resolve_link_with_index(neighbour.title, resolution_index) or neighbour
            if resolved.id in entity_ids:
                continue
            related_by_type[resolved.type].add(resolved.title)

    dependencies = sorted(
        related_by_type.get("open_loop", set())
        | related_by_type.get("risk", set())
        | related_by_type.get("decision", set())
    )

    return {
        "objectives": tuple(sorted(related_by_type.get("objective", set()))),
        "projects": tuple(sorted(related_by_type.get("project", set()))),
        "people": tuple(sorted(related_by_type.get("person", set()))),
        "meetings": tuple(sorted(related_by_type.get("meeting", set()))),
        "dependencies": tuple(dependencies),
    }


def _paths_for_related_names(names, entity_lookup, resolution_index) -> tuple[str, ...]:
    paths = []
    for name in names:
        resolved = resolve_link_with_index(name, resolution_index)
        if resolved is not None:
            paths.append(resolved.path)
    return tuple(sorted(set(paths)))


def _build_neighbour_ids(graph: dict) -> dict[str, set[str]]:
    neighbours: dict[str, set[str]] = defaultdict(set)
    for edge in graph.get("edges", []):
        source = edge.get("source")
        target = edge.get("target")
        if not source or not target:
            continue
        neighbours[source].add(target)
        neighbours[target].add(source)
    return neighbours


def _derived_status(canonical, context) -> str | None:
    if canonical.type == "objective":
        insight = context["objectives"].get(canonical.title)
        return getattr(insight, "status", None)
    if canonical.type == "project":
        insight = context["projects"].get(canonical.title)
        return getattr(insight, "status", None)
    if canonical.type == "company":
        insight = context["companies"].get(canonical.title)
        return getattr(insight, "status", None)
    return None


def _derived_risk_level(canonical, context) -> str | None:
    if canonical.type == "person":
        insight = context["people"].get(canonical.title)
        return getattr(insight, "risk", None)
    risk_item = context["risks"].get(canonical.title)
    if risk_item is not None:
        return risk_bucket(risk_item.get("risk_score"))
    if canonical.type == "company":
        insight = context["companies"].get(canonical.title)
        status = getattr(insight, "status", None)
        if status == "CRITICAL":
            return "HIGH"
        if status == "IMPORTANT":
            return "MEDIUM"
    return None


def _quality_rejections(canonical, grouped_entities: list) -> list[str]:
    entity_type = getattr(canonical, "type", "")
    title = getattr(canonical, "title", "").strip()
    path = getattr(canonical, "path", "").replace("\\", "/")
    lowered_title = title.lower()

    reasons: list[str] = []

    if entity_type not in PREFERRED_EXECUTIVE_TYPES:
        reasons.append("not a preferred executive entity type")

    if any(path.startswith(prefix) for prefix in NOISY_ENTITY_PREFIXES):
        reasons.append("noisy capture or AI-memory source")

    if any(lowered_title.startswith(prefix) for prefix in EXCLUDED_TITLE_PREFIXES):
        reasons.append("capture artefact title")

    if GENERIC_YEAR_RE.fullmatch(title):
        reasons.append("generic year title")

    if _is_weak_filename_entity(title, path, grouped_entities):
        reasons.append("weak filename-derived entity")

    return reasons


def _is_weak_filename_entity(title: str, path: str, grouped_entities: list) -> bool:
    lowered = title.lower().strip()
    if not WEAK_FILENAME_RE.fullmatch(lowered):
        return False

    tokens = [token for token in re.split(r"[-_]+", lowered) if token]
    if not tokens:
        return True

    if all(token.isdigit() for token in tokens):
        return True

    if any(token in WEAK_FILENAME_TOKENS for token in tokens):
        return True

    if any(token.isdigit() and len(token) >= 4 for token in tokens):
        return True

    source_titles = {entity.title.lower().strip() for entity in grouped_entities}
    if len(source_titles) == 1 and lowered in source_titles and path.startswith("07 AI Memory/"):
        return True

    return False


def _quality_confidence(grouped_entities: list) -> str:
    if len(grouped_entities) >= 3:
        return "HIGH"
    if len(grouped_entities) == 2:
        return "MEDIUM"
    return "LOW"
