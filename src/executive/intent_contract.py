"""Canonical executive intent contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Any

from executive.knowledge.entity_contract import canonicalise_date
from executive.knowledge.resolver import normalise_name
from src.executive.executive_intelligence import ExecutiveIntelligence, build_executive_intelligence_from_state
from src.executive.read_model import UnifiedExecutiveReadModel, build_unified_executive_read_model
from src.executive.executive_state import ExecutiveState

DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2}|\d{8})\b")


@dataclass(frozen=True)
class CanonicalExecutiveIntent:
    intent_id: str
    intent_type: str
    recommended_action: str
    why_now: str
    source_entities: tuple[str, ...]
    source_work_items: tuple[str, ...]
    priority: str | None
    urgency: str | None
    confidence: str
    owner: str | None
    blockers: tuple[str, ...]
    dependencies: tuple[str, ...]
    evidence_paths: tuple[str, ...]
    expiry: str | None
    provenance: dict[str, tuple[str, ...]] = field(default_factory=dict)
    extensions: dict[str, object] = field(default_factory=dict)


def build_executive_intents_from_state(
    state: ExecutiveState,
    *,
    intelligence: ExecutiveIntelligence | None = None,
    read_model: UnifiedExecutiveReadModel | None = None,
) -> tuple[CanonicalExecutiveIntent, ...]:
    read_model = read_model or build_unified_executive_read_model(state)
    intelligence = intelligence or build_executive_intelligence_from_state(state)
    return build_executive_intents(read_model, intelligence)


def build_executive_intents(
    read_model: UnifiedExecutiveReadModel,
    intelligence: ExecutiveIntelligence,
) -> tuple[CanonicalExecutiveIntent, ...]:
    meeting = read_model.meetings[0] if read_model.meetings else None
    followups = read_model.followups
    open_loops = read_model.open_loops

    candidates = [
        _intent_from_priority(read_model, intelligence.top_priorities[0]) if intelligence.top_priorities and _priority_actionable(intelligence.top_priorities[0]) else None,
        _intent_from_project(read_model, intelligence.projects_at_risk[0]) if intelligence.projects_at_risk else None,
        _intent_from_followup(read_model, intelligence.followups_requiring_action[0]) if intelligence.followups_requiring_action else None,
        _intent_from_open_loop(read_model, intelligence.open_loops[0]) if intelligence.open_loops else None,
        _intent_from_meeting(read_model, meeting) if meeting and meeting.recommended_discussion else None,
        _intent_from_decision(read_model, intelligence.decisions_awaiting_attention[0]) if intelligence.decisions_awaiting_attention else None,
        _intent_from_supplier(read_model, intelligence.supplier_risks[0]) if intelligence.supplier_risks else None,
        _intent_from_priority(read_model, intelligence.top_priorities[1]) if len(intelligence.top_priorities) > 1 and _priority_actionable(intelligence.top_priorities[1]) else None,
        _intent_from_followup(read_model, intelligence.followups_requiring_action[1]) if len(intelligence.followups_requiring_action) > 1 else None,
        _intent_from_open_loop(read_model, intelligence.open_loops[1]) if len(intelligence.open_loops) > 1 else None,
        _intent_from_recommendation(read_model, intelligence.recommended_actions_today[0], "HIGH") if intelligence.recommended_actions_today else None,
        _intent_from_recommendation(read_model, open_loops.recommended_actions[0], "HIGH") if open_loops.recommended_actions else None,
        _intent_from_recommendation(read_model, followups.recommendations[0], "HIGH") if followups.recommendations else None,
    ]

    merged: dict[str, CanonicalExecutiveIntent] = {}
    for intent in candidates:
        if intent is None:
            continue
        key = normalise_name(intent.recommended_action)
        if key not in merged:
            merged[key] = intent
        else:
            merged[key] = _merge_intents(merged[key], intent)

    ordered = sorted(
        merged.values(),
        key=lambda item: (-int(item.extensions.get("score", 0)), item.recommended_action),
    )
    return tuple(ordered[:10])


def intent_to_executive_action(intent: CanonicalExecutiveIntent):
    ExecutiveAction = __import__("src.executive.executive_reasoning", fromlist=["ExecutiveAction"]).ExecutiveAction
    return ExecutiveAction(
        priority=intent.priority or "NONE",
        action=intent.recommended_action,
        why_it_matters=intent.why_now,
        supporting_evidence=_supporting_evidence_text(intent),
        expected_impact=str(intent.extensions.get("expected_impact", "Focuses executive attention on already-evidenced next actions.")),
        confidence=intent.confidence,
        score=int(intent.extensions.get("score", 0)),
    )


def _intent_from_priority(read_model: UnifiedExecutiveReadModel, item) -> CanonicalExecutiveIntent:
    context = getattr(item, "context", {}) or {}
    next_step = _priority_recommended_action(item)
    priority = _priority_level(item)
    score = _priority_score(item)
    evidence_paths = tuple(context.get("evidence_paths") or ())
    owner = context.get("owner")
    status = context.get("status", "ACTIVE")
    timing = context.get("deadline_or_recency")
    why_now_items = tuple(context.get("why_now") or [item.detail])
    source_entities, source_work_items = _resolve_sources(read_model, item.title, context, evidence_paths)
    action = _specific_action_text(entity=item.title, next_step=next_step, status=status, owner=owner, timing=timing)
    why_now = f"{item.title} matters now because " + "; ".join(why_now_items[:3]) + "."
    return _build_intent(
        intent_type="priority",
        recommended_action=action,
        why_now=why_now,
        source_entities=source_entities,
        source_work_items=source_work_items,
        priority=priority,
        urgency=_derive_urgency(priority, timing),
        confidence=str(context.get("confidence", "HIGH" if priority in {"CRITICAL", "HIGH"} else "MEDIUM")),
        owner=owner,
        blockers=why_now_items[:2],
        dependencies=(),
        evidence_paths=evidence_paths,
        expiry=_extract_expiry(timing),
        score=score,
        expected_impact=_expected_impact_text(item.title, status, owner),
    )


def _intent_from_project(read_model: UnifiedExecutiveReadModel, item) -> CanonicalExecutiveIntent:
    context = getattr(item, "context", {}) or {}
    evidence_paths = tuple(context.get("evidence_paths", ()))
    source_entities, source_work_items = _resolve_sources(read_model, item.title, context, evidence_paths)
    return _build_intent(
        intent_type="project",
        recommended_action=_specific_action_text(
            entity=item.title,
            next_step=context.get("next_step", "Review recovery path"),
            status=context.get("status", "AT RISK"),
            owner=context.get("owner"),
            timing=context.get("deadline_or_recency"),
        ),
        why_now=f"{item.title} requires attention now because {item.detail}",
        source_entities=source_entities,
        source_work_items=source_work_items,
        priority="HIGH",
        urgency=_derive_urgency("HIGH", context.get("deadline_or_recency")),
        confidence="HIGH",
        owner=context.get("owner"),
        blockers=(item.detail,),
        dependencies=tuple(context.get("dependencies", ())),
        evidence_paths=evidence_paths,
        expiry=_extract_expiry(context.get("deadline_or_recency")),
        score=92,
        expected_impact="Stops further slippage in project execution and clarifies next steps.",
    )


def _intent_from_followup(read_model: UnifiedExecutiveReadModel, item) -> CanonicalExecutiveIntent:
    context = getattr(item, "context", {}) or {}
    evidence_paths = tuple(context.get("evidence_paths", ()))
    source_entities, source_work_items = _resolve_sources(read_model, item.title, context, evidence_paths)
    return _build_intent(
        intent_type="follow_up",
        recommended_action=_specific_action_text(
            entity=item.title,
            next_step=context.get("next_step", "Close follow-up"),
            status=context.get("status", "HIGH"),
            owner=context.get("owner"),
            timing=context.get("deadline_or_recency"),
        ),
        why_now=f"{item.title} needs action now because {item.detail}",
        source_entities=source_entities,
        source_work_items=source_work_items,
        priority="HIGH",
        urgency=_derive_urgency("HIGH", context.get("deadline_or_recency")),
        confidence="MEDIUM",
        owner=context.get("owner"),
        blockers=(item.detail,),
        dependencies=tuple(context.get("dependencies", ())),
        evidence_paths=evidence_paths,
        expiry=_extract_expiry(context.get("deadline_or_recency")),
        score=88,
        expected_impact="Reduces overdue operational debt and improves execution cadence.",
    )


def _intent_from_open_loop(read_model: UnifiedExecutiveReadModel, item) -> CanonicalExecutiveIntent:
    context = getattr(item, "context", {}) or {}
    evidence_paths = tuple(context.get("evidence_paths", ()))
    source_entities, source_work_items = _resolve_sources(read_model, item.title, context, evidence_paths)
    return _build_intent(
        intent_type="open_loop",
        recommended_action=_specific_action_text(
            entity=item.title,
            next_step=context.get("next_step", "Convert open loop into owned action"),
            status=context.get("status", "OPEN"),
            owner=context.get("owner"),
            timing=context.get("deadline_or_recency"),
        ),
        why_now=f"{item.title} is still unresolved because {item.detail}",
        source_entities=source_entities,
        source_work_items=source_work_items,
        priority="HIGH",
        urgency=_derive_urgency("HIGH", context.get("deadline_or_recency")),
        confidence="HIGH",
        owner=context.get("owner"),
        blockers=(item.detail,),
        dependencies=tuple(context.get("dependencies", ())),
        evidence_paths=evidence_paths,
        expiry=_extract_expiry(context.get("deadline_or_recency")),
        score=90,
        expected_impact="Moves unresolved governance risk into accountable delivery.",
    )


def _intent_from_meeting(read_model: UnifiedExecutiveReadModel, meeting) -> CanonicalExecutiveIntent:
    evidence_paths = tuple(item.path for item in meeting.matched_entities[:3])
    source_entities, source_work_items = _resolve_sources(read_model, meeting.subject, {}, evidence_paths)
    return _build_intent(
        intent_type="meeting",
        recommended_action=f"Prepare {meeting.subject} using {meeting.recommended_discussion[0] if meeting.recommended_discussion else 'the highest-friction evidence item'}",
        why_now=meeting.recommended_discussion[0],
        source_entities=source_entities,
        source_work_items=source_work_items,
        priority="HIGH",
        urgency="TODAY",
        confidence="MEDIUM",
        owner=None,
        blockers=tuple(meeting.risks[:2]),
        dependencies=(),
        evidence_paths=evidence_paths,
        expiry=None,
        score=84,
        expected_impact="Improves meeting quality and turns relationship time into concrete decisions.",
    )


def _intent_from_decision(read_model: UnifiedExecutiveReadModel, item) -> CanonicalExecutiveIntent:
    context = getattr(item, "context", {}) or {}
    evidence_paths = tuple(context.get("evidence_paths", ()))
    source_entities, source_work_items = _resolve_sources(read_model, item.title, context, evidence_paths)
    return _build_intent(
        intent_type="decision",
        recommended_action=_specific_action_text(
            entity=item.title,
            next_step=context.get("next_step", "Resolve decision attention item"),
            status=context.get("status", "ACTIVE"),
            owner=context.get("owner"),
            timing=context.get("deadline_or_recency"),
        ),
        why_now=f"{item.title} needs resolution because {item.detail}",
        source_entities=source_entities,
        source_work_items=source_work_items,
        priority="MEDIUM",
        urgency=_derive_urgency("MEDIUM", context.get("deadline_or_recency")),
        confidence="MEDIUM",
        owner=context.get("owner"),
        blockers=(item.detail,),
        dependencies=tuple(context.get("dependencies", ())),
        evidence_paths=evidence_paths,
        expiry=_extract_expiry(context.get("deadline_or_recency")),
        score=78,
        expected_impact="Prevents unresolved decisions from slowing dependent work.",
    )


def _intent_from_supplier(read_model: UnifiedExecutiveReadModel, item) -> CanonicalExecutiveIntent:
    context = getattr(item, "context", {}) or {}
    evidence_paths = tuple(context.get("evidence_paths", ()))
    source_entities, source_work_items = _resolve_sources(read_model, item.title, context, evidence_paths)
    return _build_intent(
        intent_type="supplier",
        recommended_action=_specific_action_text(
            entity=item.title,
            next_step=context.get("next_step", "Review supplier risk posture"),
            status=context.get("status", "IMPORTANT"),
            owner=context.get("owner"),
            timing=context.get("deadline_or_recency"),
        ),
        why_now=f"{item.title} is elevated because {item.detail}",
        source_entities=source_entities,
        source_work_items=source_work_items,
        priority="MEDIUM",
        urgency=_derive_urgency("MEDIUM", context.get("deadline_or_recency")),
        confidence="MEDIUM",
        owner=context.get("owner"),
        blockers=(item.detail,),
        dependencies=tuple(context.get("dependencies", ())),
        evidence_paths=evidence_paths,
        expiry=_extract_expiry(context.get("deadline_or_recency")),
        score=76,
        expected_impact="Improves third-party governance and narrows compliance exposure.",
    )


def _intent_from_recommendation(read_model: UnifiedExecutiveReadModel, text: str, priority: str) -> CanonicalExecutiveIntent:
    score = 82 if priority == "HIGH" else 70
    return _build_intent(
        intent_type="recommendation",
        recommended_action=text,
        why_now=text,
        source_entities=(),
        source_work_items=(),
        priority=priority,
        urgency=_derive_urgency(priority, None),
        confidence="MEDIUM",
        owner=None,
        blockers=(),
        dependencies=(),
        evidence_paths=(),
        expiry=None,
        score=score,
        expected_impact="Focuses executive attention on already-evidenced next actions.",
    )


def _build_intent(
    *,
    intent_type: str,
    recommended_action: str,
    why_now: str,
    source_entities: tuple[str, ...],
    source_work_items: tuple[str, ...],
    priority: str | None,
    urgency: str | None,
    confidence: str,
    owner: str | None,
    blockers: tuple[str, ...],
    dependencies: tuple[str, ...],
    evidence_paths: tuple[str, ...],
    expiry: str | None,
    score: int,
    expected_impact: str,
) -> CanonicalExecutiveIntent:
    intent_id = _stable_intent_id(intent_type, recommended_action, source_entities, source_work_items)
    provenance = {"evidence_paths": evidence_paths}
    if owner is not None:
        provenance["owner"] = evidence_paths
    if priority is not None:
        provenance["priority"] = evidence_paths
    if urgency is not None:
        provenance["urgency"] = evidence_paths
    if expiry is not None:
        provenance["expiry"] = evidence_paths
    if source_entities:
        provenance["source_entities"] = evidence_paths
    if source_work_items:
        provenance["source_work_items"] = evidence_paths
    return CanonicalExecutiveIntent(
        intent_id=intent_id,
        intent_type=intent_type,
        recommended_action=recommended_action,
        why_now=why_now,
        source_entities=tuple(sorted(source_entities)),
        source_work_items=tuple(sorted(source_work_items)),
        priority=priority,
        urgency=urgency,
        confidence=confidence,
        owner=owner,
        blockers=tuple(item for item in blockers if item),
        dependencies=tuple(item for item in dependencies if item),
        evidence_paths=tuple(sorted(evidence_paths)),
        expiry=expiry,
        provenance=provenance,
        extensions={"score": score, "expected_impact": expected_impact},
    )


def _merge_intents(left: CanonicalExecutiveIntent, right: CanonicalExecutiveIntent) -> CanonicalExecutiveIntent:
    evidence_paths = tuple(sorted(set(left.evidence_paths) | set(right.evidence_paths)))
    source_entities = tuple(sorted(set(left.source_entities) | set(right.source_entities)))
    source_work_items = tuple(sorted(set(left.source_work_items) | set(right.source_work_items)))
    blockers = tuple(dict.fromkeys(left.blockers + right.blockers))
    dependencies = tuple(dict.fromkeys(left.dependencies + right.dependencies))
    provenance = _merge_provenance(left.provenance, right.provenance)
    score = max(int(left.extensions.get("score", 0)), int(right.extensions.get("score", 0)))
    priority = _max_level(left.priority, right.priority, ("NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL"))
    urgency = _max_level(left.urgency, right.urgency, ("NONE", "LOW", "MEDIUM", "HIGH", "TODAY", "URGENT"))
    confidence = _max_level(left.confidence, right.confidence, ("LOW", "MEDIUM", "HIGH"))
    owner = left.owner or right.owner
    expiry = _earliest_date(left.expiry, right.expiry)
    why_now = left.why_now if left.why_now == right.why_now else f"{left.why_now.rstrip('.')} ; {right.why_now}"
    return CanonicalExecutiveIntent(
        intent_id=_stable_intent_id(left.intent_type, left.recommended_action, source_entities, source_work_items),
        intent_type=left.intent_type,
        recommended_action=left.recommended_action,
        why_now=why_now,
        source_entities=source_entities,
        source_work_items=source_work_items,
        priority=None if priority == "NONE" else priority,
        urgency=None if urgency == "NONE" else urgency,
        confidence=confidence,
        owner=owner,
        blockers=blockers,
        dependencies=dependencies,
        evidence_paths=evidence_paths,
        expiry=expiry,
        provenance=provenance,
        extensions={
            "score": score,
            "expected_impact": left.extensions.get("expected_impact") or right.extensions.get("expected_impact"),
        },
    )


def _merge_provenance(left: dict[str, tuple[str, ...]], right: dict[str, tuple[str, ...]]) -> dict[str, tuple[str, ...]]:
    keys = set(left) | set(right)
    return {
        key: tuple(sorted(set(left.get(key, ())) | set(right.get(key, ()))))
        for key in keys
    }


def _resolve_sources(
    read_model: UnifiedExecutiveReadModel,
    title: str,
    context: dict[str, Any],
    evidence_paths: tuple[str, ...],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    entity_ids = set()
    work_item_ids = set()
    contract_entity_id = context.get("contract_entity_id")
    if contract_entity_id:
        entity_ids.add(str(contract_entity_id))
    for entity in read_model.entities:
        if entity.canonical_name == title or entity.primary_path in evidence_paths:
            entity_ids.add(entity.entity_id)
    for item in read_model.work_items:
        if item.title == title or any(path in item.evidence_paths for path in evidence_paths):
            work_item_ids.add(item.work_item_id)
    return tuple(sorted(entity_ids)), tuple(sorted(work_item_ids))


def _supporting_evidence_text(intent: CanonicalExecutiveIntent) -> str:
    if intent.evidence_paths:
        title = intent.extensions.get("entity_title") or intent.recommended_action
        return f"{title} is evidenced by {', '.join(intent.evidence_paths[:3])}. {intent.why_now}"
    return intent.why_now


def _specific_action_text(*, entity: str, next_step: str, status: str | None, owner: str | None, timing: str | None) -> str:
    qualifiers = []
    if status:
        qualifiers.append(status)
    if owner:
        qualifiers.append(f"owner {owner}")
    if timing:
        qualifiers.append(timing)
    qualifier_text = f" ({'; '.join(qualifiers)})" if qualifiers else ""
    return f"{next_step} for {entity}{qualifier_text}"


def _expected_impact_text(entity: str, status: str | None, owner: str | None) -> str:
    owner_text = f" and clarifies accountability with {owner}" if owner else ""
    status_text = f"{status.lower()} exposure" if status else "delivery exposure"
    return f"Reduces {status_text} for {entity}{owner_text}."


def _priority_actionable(item) -> bool:
    return _priority_score(item) >= 40 and _priority_level(item) in {"CRITICAL", "HIGH", "MEDIUM"}


def _priority_match(item) -> re.Match[str] | None:
    detail = getattr(item, "detail", "")
    return re.match(r"^(?P<priority>[A-Z]+) score (?P<score>\d+)\.\s*(?P<action>.+)$", detail)


def _priority_score(item) -> int:
    context = getattr(item, "context", {}) or {}
    if "priority_score" in context:
        return int(context["priority_score"])
    match = _priority_match(item)
    return int(match.group("score")) if match else 0


def _priority_level(item) -> str:
    context = getattr(item, "context", {}) or {}
    if "priority" in context:
        return str(context["priority"])
    match = _priority_match(item)
    return match.group("priority") if match else "LOW"


def _priority_recommended_action(item) -> str:
    context = getattr(item, "context", {}) or {}
    if "next_step" in context:
        return str(context["next_step"])
    match = _priority_match(item)
    return match.group("action") if match else "Review and confirm executive treatment"


def _derive_urgency(priority: str | None, timing: str | None) -> str | None:
    expiry = _extract_expiry(timing)
    if expiry:
        return "TODAY" if expiry <= "2026-07-08" else "HIGH"
    if priority in {"CRITICAL", "HIGH"}:
        return "HIGH"
    if priority == "MEDIUM":
        return "MEDIUM"
    if priority == "LOW":
        return "LOW"
    return None


def _extract_expiry(timing: str | None) -> str | None:
    if not timing:
        return None
    match = DATE_RE.search(str(timing))
    return canonicalise_date(match.group(1)) if match else None


def _earliest_date(left: str | None, right: str | None) -> str | None:
    dates = [item for item in (left, right) if item]
    return min(dates) if dates else None


def _max_level(left: str | None, right: str | None, order: tuple[str, ...]) -> str:
    rank = {value: index for index, value in enumerate(order)}
    left_key = left or order[0]
    right_key = right or order[0]
    return left_key if rank[left_key] >= rank[right_key] else right_key


def _stable_intent_id(
    intent_type: str,
    recommended_action: str,
    source_entities: tuple[str, ...],
    source_work_items: tuple[str, ...],
) -> str:
    source_key = "::".join(sorted(source_entities + source_work_items))
    base = f"{intent_type}::{normalise_name(recommended_action)}"
    return f"{base}::{source_key}" if source_key else base
