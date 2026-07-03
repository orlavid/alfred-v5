"""Objective and project spine report for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from src.executive.knowledge_engine import ExecutiveState, build_executive_state
from src.objectives.objective_intelligence import (
    ObjectiveView,
    build_objective_views_from_state,
)

SECTION_HEADINGS = [
    "Executive Summary",
    "Objective to Project Traceability",
    "Orphan Projects",
    "Objectives Without Projects",
    "Objective Dependency Graph",
    "Objective Health Scores",
    "Objective Review Cadence",
    "Recommended Actions",
]

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_ROOT = ROOT / "evidence" / "alfred-inventory"


@dataclass(frozen=True)
class SpineLineItem:
    title: str
    detail: str


@dataclass(frozen=True)
class ObjectiveProjectSpine:
    executive_summary: list[str]
    objective_to_project_traceability: list[SpineLineItem]
    orphan_projects: list[SpineLineItem]
    objectives_without_projects: list[SpineLineItem]
    objective_dependency_graph: list[SpineLineItem]
    objective_health_scores: list[SpineLineItem]
    objective_review_cadence: list[SpineLineItem]
    recommended_actions: list[str]


def build_objective_project_spine(
    evidence_root: Path,
    *,
    today: date | None = None,
) -> ObjectiveProjectSpine:
    state = build_executive_state(evidence_root)
    return build_objective_project_spine_from_state(state, today=today)


def build_objective_project_spine_from_state(
    state: ExecutiveState,
    *,
    today: date | None = None,
) -> ObjectiveProjectSpine:
    effective_today = today or date.today()
    objective_views = build_objective_views_from_state(state, today=effective_today)
    traceability = _build_traceability(objective_views)
    orphan_projects = _build_orphan_projects(state)
    objectives_without_projects = _build_objectives_without_projects(objective_views)
    dependency_graph = _build_dependency_graph(objective_views)
    health_scores = _build_health_scores(objective_views)
    review_cadence = _build_review_cadence(objective_views, effective_today)
    summary = _build_summary(
        objective_views=objective_views,
        traceability=traceability,
        orphan_projects=orphan_projects,
        without_projects=objectives_without_projects,
        review_cadence=review_cadence,
    )
    actions = _build_actions(
        orphan_projects=orphan_projects,
        without_projects=objectives_without_projects,
        review_cadence=review_cadence,
        dependency_graph=dependency_graph,
    )

    return ObjectiveProjectSpine(
        executive_summary=summary,
        objective_to_project_traceability=traceability,
        orphan_projects=orphan_projects,
        objectives_without_projects=objectives_without_projects,
        objective_dependency_graph=dependency_graph,
        objective_health_scores=health_scores,
        objective_review_cadence=review_cadence,
        recommended_actions=actions,
    )


def render_objective_project_spine(report: ObjectiveProjectSpine) -> str:
    parts = ["# Objective Project Spine", ""]
    parts.extend(["## Executive Summary", ""])
    parts.extend(_render_bullets(report.executive_summary))
    parts.extend(["", "## Objective to Project Traceability", ""])
    parts.extend(_render_items(report.objective_to_project_traceability))
    parts.extend(["", "## Orphan Projects", ""])
    parts.extend(_render_items(report.orphan_projects))
    parts.extend(["", "## Objectives Without Projects", ""])
    parts.extend(_render_items(report.objectives_without_projects))
    parts.extend(["", "## Objective Dependency Graph", ""])
    parts.extend(_render_items(report.objective_dependency_graph))
    parts.extend(["", "## Objective Health Scores", ""])
    parts.extend(_render_items(report.objective_health_scores))
    parts.extend(["", "## Objective Review Cadence", ""])
    parts.extend(_render_items(report.objective_review_cadence))
    parts.extend(["", "## Recommended Actions", ""])
    parts.extend(_render_bullets(report.recommended_actions))
    parts.append("")
    return "\n".join(parts)


def _build_traceability(objective_views: list[ObjectiveView]) -> list[SpineLineItem]:
    items = []
    for view in objective_views:
        projects = ", ".join(entity.title for entity in view.project_entities) or "None"
        items.append(
            SpineLineItem(
                view.objective.title,
                f"Projects: {projects}. Linked entity count: {view.objective.linked_entities}.",
            )
        )
    return items[:10]


def _build_orphan_projects(state: ExecutiveState) -> list[SpineLineItem]:
    project_insights = {project.path: project for project in state.projects}
    entity_lookup = {entity.id: entity for entity in state.entities}
    items = []
    for entity in sorted((item for item in state.entities if item.type == "project"), key=lambda current: current.title.lower()):
        linked = [entity_lookup[entity_id] for entity_id in state.neighbours.get(entity.id, ()) if entity_id in entity_lookup]
        objective_links = [item for item in linked if item.type == "objective"]
        if objective_links:
            continue
        insight = project_insights.get(entity.path)
        if insight is None:
            detail = "No linked objective found in the lightweight graph."
        else:
            detail = f"{insight.status}. {insight.recommendation}"
        items.append(SpineLineItem(entity.title, detail))
    return items[:10]


def _build_objectives_without_projects(objective_views: list[ObjectiveView]) -> list[SpineLineItem]:
    return [
        SpineLineItem(
            view.objective.title,
            "No supporting project links were found from the current objective graph.",
        )
        for view in objective_views
        if not view.project_entities
    ][:10]


def _build_dependency_graph(objective_views: list[ObjectiveView]) -> list[SpineLineItem]:
    items = []
    for view in objective_views:
        dependencies = sorted(entity.title for entity in view.linked_entities if entity.type == "objective" and entity.path != view.objective.path)
        if dependencies:
            detail = f"Depends on or is linked with: {', '.join(dependencies)}."
        else:
            detail = "No explicit objective-to-objective dependencies found in current links. Confidence: LOW."
        items.append(SpineLineItem(view.objective.title, detail))
    return items[:10]


def _build_health_scores(objective_views: list[ObjectiveView]) -> list[SpineLineItem]:
    items = []
    for view in objective_views:
        score = 100
        if view.objective.status == "AT RISK":
            score -= 40
        elif view.objective.status == "WATCH":
            score -= 20
        if not view.project_entities:
            score -= 20
        if not view.decision_entities:
            score -= 10
        if view.stale_evidence:
            score -= 15
        if not view.followups:
            score -= 5
        score = max(0, min(100, score))
        band = "HEALTHY" if score >= 70 else "WATCH" if score >= 40 else "AT RISK"
        detail = (
            f"Score {score}/100 ({band}); projects {len(view.project_entities)}; "
            f"decisions {len(view.decision_entities)}; stale evidence {'YES' if view.stale_evidence else 'NO'}."
        )
        items.append(SpineLineItem(view.objective.title, detail))
    return items[:10]


def _build_review_cadence(objective_views: list[ObjectiveView], today: date) -> list[SpineLineItem]:
    items = []
    for view in objective_views:
        if view.latest_evidence_date is None:
            detail = "No dated evidence found; review status inferred as untracked. Cadence confidence: LOW."
        else:
            age = (today - view.latest_evidence_date).days
            if age <= 30:
                status = "Current"
            elif age <= 60:
                status = "Due Soon"
            else:
                status = "Overdue"
            detail = (
                f"{status}; latest evidence {view.latest_evidence_date.isoformat()}; "
                f"age {age} days. Cadence confidence: LOW."
            )
        items.append(SpineLineItem(view.objective.title, detail))
    return items[:10]


def _build_summary(
    *,
    objective_views: list[ObjectiveView],
    traceability: list[SpineLineItem],
    orphan_projects: list[SpineLineItem],
    without_projects: list[SpineLineItem],
    review_cadence: list[SpineLineItem],
) -> list[str]:
    overdue_reviews = sum(1 for item in review_cadence if item.detail.startswith("Overdue"))
    return [
        f"Objectives analysed: {len(objective_views)}; traceability rows: {len(traceability)}.",
        f"Orphan projects: {len(orphan_projects)}; objectives without projects: {len(without_projects)}.",
        f"Review cadence is inferred from latest evidence dates; overdue reviews: {overdue_reviews}.",
    ]


def _build_actions(
    *,
    orphan_projects: list[SpineLineItem],
    without_projects: list[SpineLineItem],
    review_cadence: list[SpineLineItem],
    dependency_graph: list[SpineLineItem],
) -> list[str]:
    actions = []
    overdue_reviews = sum(1 for item in review_cadence if item.detail.startswith("Overdue"))
    missing_dependencies = sum(1 for item in dependency_graph if "No explicit objective-to-objective dependencies found" in item.detail)
    if without_projects:
        actions.append(f"Link projects to the {len(without_projects)} objectives that currently lack delivery traceability.")
    if orphan_projects:
        actions.append(f"Review {len(orphan_projects)} orphan projects and either attach them to objectives or retire them.")
    if overdue_reviews:
        actions.append(f"Run an objective review on the {overdue_reviews} objectives with overdue inferred cadence.")
    if missing_dependencies:
        actions.append(f"Capture explicit dependencies for {missing_dependencies} objectives where the lightweight graph is empty.")
    if not actions:
        actions.append("Objective and project traceability is currently sufficient for v1.")
    return actions[:5]


def _render_items(values: Iterable[SpineLineItem]) -> list[str]:
    rendered = [f"- {value.title}: {value.detail}" for value in values]
    return rendered or ["_None found._"]


def _render_bullets(values: Iterable[str]) -> list[str]:
    rendered = [f"- {value}" for value in values if value]
    return rendered or ["_None found._"]
