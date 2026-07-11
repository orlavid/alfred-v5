from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from executive.knowledge.entity_contract import normalise_unknown
from executive.knowledge.resolver import normalise_name
from src.followups.followup_intelligence import FollowupIntelligence, FollowupItem
from src.meeting.meeting_intelligence import EvidenceItem, MeetingBrief
from src.openloops.open_loop_intelligence import OpenLoopIntelligence, OpenLoopItem


@dataclass(frozen=True)
class ExecutiveWorkItemContract:
    work_item_id: str
    work_item_type: str
    title: str
    status: str | None
    priority: str | None
    risk_level: str | None
    owner: str | None
    delegates: tuple[str, ...]
    due_date: str | None
    created: str | None
    last_activity: str | None
    related_entities: tuple[str, ...]
    related_objectives: tuple[str, ...]
    related_projects: tuple[str, ...]
    related_people: tuple[str, ...]
    evidence_paths: tuple[str, ...]
    evidence_count: int
    source_entity_ids: tuple[str, ...]
    confidence: str
    missing_fields: tuple[str, ...]
    provenance: dict[str, tuple[str, ...]] = field(default_factory=dict)
    last_verified: str | None = None
    extensions: dict[str, object] = field(default_factory=dict)


def build_executive_work_items(
    *,
    followups: FollowupIntelligence,
    open_loops: OpenLoopIntelligence,
    meetings: tuple[MeetingBrief, ...],
) -> tuple[ExecutiveWorkItemContract, ...]:
    items: list[ExecutiveWorkItemContract] = []

    grouped_followups: dict[tuple[str, str], tuple[FollowupItem, set[str]]] = {}
    for item in followups.all_items:
        key = (item.path, normalise_name(item.summary))
        grouped_followups.setdefault(key, (item, set()))
    for group_name, group in (
        ("overdue", followups.overdue),
        ("due_today", followups.due_today),
        ("due_this_week", followups.due_this_week),
        ("waiting_on_others", followups.waiting_on_others),
        ("high_priority", followups.high_priority),
    ):
        for item in group:
            key = (item.path, normalise_name(item.summary))
            existing = grouped_followups.get(key)
            if existing is None:
                grouped_followups[key] = (item, {group_name})
            else:
                grouped_followups[key] = (existing[0], existing[1] | {group_name})
    for item, buckets in grouped_followups.values():
        items.append(_followup_to_work_item(item, followups.generated_at, tuple(sorted(buckets))))

    grouped_loops: dict[tuple[str, str], tuple[OpenLoopItem, set[str]]] = {}
    for item in open_loops.all_items:
        key = (item.path, normalise_name(item.summary))
        grouped_loops.setdefault(key, (item, set()))
    for group_name, group in (
        ("critical_open_loops", open_loops.critical_open_loops),
        ("waiting_for", open_loops.waiting_for),
        ("stalled_projects", open_loops.stalled_projects),
        ("missing_decisions", open_loops.missing_decisions),
        ("missing_owners", open_loops.missing_owners),
    ):
        for item in group:
            key = (item.path, normalise_name(item.summary))
            existing = grouped_loops.get(key)
            if existing is None:
                grouped_loops[key] = (item, {group_name})
            else:
                grouped_loops[key] = (existing[0], existing[1] | {group_name})
    for item, buckets in grouped_loops.values():
        items.append(_open_loop_to_work_item(item, open_loops.generated_at, tuple(sorted(buckets))))

    for meeting in meetings:
        items.append(_meeting_to_work_item(meeting))

    items.sort(key=lambda item: (item.work_item_type, item.title.lower(), item.work_item_id))
    return tuple(items)


