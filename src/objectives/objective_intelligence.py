"""Dedicated objective intelligence report for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
from typing import Iterable

from src.executive.knowledge_engine import ExecutiveState, build_executive_state
from src.followups.followup_intelligence import FollowupItem

SECTION_HEADINGS = [
    "Executive Summary",
    "Strategic Objectives",
    "Objectives At Risk",
    "Objectives Without Supporting Projects",
    "Objectives With Stale Evidence",
    "Projects Supporting Objectives",
    "Decisions Linked To Objectives",
    "Follow-ups Linked To Objectives",
    "Recommended Actions",
]

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_ROOT = ROOT / "evidence" / "alfred-inventory"
STALE_AFTER_DAYS = 30
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2}|20\d{6})")


@dataclass(frozen=True)
class ObjectiveLineItem:
    title: str
    detail: str


@dataclass(frozen=True)
class ObjectiveIntelligence:
    executive_summary: list[str]
    strategic_objectives: list[ObjectiveLineItem]
    objectives_at_risk: list[ObjectiveLineItem]
    objectives_without_supporting_projects: list[ObjectiveLineItem]
    objectives_with_stale_evidence: list[ObjectiveLineItem]
    projects_supporting_objectives: list[ObjectiveLineItem]
    decisions_linked_to_objectives: list[ObjectiveLineItem]
    followups_linked_to_objectives: list[ObjectiveLineItem]
    recommended_actions: list[str]


def build_objective_intelligence(
    evidence_root: Path,
    *,
    today: date | None = None,
) -> ObjectiveIntelligence:
    state = build_executive_state(evidence_root)
    return build_objective_intelligence_from_state(state, today=today)


def build_objective_intelligence_from_state(
    state: ExecutiveState,
    *,
    today: date | None = None,
) -> ObjectiveIntelligence:
    effective_today = today or date.today()
    objective_views = _build_objective_views(state, effective_today)

    strategic = [
        ObjectiveLineItem(
            view.objective.title,
            f"{view.objective.status}; linked entities {view.objective.linked_entities}; path {view.objective.path}.",
        )
        for view in objective_views
    ][:10]
    at_risk = [
        ObjectiveLineItem(view.objective.title, f"{view.objective.status}. {view.objective.recommendation}")
        for view in objective_views
        if view.objective.status in {"AT RISK", "WATCH"}
    ][:10]
    without_projects = [
        ObjectiveLineItem(
            view.objective.title,
            "No linked project entities were found in the executive knowledge graph.",
        )
        for view in objective_views
        if not view.project_entities
    ][:10]
    stale = [
        ObjectiveLineItem(
            view.objective.title,
            f"Latest dated supporting evidence is {view.latest_evidence_date.isoformat()}, which is older than {STALE_AFTER_DAYS} days.",
        )
        for view in objective_views
        if view.latest_evidence_date is not None and (effective_today - view.latest_evidence_date).days >= STALE_AFTER_DAYS
    ][:10]
    supporting_projects = _build_supporting_projects(objective_views)
    decisions = _build_linked_decisions(objective_views, state)
    followups = _build_linked_followups(objective_views)
    actions = _build_recommended_actions(objective_views, without_projects, stale, followups)
    summary = _build_summary(state, objective_views, at_risk, without_projects, stale, followups)

    return ObjectiveIntelligence(
        executive_summary=summary,
        strategic_objectives=strategic,
        objectives_at_risk=at_risk,
        objectives_without_supporting_projects=without_projects,
        objectives_with_stale_evidence=stale,
        projects_supporting_objectives=supporting_projects,
        decisions_linked_to_objectives=decisions,
        followups_linked_to_objectives=followups,
        recommended_actions=actions,
    )


def render_objective_intelligence(report: ObjectiveIntelligence) -> str:
    parts = ["# Objective Intelligence", ""]
    parts.extend(["## Executive Summary", ""])
    parts.extend(_render_bullets(report.executive_summary))
    parts.extend(["", "## Strategic Objectives", ""])
    parts.extend(_render_items(report.strategic_objectives))
    parts.extend(["", "## Objectives At Risk", ""])
    parts.extend(_render_items(report.objectives_at_risk))
    parts.extend(["", "## Objectives Without Supporting Projects", ""])
    parts.extend(_render_items(report.objectives_without_supporting_projects))
    parts.extend(["", "## Objectives With Stale Evidence", ""])
    parts.extend(_render_items(report.objectives_with_stale_evidence))
    parts.extend(["", "## Projects Supporting Objectives", ""])
    parts.extend(_render_items(report.projects_supporting_objectives))
    parts.extend(["", "## Decisions Linked To Objectives", ""])
    parts.extend(_render_items(report.decisions_linked_to_objectives))
    parts.extend(["", "## Follow-ups Linked To Objectives", ""])
    parts.extend(_render_items(report.followups_linked_to_objectives))
    parts.extend(["", "## Recommended Actions", ""])
    parts.extend(_render_bullets(report.recommended_actions))
    parts.append("")
    return "\n".join(parts)


@dataclass(frozen=True)
class ObjectiveView:
    objective: object
    linked_entities: tuple[object, ...]
    project_entities: tuple[object, ...]
    decision_entities: tuple[object, ...]
    followups: tuple[FollowupItem, ...]
    latest_evidence_date: date | None


def _build_objective_views(state: ExecutiveState, today: date) -> list[ObjectiveView]:
    entity_lookup = {entity.id: entity for entity in state.entities}
    followups = _all_followups(state)
    views = []

    for objective in sorted(state.objectives, key=lambda item: item.title.lower()):
        linked_entities = tuple(
            entity_lookup[entity_id]
            for entity_id in state.neighbours.get(objective.path, ())
            if entity_id in entity_lookup
        )
        project_entities = tuple(entity for entity in linked_entities if entity.type == "project")
        decision_entities = tuple(entity for entity in linked_entities if entity.type == "decision")
        related_followups = tuple(
            item
            for item in followups
            if item.path == objective.path or _mentions_objective(item, objective.title)
        )
        latest_evidence_date = _latest_date(objective, linked_entities, related_followups)
        views.append(
            ObjectiveView(
                objective=objective,
                linked_entities=linked_entities,
                project_entities=project_entities,
                decision_entities=decision_entities,
                followups=related_followups,
                latest_evidence_date=latest_evidence_date,
            )
        )
    return views


def _build_supporting_projects(objective_views: list[ObjectiveView]) -> list[ObjectiveLineItem]:
    items: list[ObjectiveLineItem] = []
    for view in objective_views:
        for entity in view.project_entities:
            items.append(
                ObjectiveLineItem(
                    entity.title,
                    f"Supports {view.objective.title}; source {entity.path}.",
                )
            )
    return _dedupe_items(items)[:10]


def _build_linked_decisions(objective_views: list[ObjectiveView], state: ExecutiveState) -> list[ObjectiveLineItem]:
    decision_lookup = {decision["title"]: decision for decision in state.vault.get("decisions", {}).get("top_decisions", [])}
    items: list[ObjectiveLineItem] = []
    for view in objective_views:
        for entity in view.decision_entities:
            decision = decision_lookup.get(entity.title)
            if decision is None:
                detail = f"Linked to {view.objective.title}; source {entity.path}."
            else:
                detail = (
                    f"Linked to {view.objective.title}; importance {decision['importance']}; "
                    f"projects {decision['projects']}; objectives {decision['objectives']}."
                )
            items.append(ObjectiveLineItem(entity.title, detail))
    return _dedupe_items(items)[:10]


def _build_linked_followups(objective_views: list[ObjectiveView]) -> list[ObjectiveLineItem]:
    items: list[ObjectiveLineItem] = []
    for view in objective_views:
        for followup in view.followups:
            due = followup.due_date or "no explicit due date"
            items.append(
                ObjectiveLineItem(
                    view.objective.title,
                    f"{followup.summary} Due: {due}; Priority: {followup.priority}; Source: {followup.path}.",
                )
            )
    return _dedupe_items(items)[:10]


def _build_recommended_actions(
    objective_views: list[ObjectiveView],
    without_projects: list[ObjectiveLineItem],
    stale: list[ObjectiveLineItem],
    followups: list[ObjectiveLineItem],
) -> list[str]:
    actions = []
    at_risk_count = sum(1 for view in objective_views if view.objective.status in {"AT RISK", "WATCH"})
    if at_risk_count:
        actions.append(f"Review the {at_risk_count} objectives currently flagged AT RISK or WATCH.")
    if without_projects:
        actions.append(f"Link active projects to the {len(without_projects)} objectives that currently have no supporting project traceability.")
    if stale:
        actions.append(f"Refresh evidence or status updates for the {len(stale)} objectives with stale dated support.")
    if followups:
        actions.append(f"Close or re-sequence the {len(followups)} follow-ups that are explicitly linked to objective work.")
    if not actions:
        actions.append("Objective coverage is current; preserve the existing evidence and ownership model.")
    return actions[:5]


def _build_summary(
    state: ExecutiveState,
    objective_views: list[ObjectiveView],
    at_risk: list[ObjectiveLineItem],
    without_projects: list[ObjectiveLineItem],
    stale: list[ObjectiveLineItem],
    followups: list[ObjectiveLineItem],
) -> list[str]:
    supported = state.vault.get("objectives", {}).get("supported", 0)
    return [
        f"Objectives analysed: {len(objective_views)}; supported: {supported}; at risk or watch: {len(at_risk)}.",
        f"Objectives without linked projects: {len(without_projects)}; stale evidence: {len(stale)}.",
        f"Linked follow-ups found: {len(followups)}; overall objective confidence: {state.confidence}.",
    ]


def _all_followups(state: ExecutiveState) -> tuple[FollowupItem, ...]:
    seen = set()
    items = []
    for group in (
        state.followups.overdue,
        state.followups.due_today,
        state.followups.due_this_week,
        state.followups.waiting_on_others,
        state.followups.high_priority,
    ):
        for item in group:
            key = (item.path, item.summary)
            if key in seen:
                continue
            seen.add(key)
            items.append(item)
    return tuple(items)


def _mentions_objective(followup: FollowupItem, objective_title: str) -> bool:
    objective_key = _normalise(objective_title)
    return objective_key and objective_key in _normalise(f"{followup.title} {followup.summary} {followup.path}")


def _latest_date(objective: object, linked_entities: tuple[object, ...], followups: tuple[FollowupItem, ...]) -> date | None:
    candidates: list[date] = []
    for value in [objective.path, objective.title]:
        extracted = _extract_dates(value)
        candidates.extend(extracted)
    for entity in linked_entities:
        candidates.extend(_extract_dates(entity.path))
        candidates.extend(_extract_dates(entity.title))
    for item in followups:
        candidates.extend(_extract_dates(item.path))
        candidates.extend(_extract_dates(item.title))
        candidates.extend(_extract_dates(item.summary))
        if item.due_date:
            try:
                candidates.append(date.fromisoformat(item.due_date))
            except ValueError:
                pass
    return max(candidates) if candidates else None


def _extract_dates(value: str) -> list[date]:
    dates = []
    for match in DATE_RE.findall(value):
        try:
            if "-" in match:
                dates.append(date.fromisoformat(match))
            elif len(match) == 8:
                dates.append(date.fromisoformat(f"{match[:4]}-{match[4:6]}-{match[6:]}"))
        except ValueError:
            continue
    return dates


def _dedupe_items(items: list[ObjectiveLineItem]) -> list[ObjectiveLineItem]:
    deduped = []
    seen = set()
    for item in sorted(items, key=lambda current: (current.title.lower(), current.detail)):
        key = (item.title, item.detail)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _render_items(values: Iterable[ObjectiveLineItem]) -> list[str]:
    rendered = [f"- {value.title}: {value.detail}" for value in values]
    return rendered or ["_None found._"]


def _render_bullets(values: Iterable[str]) -> list[str]:
    rendered = [f"- {value}" for value in values if value]
    return rendered or ["_None found._"]
