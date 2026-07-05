"""Meeting brief builder for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Iterable

from executive.intelligence.risk import analyse_risk
from executive.knowledge.extractor import extract_entities, extract_links
from executive.knowledge.graph import build_graph
from executive.knowledge.resolver import build_resolution_index, normalise_name, resolve_link_with_index
from executive.knowledge.vault import VaultNote, load_vault
from src.obsidian.live_vault import resolve_live_vault_path

SECTION_HEADINGS = [
    "Meeting",
    "Executive Summary",
    "Related People",
    "Related Projects",
    "Related Companies",
    "Related Objectives",
    "Related Decisions",
    "Risks",
    "Open Loops",
    "Follow-ups",
    "Recommended Discussion",
    "Confidence",
]


@dataclass(frozen=True)
class EvidenceItem:
    title: str
    path: str
    kind: str
    reason: str


@dataclass(frozen=True)
class MeetingBrief:
    subject: str
    generated_at: str
    matched_entities: list[EvidenceItem]
    executive_summary: list[str]
    related_people: list[EvidenceItem]
    related_projects: list[EvidenceItem]
    related_companies: list[EvidenceItem]
    related_objectives: list[EvidenceItem]
    related_decisions: list[EvidenceItem]
    risks: list[str]
    open_loops: list[EvidenceItem]
    follow_ups: list[EvidenceItem]
    recommended_discussion: list[str]
    confidence: str
    confidence_reason: str
    evidence_note_count: int


def build_meeting_brief(subject: str, vault_root: Path | None = None) -> MeetingBrief:
    if not subject or not subject.strip():
        raise ValueError("Meeting subject is required.")

    resolved_vault = resolve_live_vault_path(vault_root)
    notes = load_vault(resolved_vault)
    entities = extract_entities(resolved_vault)
    resolution_index = build_resolution_index(entities)
    graph = build_graph(entities, resolution_index)

    note_lookup = {note.path: note for note in notes}
    entity_lookup = {entity.id: entity for entity in entities}
    subject_key = normalise_name(subject)

    seed_entities = _find_seed_entities(subject, entities)
    seed_ids = {entity.id for entity in seed_entities}

    context_notes = _find_context_notes(subject, notes, seed_entities)
    context_note_paths = {note.path for note in context_notes}

    related_entities = _collect_related_entities(
        subject=subject,
        context_notes=context_notes,
        seed_entities=seed_entities,
        seed_ids=seed_ids,
        entities=entities,
        entity_lookup=entity_lookup,
        resolution_index=resolution_index,
        graph=graph,
    )

    matched_entities = [
        EvidenceItem(
            title=entity.title,
            path=entity.path,
            kind=entity.type,
            reason="Matched meeting subject.",
        )
        for entity in seed_entities
    ]

    executive_summary = _build_executive_summary(subject, seed_entities, context_notes, related_entities)
    risks = _build_risks(seed_entities, related_entities, note_lookup, graph, entities)

    open_loops = _build_note_items(
        [note for note in context_notes if note.kind == "open_loop"],
        "Direct note mention.",
    )
    follow_ups = _build_note_items(
        [note for note in context_notes if note.kind == "follow_up"],
        "Direct note mention.",
    )

    recommended_discussion = _build_recommended_discussion(
        subject=subject.strip(),
        related_entities=related_entities,
        risks=risks,
        follow_ups=follow_ups,
        open_loops=open_loops,
    )

    confidence, confidence_reason = _build_confidence(
        seed_entities=seed_entities,
        context_note_count=len(context_note_paths),
        related_entity_count=len(related_entities),
    )

    return MeetingBrief(
        subject=subject.strip(),
        generated_at=datetime.now(timezone.utc).isoformat(),
        matched_entities=matched_entities,
        executive_summary=executive_summary,
        related_people=_build_entity_items(related_entities, "person"),
        related_projects=_build_entity_items(related_entities, "project"),
        related_companies=_build_entity_items(related_entities, "company"),
        related_objectives=_build_entity_items(related_entities, "objective"),
        related_decisions=_build_entity_items(related_entities, "decision"),
        risks=risks,
        open_loops=open_loops,
        follow_ups=follow_ups,
        recommended_discussion=recommended_discussion,
        confidence=confidence,
        confidence_reason=confidence_reason,
        evidence_note_count=len(context_note_paths),
    )


def render_meeting_brief(brief: MeetingBrief) -> str:
    matched = ", ".join(f"{item.title} ({item.kind})" for item in brief.matched_entities) or "No canonical entity matched"

    parts = [
        f"# Meeting Brief - {brief.subject}",
        "",
        "## Meeting",
        "",
        f"- Subject: {brief.subject}",
        f"- Generated: {brief.generated_at}",
        f"- Matched Entities: {matched}",
        f"- Evidence Notes Reviewed: {brief.evidence_note_count}",
        "",
        "## Executive Summary",
        "",
    ]

    parts.extend(_render_bullets(brief.executive_summary))
    parts.extend(["", "## Related People", ""])
    parts.extend(_render_items(brief.related_people))
    parts.extend(["", "## Related Projects", ""])
    parts.extend(_render_items(brief.related_projects))
    parts.extend(["", "## Related Companies", ""])
    parts.extend(_render_items(brief.related_companies))
    parts.extend(["", "## Related Objectives", ""])
    parts.extend(_render_items(brief.related_objectives))
    parts.extend(["", "## Related Decisions", ""])
    parts.extend(_render_items(brief.related_decisions))
    parts.extend(["", "## Risks", ""])
    parts.extend(_render_bullets(brief.risks))
    parts.extend(["", "## Open Loops", ""])
    parts.extend(_render_items(brief.open_loops))
    parts.extend(["", "## Follow-ups", ""])
    parts.extend(_render_items(brief.follow_ups))
    parts.extend(["", "## Recommended Discussion", ""])
    parts.extend(_render_bullets(brief.recommended_discussion))
    parts.extend(
        [
            "",
            "## Confidence",
            "",
            f"- Rating: {brief.confidence}",
            f"- Basis: {brief.confidence_reason}",
            "",
        ]
    )

    return "\n".join(parts)


def _render_bullets(values: Iterable[str]) -> list[str]:
    items = [f"- {value}" for value in values if value]
    return items or ["_None found._"]


def _render_items(values: Iterable[EvidenceItem]) -> list[str]:
    items = [
        f"- {value.title} ({value.kind}) - {value.reason} [{value.path}]"
        for value in values
    ]
    return items or ["_None found._"]


def _find_seed_entities(subject: str, entities: list) -> list:
    subject_key = normalise_name(subject)
    exact = [
        entity
        for entity in entities
        if normalise_name(entity.title) == subject_key
        or normalise_name(Path(entity.path).stem) == subject_key
    ]
    if exact:
        return sorted(exact, key=lambda entity: (entity.type, entity.path))

    subject_parts = subject_key.split()
    partial = []
    for entity in entities:
        entity_key = normalise_name(entity.title)
        if subject_key in entity_key or all(part in entity_key for part in subject_parts):
            partial.append(entity)
    return sorted(partial, key=lambda entity: (entity.type, entity.path))[:10]


def _find_context_notes(subject: str, notes: list[VaultNote], seed_entities: list) -> list[VaultNote]:
    subject_pattern = re.compile(rf"\b{re.escape(subject.strip())}\b", re.IGNORECASE)
    seed_titles = {entity.title for entity in seed_entities}
    seed_paths = {entity.path for entity in seed_entities}

    context = []
    for note in notes:
        if note.path in seed_paths or note.title in seed_titles:
            context.append(note)
            continue
        if subject_pattern.search(note.title) or subject_pattern.search(note.path) or subject_pattern.search(note.text):
            context.append(note)

    return sorted(context, key=lambda note: (note.kind, note.path))


def _collect_related_entities(
    *,
    subject: str,
    context_notes: list[VaultNote],
    seed_entities: list,
    seed_ids: set[str],
    entities: list,
    entity_lookup: dict,
    resolution_index: dict,
    graph: dict,
) -> list[tuple]:
    reasons: dict[str, set[str]] = {}

    def add_entity(entity_id: str, reason: str) -> None:
        if entity_id in seed_ids or entity_id not in entity_lookup:
            return
        reasons.setdefault(entity_id, set()).add(reason)

    for edge in graph["edges"]:
        if edge["source"] in seed_ids:
            add_entity(edge["target"], f"Explicit link from {entity_lookup[edge['source']].title}.")
        if edge["target"] in seed_ids:
            add_entity(edge["source"], f"Backlink to {entity_lookup[edge['target']].title}.")

    for note in context_notes:
        if note.kind in {"person", "project", "company", "objective", "decision"} and note.path in entity_lookup:
            add_entity(note.path, "Direct note mention.")

        for link in extract_links(note.text):
            resolved = resolve_link_with_index(link, resolution_index)
            if resolved is None:
                continue
            add_entity(resolved.id, f"Linked from context note {note.title}.")

    subject_key = normalise_name(subject)
    for entity in entities:
        if entity.id in seed_ids:
            continue
        haystacks = [entity.title, entity.path]
        if any(subject_key in normalise_name(value) for value in haystacks):
            add_entity(entity.id, "Name overlap with meeting subject.")

    ranked = []
    for entity_id, entity_reasons in reasons.items():
        entity = entity_lookup[entity_id]
        score = len(entity_reasons) * 10
        score += len(entity.links)
        ranked.append((score, entity, sorted(entity_reasons)))

    ranked.sort(key=lambda item: (-item[0], item[1].type, item[1].title, item[1].path))
    return ranked[:50]


def _build_entity_items(related_entities: list[tuple], entity_type: str) -> list[EvidenceItem]:
    items = []
    for _, entity, reasons in related_entities:
        if entity.type != entity_type:
            continue
        items.append(
            EvidenceItem(
                title=entity.title,
                path=entity.path,
                kind=entity.type,
                reason="; ".join(reasons[:2]),
            )
        )
    return items[:10]


def _build_note_items(notes: list[VaultNote], reason: str) -> list[EvidenceItem]:
    items = []
    for note in notes[:10]:
        items.append(
            EvidenceItem(
                title=note.title,
                path=note.path,
                kind=note.kind,
                reason=reason,
            )
        )
    return items


def _build_executive_summary(subject: str, seed_entities: list, context_notes: list[VaultNote], related_entities: list[tuple]) -> list[str]:
    summary = []

    if seed_entities:
        seed_types = ", ".join(sorted({entity.type for entity in seed_entities}))
        summary.append(f"{subject} matches {len(seed_entities)} vault entities across: {seed_types}.")
    else:
        summary.append(f"No canonical vault entity matched {subject}; this brief is based on direct note mentions.")

    linked_counts = {}
    for _, entity, _ in related_entities:
        linked_counts[entity.type] = linked_counts.get(entity.type, 0) + 1

    if linked_counts:
        ordered = ", ".join(f"{count} {kind}" for kind, count in sorted(linked_counts.items()))
        summary.append(f"Related evidence found across {ordered} records.")

    salient = []
    for entity in seed_entities:
        note = context_notes[0] if context_notes and context_notes[0].path == entity.path else None
        if note is None:
            for candidate in context_notes:
                if candidate.path == entity.path:
                    note = candidate
                    break
        if note is None:
            continue
        salient.extend(_extract_salient_lines(note.text))

    summary.extend(salient[:3])
    return summary[:5]


def _extract_salient_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip().strip("*")
        if not line:
            continue
        if line.startswith(("#", "!", "---")):
            continue
        if line.startswith(("- ", "* ")):
            line = line[2:].strip()
        elif re.match(r"^\d+\.\s+", line):
            line = re.sub(r"^\d+\.\s+", "", line)

        if len(line) < 30:
            continue
        lines.append(_clean_inline_markdown(line))

    deduped = []
    seen = set()
    for line in lines:
        key = normalise_name(line)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(line.rstrip(".") + ".")
    return deduped


def _clean_inline_markdown(value: str) -> str:
    value = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", value)
    value = re.sub(r"\[\[([^\]]+)\]\]", r"\1", value)
    value = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", value)
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _build_risks(seed_entities: list, related_entities: list[tuple], note_lookup: dict[str, VaultNote], graph: dict, entities: list) -> list[str]:
    risks = []
    risk_analysis = analyse_risk(graph, entities)
    seed_titles = {entity.title for entity in seed_entities}
    related_titles = {entity.title for _, entity, _ in related_entities}

    for risk in risk_analysis["all"]:
        if risk["title"] in seed_titles or risk["title"] in related_titles:
            risks.append(f"{risk['title']}: {'; '.join(risk['reasons'])}.")

    for entity in seed_entities:
        note = note_lookup.get(entity.path)
        if note is None:
            continue
        for line in _extract_risk_lines(note.text):
            risks.append(line)

    deduped = []
    seen = set()
    for risk in risks:
        key = normalise_name(risk)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(risk)
    return deduped[:8]


def _extract_risk_lines(text: str) -> list[str]:
    markers = ("risk", "constraint", "issue", "however", "manual", "limited", "responsibility", "reduce need", "no ")
    lines = []
    for raw in text.splitlines():
        line = _clean_inline_markdown(raw.strip(" -"))
        lowered = line.lower()
        if len(line) < 25:
            continue
        if any(marker in lowered for marker in markers):
            lines.append(line.rstrip(".") + ".")
    return lines


def _build_recommended_discussion(
    *,
    subject: str,
    related_entities: list[tuple],
    risks: list[str],
    follow_ups: list[EvidenceItem],
    open_loops: list[EvidenceItem],
) -> list[str]:
    discussion = []

    top_people = [entity.title for _, entity, _ in related_entities if entity.type == "person"][:3]
    if top_people:
        discussion.append(f"Confirm who owns the next {subject} actions across {', '.join(top_people)}.")

    top_objectives = [entity.title for _, entity, _ in related_entities if entity.type == "objective"][:3]
    if top_objectives:
        discussion.append(f"Test whether the meeting outcome advances {', '.join(top_objectives)}.")

    if risks:
        discussion.append(f"Resolve the highest-friction issue first: {risks[0]}")

    if follow_ups:
        discussion.append(f"Review outstanding follow-ups, starting with {follow_ups[0].title}.")

    if open_loops:
        discussion.append(f"Close any open loop that blocks commercial or operational progress, starting with {open_loops[0].title}.")

    return discussion[:5]


def _build_confidence(*, seed_entities: list, context_note_count: int, related_entity_count: int) -> tuple[str, str]:
    if len(seed_entities) >= 1 and context_note_count >= 3 and related_entity_count >= 5:
        return "HIGH", "Canonical entities matched and multiple supporting notes were found."
    if len(seed_entities) >= 1 and context_note_count >= 1:
        return "MEDIUM", "Canonical entities matched, but supporting graph evidence is limited."
    return "LOW", "The brief is based mainly on sparse note mentions rather than strong linked evidence."