def project_followups_from_work_items(
    work_items: tuple[ExecutiveWorkItemContract, ...],
    source: FollowupIntelligence,
) -> FollowupIntelligence:
    followup_items = [item for item in work_items if item.work_item_type == "follow_up"]
    overdue = [_work_item_to_followup(item) for item in followup_items if "overdue" in item.extensions.get("buckets", ())]
    due_today = [_work_item_to_followup(item) for item in followup_items if "due_today" in item.extensions.get("buckets", ())]
    due_this_week = [_work_item_to_followup(item) for item in followup_items if "due_this_week" in item.extensions.get("buckets", ())]
    waiting_on_others = [_work_item_to_followup(item) for item in followup_items if "waiting_on_others" in item.extensions.get("buckets", ())]
    high_priority = [_work_item_to_followup(item) for item in followup_items if "high_priority" in item.extensions.get("buckets", ())]

    return FollowupIntelligence(
        generated_at=source.generated_at,
        followup_count=source.followup_count,
        overdue=overdue,
        due_today=due_today,
        due_this_week=due_this_week,
        waiting_on_others=waiting_on_others,
        high_priority=high_priority,
        recommendations=list(source.recommendations),
        executive_summary=list(source.executive_summary),
        all_items=list(source.all_items) if source.all_items else [_work_item_to_followup(item) for item in followup_items],
    )


def project_open_loops_from_work_items(
    work_items: tuple[ExecutiveWorkItemContract, ...],
    source: OpenLoopIntelligence,
) -> OpenLoopIntelligence:
    loop_items = [item for item in work_items if item.work_item_type in {"open_loop", "decision_review"}]
    critical = [_work_item_to_open_loop(item) for item in loop_items if "critical_open_loops" in item.extensions.get("buckets", ())]
    waiting_for = [_work_item_to_open_loop(item) for item in loop_items if "waiting_for" in item.extensions.get("buckets", ())]
    stalled = [_work_item_to_open_loop(item) for item in loop_items if "stalled_projects" in item.extensions.get("buckets", ())]
    missing_decisions = [_work_item_to_open_loop(item) for item in loop_items if "missing_decisions" in item.extensions.get("buckets", ())]
    missing_owners = [_work_item_to_open_loop(item) for item in loop_items if "missing_owners" in item.extensions.get("buckets", ())]

    return OpenLoopIntelligence(
        generated_at=source.generated_at,
        open_loop_count=source.open_loop_count,
        critical_open_loops=critical,
        waiting_for=waiting_for,
        stalled_projects=stalled,
        missing_decisions=missing_decisions,
        missing_owners=missing_owners,
        recommended_actions=list(source.recommended_actions),
        executive_summary=list(source.executive_summary),
        all_items=list(source.all_items) if source.all_items else [_work_item_to_open_loop(item) for item in loop_items if item.work_item_type == "open_loop"],
    )


def _followup_to_work_item(item: FollowupItem, generated_at: str, buckets: tuple[str, ...]) -> ExecutiveWorkItemContract:
    owner = None
    status = "WAITING" if item.waiting_on_others else None
    related_objectives, related_projects, related_people = _related_titles(item.title, item.source_kind)
    related_entities = tuple(value for value in (item.title,) if value)
    missing_fields = _missing_fields(
        owner=owner,
        due_date=item.due_date,
        status=status,
        priority=item.priority,
        related_entities=related_entities,
    )
    return ExecutiveWorkItemContract(
        work_item_id=f"follow_up::{item.path}::{normalise_name(item.summary)}",
        work_item_type="follow_up",
        title=item.summary,
        status=status,
        priority=item.priority,
        risk_level="HIGH" if item.priority == "HIGH" else None,
        owner=owner,
        delegates=(),
        due_date=item.due_date,
        created=None,
        last_activity=None,
        related_entities=related_entities,
        related_objectives=related_objectives,
        related_projects=related_projects,
        related_people=related_people,
        evidence_paths=(item.path,),
        evidence_count=1,
        source_entity_ids=(item.path,),
        confidence="MEDIUM" if item.due_date or item.priority == "HIGH" else "LOW",
        missing_fields=missing_fields,
        provenance=_provenance(
            evidence_paths=(item.path,),
            status=status,
            priority=item.priority,
            due_date=item.due_date,
            related_entities=related_entities,
            related_objectives=related_objectives,
            related_projects=related_projects,
            related_people=related_people,
        ),
        last_verified=generated_at,
        extensions={
            "buckets": buckets,
            "source_kind": item.source_kind,
            "waiting_on_others": item.waiting_on_others,
            "legacy_title": item.title,
        },
    )


