"""Executive delivery planning for discovered projects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.executive.executive_state import ExecutiveState

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_ROOT = ROOT / "evidence" / "alfred-inventory"


@dataclass(frozen=True)
class ExecutivePlan:
    project_title: str
    goal: str
    phases: tuple[str, ...]
    milestones: tuple[str, ...]
    suggested_owners: tuple[str, ...]
    target_dates: tuple[str, ...]
    dependencies: tuple[str, ...]
    risks: tuple[str, ...]
    success_measures: tuple[str, ...]
    status: str = "Draft"
    can_edit: bool = True
    can_approve: bool = True
    can_reject: bool = True


@dataclass(frozen=True)
class ExecutivePlanningReport:
    summary: tuple[str, ...]
    plans: tuple[ExecutivePlan, ...]


@dataclass(frozen=True)
class ProjectPlanningContext:
    project: Any
    objective_titles: tuple[str, ...]
    person_titles: tuple[str, ...]
    decision_titles: tuple[str, ...]
    risk_titles: tuple[str, ...]
    dependency_titles: tuple[str, ...]


def build_executive_plans(
    evidence_root: Path,
    *,
    today: date | None = None,
) -> ExecutivePlanningReport:
    from src.executive.executive_state import build_executive_state

    state = build_executive_state(evidence_root)
    return build_executive_plans_from_state(state, today=today)


def build_executive_plans_from_state(
    state: ExecutiveState,
    *,
    today: date | None = None,
) -> ExecutivePlanningReport:
    return build_executive_plans_from_inputs(
        projects=state.projects,
        people=state.people,
        entities=state.entities,
        neighbours=state.neighbours,
        project_health=state.project_health,
        today=today,
    )


def build_executive_plans_from_inputs(
    *,
    projects: tuple[Any, ...],
    people: tuple[Any, ...],
    entities: tuple[Any, ...],
    neighbours: dict[str, tuple[str, ...]],
    project_health: dict[str, Any],
    today: date | None = None,
) -> ExecutivePlanningReport:
    effective_today = today or date.today()
    contexts = build_project_planning_contexts(
        projects=projects,
        entities=entities,
        neighbours=neighbours,
    )
    plans = []

    for index, context in enumerate(contexts):
        project = context.project
        phases = (
            "Frame the executive goal and confirm scope.",
            "Assign accountable owners and resolve dependencies.",
            "Deliver milestones and track risk burn-down.",
        )
        target_dates = _target_dates(effective_today, index)
        milestones = (
            f"Draft scope approved by {target_dates[0]}",
            f"Owner and dependency review complete by {target_dates[1]}",
            f"Executive progress checkpoint held by {target_dates[2]}",
        )
        suggested_owners = context.person_titles or _fallback_owners(people)
        dependencies = context.objective_titles + context.decision_titles + context.dependency_titles
        risks = context.risk_titles or _fallback_risks(project, project_health)
        success_measures = (
            f"Objective linkage confirmed for {project.title}" if context.objective_titles else f"Objective linkage created for {project.title}",
            "Named owner accepts delivery accountability.",
            "Risk and dependency review stays within executive tolerance.",
        )

        plans.append(
            ExecutivePlan(
                project_title=project.title,
                goal=_goal_for_project(project, context.objective_titles),
                phases=phases,
                milestones=milestones,
                suggested_owners=suggested_owners,
                target_dates=target_dates,
                dependencies=dependencies or ("No explicit dependency captured yet.",),
                risks=risks,
                success_measures=success_measures,
            )
        )

    summary = (
        f"Projects discovered: {len(projects)}.",
        f"Draft executive plans proposed: {len(plans)}.",
        "Only approved plans become active.",
    )
    return ExecutivePlanningReport(summary=summary, plans=tuple(plans))


def build_project_planning_contexts(
    *,
    projects: tuple[Any, ...],
    entities: tuple[Any, ...],
    neighbours: dict[str, tuple[str, ...]],
) -> tuple[ProjectPlanningContext, ...]:
    entity_lookup = {entity.id: entity for entity in entities}
    contexts: list[ProjectPlanningContext] = []
    for project in sorted(projects, key=lambda item: getattr(item, "title", "").lower()):
        linked_ids = neighbours.get(project.path, ())
        linked_entities = tuple(entity_lookup[entity_id] for entity_id in linked_ids if entity_id in entity_lookup)
        contexts.append(
            ProjectPlanningContext(
                project=project,
                objective_titles=tuple(sorted(entity.title for entity in linked_entities if getattr(entity, "type", "") == "objective")),
                person_titles=tuple(sorted(entity.title for entity in linked_entities if getattr(entity, "type", "") == "person")),
                decision_titles=tuple(sorted(entity.title for entity in linked_entities if getattr(entity, "type", "") == "decision")),
                risk_titles=tuple(sorted(entity.title for entity in linked_entities if getattr(entity, "type", "") == "risk")),
                dependency_titles=tuple(
                    sorted(
                        entity.title
                        for entity in linked_entities
                        if getattr(entity, "type", "") in {"project", "company", "policy"}
                    )
                ),
            )
        )
    return tuple(contexts)


def render_executive_plans(report: ExecutivePlanningReport) -> str:
    parts = ["# Executive Plans", "", "## Summary", ""]
    parts.extend(f"- {item}" for item in report.summary)
    for plan in report.plans:
        parts.extend(
            [
                "",
                f"## {plan.project_title}",
                "",
                f"- Status: {plan.status}",
                f"- Goal: {plan.goal}",
                f"- Phases: {'; '.join(plan.phases)}",
                f"- Milestones: {'; '.join(plan.milestones)}",
                f"- Suggested owners: {', '.join(plan.suggested_owners)}",
                f"- Target dates: {', '.join(plan.target_dates)}",
                f"- Dependencies: {', '.join(plan.dependencies)}",
                f"- Risks: {', '.join(plan.risks)}",
                f"- Success measures: {'; '.join(plan.success_measures)}",
                f"- User actions: Edit={plan.can_edit}, Approve={plan.can_approve}, Reject={plan.can_reject}",
            ]
        )
    parts.append("")
    return "\n".join(parts)


def _goal_for_project(project: Any, objective_titles: tuple[str, ...]) -> str:
    if objective_titles:
        return f"Deliver {project.title} in support of {objective_titles[0]}."
    recommendation = getattr(project, "recommendation", "")
    if recommendation:
        return f"Stabilise and deliver {project.title}: {recommendation}"
    return f"Deliver {project.title} with clear ownership, milestones, and executive control."


def _target_dates(today: date, offset: int) -> tuple[str, ...]:
    base = today + timedelta(days=offset * 2)
    return (
        (base + timedelta(days=7)).isoformat(),
        (base + timedelta(days=21)).isoformat(),
        (base + timedelta(days=42)).isoformat(),
    )


def _fallback_owners(people: tuple[Any, ...]) -> tuple[str, ...]:
    owners = sorted(getattr(person, "title", "") for person in people[:2] if getattr(person, "title", ""))
    return tuple(owners) or ("Owner to be confirmed",)


def _fallback_risks(project: Any, project_health: dict[str, Any]) -> tuple[str, ...]:
    project_status = getattr(project, "status", "UNKNOWN")
    risks = [f"Project status is {project_status}."]
    if project_health.get("at_risk", 0) > 0:
        risks.append("Portfolio already contains at-risk delivery items.")
    recommendation = getattr(project, "recommendation", "")
    if recommendation:
        risks.append(recommendation)
    return tuple(dict.fromkeys(risks))
