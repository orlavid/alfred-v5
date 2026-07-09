"""Canonical executive presentation contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.executive.executive_reasoning import ExecutiveReasoning, build_executive_reasoning_from_state
from src.executive.read_model import UnifiedExecutiveReadModel, build_unified_executive_read_model
from src.executive.executive_state import ExecutiveState

SECTION_ORDER = (
    "priorities",
    "objectives",
    "projects",
    "risks",
    "followups",
    "meetings",
    "decisions",
    "recommended_actions",
    "evidence_summaries",
)


@dataclass(frozen=True)
class ExecutivePresentationItem:
    item_id: str
    title: str
    summary: str
    evidence_paths: tuple[str, ...]
    provenance: dict[str, tuple[str, ...]]
    confidence: str
    source_entities: tuple[str, ...] = ()
    source_work_items: tuple[str, ...] = ()
    extensions: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutivePresentationSection:
    section_id: str
    title: str
    items: tuple[ExecutivePresentationItem, ...]
    summary_lines: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutivePresentationContract:
    ordered_sections: tuple[str, ...]
    sections: dict[str, ExecutivePresentationSection]
    confidence: str


def build_executive_presentation_from_state(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
    read_model: UnifiedExecutiveReadModel | None = None,
) -> ExecutivePresentationContract:
    read_model = read_model or build_unified_executive_read_model(state)
    reasoning = reasoning or build_executive_reasoning_from_state(state)

    sections = {
        "priorities": _build_priorities_section(reasoning),
        "objectives": _build_objectives_section(read_model),
        "projects": _build_projects_section(read_model),
        "risks": _build_risks_section(reasoning),
        "followups": _build_followups_section(read_model),
        "meetings": _build_meetings_section(read_model),
        "decisions": _build_decisions_section(reasoning),
        "recommended_actions": _build_recommended_actions_section(reasoning),
        "evidence_summaries": _build_evidence_summaries_section(read_model),
    }
    return ExecutivePresentationContract(
        ordered_sections=SECTION_ORDER,
        sections=sections,
        confidence=reasoning.confidence,
    )


def _build_priorities_section(reasoning: ExecutiveReasoning) -> ExecutivePresentationSection:
    items = tuple(
        ExecutivePresentationItem(
            item_id=intent.intent_id,
            title=intent.recommended_action,
            summary=intent.why_now,
            evidence_paths=intent.evidence_paths,
            provenance=dict(intent.provenance),
            confidence=intent.confidence,
            source_entities=intent.source_entities,
            source_work_items=intent.source_work_items,
            extensions={
                "priority": intent.priority,
                "urgency": intent.urgency,
                "owner": intent.owner,
                "blockers": intent.blockers,
                "dependencies": intent.dependencies,
                "expiry": intent.expiry,
                "intent_type": intent.intent_type,
            },
        )
        for intent in reasoning.intents[:10]
    )
    return ExecutivePresentationSection(
        section_id="priorities",
        title="Priorities",
        items=items,
        summary_lines=tuple(reasoning.key_themes[:2]),
    )


def _build_objectives_section(read_model: UnifiedExecutiveReadModel) -> ExecutivePresentationSection:
    items = tuple(
        ExecutivePresentationItem(
            item_id=f"objective::{item.path}",
            title=item.title,
            summary=f"{item.status}. {item.recommendation}",
            evidence_paths=(item.path,),
            provenance={"status": (item.path,), "recommendation": (item.path,)},
            confidence=getattr(item, "confidence", "MEDIUM"),
            extensions={"status": item.status},
        )
        for item in read_model.objectives[:10]
    )
    return ExecutivePresentationSection("objectives", "Objectives", items)


def _build_projects_section(read_model: UnifiedExecutiveReadModel) -> ExecutivePresentationSection:
    items = tuple(
        ExecutivePresentationItem(
            item_id=f"project::{item.path}",
            title=item.title,
            summary=f"{item.status}. {item.recommendation}",
            evidence_paths=(item.path,),
            provenance={"status": (item.path,), "recommendation": (item.path,)},
            confidence=getattr(item, "confidence", "MEDIUM"),
            extensions={"status": item.status},
        )
        for item in read_model.projects[:10]
    )
    return ExecutivePresentationSection("projects", "Projects", items)


def _build_risks_section(reasoning: ExecutiveReasoning) -> ExecutivePresentationSection:
    items = tuple(
        ExecutivePresentationItem(
            item_id=f"risk::{index}",
            title=value,
            summary=value,
            evidence_paths=(),
            provenance={},
            confidence=reasoning.confidence,
        )
        for index, value in enumerate(reasoning.risks_requiring_immediate_attention[:10], start=1)
    )
    return ExecutivePresentationSection("risks", "Risks", items)


def _build_followups_section(read_model: UnifiedExecutiveReadModel) -> ExecutivePresentationSection:
    followups = read_model.followups
    if followups is None:
        return ExecutivePresentationSection("followups", "Follow-ups", ())
    merged = []
    seen = set()
    for group in (followups.due_today, followups.overdue, followups.high_priority):
        for item in group:
            key = (item.path, item.summary)
            if key in seen:
                continue
            seen.add(key)
            merged.append(item)
    items = tuple(
        ExecutivePresentationItem(
            item_id=f"followup::{item.path}::{item.summary}",
            title=item.summary,
            summary=f"Due: {item.due_date or 'unknown'}; Priority: {item.priority}.",
            evidence_paths=(item.path,),
            provenance={"due_date": (item.path,), "priority": (item.path,)},
            confidence="MEDIUM" if item.due_date or item.priority == "HIGH" else "LOW",
            extensions={"priority": item.priority, "due_date": item.due_date},
        )
        for item in merged[:10]
    )
    return ExecutivePresentationSection("followups", "Follow-ups", items)


def _build_meetings_section(read_model: UnifiedExecutiveReadModel) -> ExecutivePresentationSection:
    items = tuple(
        ExecutivePresentationItem(
            item_id=f"meeting::{item.subject}",
            title=item.subject,
            summary=item.recommended_discussion[0] if item.recommended_discussion else "No evidence found.",
            evidence_paths=tuple(match.path for match in item.matched_entities[:5]),
            provenance={"recommended_discussion": tuple(match.path for match in item.matched_entities[:5])},
            confidence=item.confidence,
            extensions={
                "risks": tuple(item.risks),
                "recommended_discussion": tuple(item.recommended_discussion),
                "related_people": tuple(person.title for person in item.related_people),
                "related_projects": tuple(project.title for project in item.related_projects),
                "related_companies": tuple(company.title for company in item.related_companies),
                "related_objectives": tuple(objective.title for objective in item.related_objectives),
                "related_decisions": tuple(decision.title for decision in item.related_decisions),
                "open_loops": tuple(loop.title for loop in item.open_loops),
                "follow_ups": tuple(followup.title for followup in item.follow_ups),
                "executive_summary": tuple(item.executive_summary),
            },
        )
        for item in read_model.meetings[:5]
    )
    return ExecutivePresentationSection("meetings", "Meetings", items)


def _build_decisions_section(reasoning: ExecutiveReasoning) -> ExecutivePresentationSection:
    items = tuple(
        ExecutivePresentationItem(
            item_id=f"decision::{index}",
            title=value,
            summary=value,
            evidence_paths=(),
            provenance={},
            confidence=reasoning.confidence,
        )
        for index, value in enumerate(reasoning.decisions_required[:10], start=1)
    )
    return ExecutivePresentationSection("decisions", "Decisions", items)


def _build_recommended_actions_section(reasoning: ExecutiveReasoning) -> ExecutivePresentationSection:
    items = tuple(
        ExecutivePresentationItem(
            item_id=intent.intent_id,
            title=intent.recommended_action,
            summary=intent.why_now,
            evidence_paths=intent.evidence_paths,
            provenance=dict(intent.provenance),
            confidence=intent.confidence,
            source_entities=intent.source_entities,
            source_work_items=intent.source_work_items,
            extensions={"priority": intent.priority, "urgency": intent.urgency},
        )
        for intent in reasoning.intents[:10]
    )
    return ExecutivePresentationSection("recommended_actions", "Recommended Actions", items)


def _build_evidence_summaries_section(read_model: UnifiedExecutiveReadModel) -> ExecutivePresentationSection:
    items = tuple(
        ExecutivePresentationItem(
            item_id=summary.subject_id,
            title=summary.title,
            summary=f"{summary.subject_type} with {summary.evidence_count} evidence path(s).",
            evidence_paths=summary.evidence_paths,
            provenance=dict(summary.provenance),
            confidence=summary.confidence,
        )
        for _, summary in sorted(read_model.evidence_summaries.items())[:20]
    )
    return ExecutivePresentationSection("evidence_summaries", "Evidence Summaries", items)