def _open_loop_to_work_item(item: OpenLoopItem, generated_at: str, buckets: tuple[str, ...]) -> ExecutiveWorkItemContract:
    owner = normalise_unknown(item.owner)
    related_objectives, related_projects, related_people = _related_titles(item.title, item.source_kind)
    related_entities = tuple(value for value in (item.title,) if value)
    work_item_type = "decision_review" if "missing_decisions" in buckets else "open_loop"
    missing_fields = _missing_fields(
        owner=owner,
        due_date=None,
        status=item.status,
        priority=item.priority,
        related_entities=related_entities,
    )
    return ExecutiveWorkItemContract(
        work_item_id=f"{work_item_type}::{item.path}::{normalise_name(item.summary)}",
        work_item_type=work_item_type,
        title=item.summary if work_item_type == "decision_review" else item.title,
        status=item.status,
        priority=item.priority,
        risk_level=item.priority if item.priority in {"CRITICAL", "HIGH"} else None,
        owner=owner,
        delegates=(),
        due_date=None,
        created=None,
        last_activity=None,
        related_entities=related_entities,
        related_objectives=related_objectives,
        related_projects=related_projects,
        related_people=related_people,
        evidence_paths=(item.path,),
        evidence_count=1,
        source_entity_ids=(item.path,),
        confidence="HIGH" if item.priority in {"CRITICAL", "HIGH"} else "MEDIUM",
        missing_fields=missing_fields,
        provenance=_provenance(
            evidence_paths=(item.path,),
            status=item.status,
            priority=item.priority,
            related_entities=related_entities,
            related_objectives=related_objectives,
            related_projects=related_projects,
            related_people=related_people,
            owner=owner,
        ),
        last_verified=generated_at,
        extensions={
            "buckets": buckets,
            "source_kind": item.source_kind,
            "summary": item.summary,
            "legacy_title": item.title,
        },
    )


def _meeting_to_work_item(meeting: MeetingBrief) -> ExecutiveWorkItemContract:
    related_people = tuple(item.title for item in meeting.related_people)
    related_projects = tuple(item.title for item in meeting.related_projects)
    related_objectives = tuple(item.title for item in meeting.related_objectives)
    related_entities = tuple(
        _dedupe(
            [item.title for item in meeting.matched_entities],
            related_people,
            related_projects,
            tuple(item.title for item in meeting.related_companies),
            related_objectives,
            tuple(item.title for item in meeting.related_decisions),
            tuple(item.title for item in meeting.open_loops),
            tuple(item.title for item in meeting.follow_ups),
        )
    )
    evidence_paths = tuple(
        _dedupe(
            [item.path for item in meeting.matched_entities],
            [item.path for item in meeting.related_people],
            [item.path for item in meeting.related_projects],
            [item.path for item in meeting.related_companies],
            [item.path for item in meeting.related_objectives],
            [item.path for item in meeting.related_decisions],
            [item.path for item in meeting.open_loops],
            [item.path for item in meeting.follow_ups],
        )
    )
    missing_fields = _missing_fields(
        owner=None,
        due_date=None,
        status=None,
        priority=None,
        related_entities=related_entities,
    )
    return ExecutiveWorkItemContract(
        work_item_id=f"meeting::{normalise_name(meeting.subject)}",
        work_item_type="meeting",
        title=meeting.subject,
        status=None,
        priority=None,
        risk_level="HIGH" if meeting.risks else None,
        owner=None,
        delegates=(),
        due_date=None,
        created=None,
        last_activity=None,
        related_entities=related_entities,
        related_objectives=related_objectives,
        related_projects=related_projects,
        related_people=related_people,
        evidence_paths=evidence_paths,
        evidence_count=len(evidence_paths),
        source_entity_ids=tuple(item.path for item in meeting.matched_entities),
        confidence=meeting.confidence,
        missing_fields=missing_fields,
        provenance=_provenance(
            evidence_paths=evidence_paths,
            related_entities=related_entities,
            related_objectives=related_objectives,
            related_projects=related_projects,
            related_people=related_people,
        ),
        last_verified=meeting.generated_at,
        extensions={
            "recommended_discussion": tuple(meeting.recommended_discussion),
            "risks": tuple(meeting.risks),
            "confidence_reason": meeting.confidence_reason,
            "open_loops": tuple(item.title for item in meeting.open_loops),
            "follow_ups": tuple(item.title for item in meeting.follow_ups),
        },
    )


def _work_item_to_followup(item: ExecutiveWorkItemContract) -> FollowupItem:
    return FollowupItem(
        title=str(item.extensions.get("legacy_title", item.title)),
        path=item.evidence_paths[0] if item.evidence_paths else "",
        source_kind=str(item.extensions.get("source_kind", "unknown")),
        due_date=item.due_date,
        priority=item.priority or "NORMAL",
        waiting_on_others=bool(item.extensions.get("waiting_on_others", False)),
        summary=item.title if item.work_item_type == "follow_up" else str(item.extensions.get("summary", item.title)),
    )


def _work_item_to_open_loop(item: ExecutiveWorkItemContract) -> OpenLoopItem:
    return OpenLoopItem(
        title=str(item.extensions.get("legacy_title", item.title)),
        path=item.evidence_paths[0] if item.evidence_paths else "",
        source_kind=str(item.extensions.get("source_kind", "unknown")),
        status=item.status or "OPEN",
        priority=item.priority or "MEDIUM",
        owner=item.owner or "Unknown",
        summary=str(item.extensions.get("summary", item.title)),
    )


def _related_titles(title: str, source_kind: str) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    if source_kind == "objective":
        return (title,), (), ()
    if source_kind == "project":
        return (), (title,), ()
    if source_kind == "person":
        return (), (), (title,)
    return (), (), ()


def _missing_fields(*, owner, due_date, status, priority, related_entities) -> tuple[str, ...]:
    fields = []
    if owner is None:
        fields.append("owner")
    if due_date is None:
        fields.append("due_date")
    if status is None:
        fields.append("status")
    if priority is None:
        fields.append("priority")
    if not related_entities:
        fields.append("related_entities")
    return tuple(fields)


def _provenance(
    *,
    evidence_paths: tuple[str, ...],
    status=None,
    priority=None,
    due_date=None,
    related_entities=(),
    related_objectives=(),
    related_projects=(),
    related_people=(),
    owner=None,
) -> dict[str, tuple[str, ...]]:
    provenance = {
        "evidence_paths": evidence_paths,
    }
    if status is not None:
        provenance["status"] = evidence_paths
    if priority is not None:
        provenance["priority"] = evidence_paths
    if due_date is not None:
        provenance["due_date"] = evidence_paths
    if owner is not None:
        provenance["owner"] = evidence_paths
    if related_entities:
        provenance["related_entities"] = evidence_paths
    if related_objectives:
        provenance["related_objectives"] = evidence_paths
    if related_projects:
        provenance["related_projects"] = evidence_paths
    if related_people:
        provenance["related_people"] = evidence_paths
    return provenance


def _dedupe(*groups: Iterable[str]) -> list[str]:
    values: list[str] = []
    seen = set()
    for group in groups:
        for value in group:
            if not value or value in seen:
                continue
            seen.add(value)
            values.append(value)
    return values
