"""Board review intelligence for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.board.board_registry import BoardGovernance, BoardMember, build_board_governance

if TYPE_CHECKING:
    from src.executive.executive_state import ExecutiveState

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_ROOT = ROOT / "evidence" / "alfred-inventory"


@dataclass(frozen=True)
class BoardAssignment:
    board_member: str
    item_title: str
    item_type: str
    rationale: str


@dataclass(frozen=True)
class BoardReview:
    review_type: str
    findings: tuple[str, ...]
    recommendations: tuple[str, ...]
    risks: tuple[str, ...]
    decisions: tuple[str, ...]
    proposed_actions: tuple[str, ...]
    proposed_executive_updates: tuple[str, ...]
    approval_required: bool = True


@dataclass(frozen=True)
class BoardIntelligence:
    objective_assignments: tuple[BoardAssignment, ...]
    project_assignments: tuple[BoardAssignment, ...]
    ad_hoc_review: BoardReview
    monthly_review: BoardReview
    summary: tuple[str, ...]


def build_board_intelligence(evidence_root: Path) -> BoardIntelligence:
    from src.executive.executive_state import build_executive_state

    state = build_executive_state(evidence_root)
    return build_board_intelligence_from_state(state)


def build_board_intelligence_from_state(state: ExecutiveState) -> BoardIntelligence:
    board = state.board or build_board_governance()
    objective_assignments = _assign_objectives(board, state.objectives)
    project_assignments = _assign_projects(board, state.projects)
    ad_hoc_review = _build_review("Ad Hoc Board Review", state, objective_assignments, project_assignments, limit=3)
    monthly_review = _build_review("Monthly Board Meeting", state, objective_assignments, project_assignments, limit=5)
    summary = (
        f"Objectives assigned to board members: {len(objective_assignments)}.",
        f"Projects assigned to board members: {len(project_assignments)}.",
        "Board intelligence produces proposed executive updates only.",
        "User approval is required before any ExecutiveState changes.",
    )
    return BoardIntelligence(
        objective_assignments=objective_assignments,
        project_assignments=project_assignments,
        ad_hoc_review=ad_hoc_review,
        monthly_review=monthly_review,
        summary=summary,
    )


def render_board_intelligence(report: BoardIntelligence) -> str:
    parts = ["# Board Intelligence", "", "## Summary", ""]
    parts.extend(f"- {item}" for item in report.summary)
    parts.extend(["", "## Objective Assignments", ""])
    parts.extend(_render_assignments(report.objective_assignments))
    parts.extend(["", "## Project Assignments", ""])
    parts.extend(_render_assignments(report.project_assignments))
    parts.extend(["", "## Ad Hoc Board Review", ""])
    parts.extend(_render_review(report.ad_hoc_review))
    parts.extend(["", "## Monthly Board Meeting", ""])
    parts.extend(_render_review(report.monthly_review))
    parts.append("")
    return "\n".join(parts)


def _assign_objectives(board: BoardGovernance, objectives: tuple[Any, ...]) -> tuple[BoardAssignment, ...]:
    strategy_member = _member(board, "Athena")
    risk_member = _member(board, "Sentinel")
    assignments = []
    for objective in sorted(objectives, key=lambda item: getattr(item, "title", "").lower()):
        member = risk_member if getattr(objective, "status", "") == "AT RISK" else strategy_member
        assignments.append(
            BoardAssignment(
                board_member=member.name,
                item_title=objective.title,
                item_type="Objective",
                rationale=f"{member.role} owns objective alignment and intervention for status {getattr(objective, 'status', 'UNKNOWN')}.",
            )
        )
    return tuple(assignments)


def _assign_projects(board: BoardGovernance, projects: tuple[Any, ...]) -> tuple[BoardAssignment, ...]:
    operations_member = _member(board, "Titan")
    technology_member = _member(board, "Vector")
    finance_member = _member(board, "Sterling")
    assignments = []
    for project in sorted(projects, key=lambda item: getattr(item, "title", "").lower()):
        lowered = project.title.lower()
        if any(token in lowered for token in ("finance", "capex", "po", "subscription")):
            member = finance_member
        elif any(token in lowered for token in ("data", "system", "agent", "tech", "platform")):
            member = technology_member
        else:
            member = operations_member
        assignments.append(
            BoardAssignment(
                board_member=member.name,
                item_title=project.title,
                item_type="Project",
                rationale=f"{member.role} is the best-fit executive reviewer for this project domain.",
            )
        )
    return tuple(assignments)


def _build_review(
    review_type: str,
    state: ExecutiveState,
    objective_assignments: tuple[BoardAssignment, ...],
    project_assignments: tuple[BoardAssignment, ...],
    *,
    limit: int,
) -> BoardReview:
    findings = tuple(
        list(_top_titles(state.objectives, limit, suffix="objective")) +
        list(_top_titles(state.projects, limit, suffix="project"))
    )[:limit]
    recommendations = tuple(
        [f"Board member {assignment.board_member} should review {assignment.item_title}." for assignment in objective_assignments[:2]]
        + [f"Board member {assignment.board_member} should stabilise {assignment.item_title}." for assignment in project_assignments[:2]]
    )[:limit]
    risks = tuple(item.get("title", "") for item in state.decisions[:limit] if item.get("title")) or tuple(
        getattr(item, "title", "") for item in state.risks[:limit] if getattr(item, "title", "")
    )
    decisions = tuple(
        f"Approve or reject the draft executive plan for {plan.project_title}."
        for plan in state.executive_plans[:limit]
    )
    proposed_actions = tuple(
        list(state.recommendations[:limit]) +
        [f"Schedule board follow-through on {plan.project_title}." for plan in state.executive_plans[:2]]
    )[:limit]
    proposed_updates = tuple(
        f"Proposed Executive Update: assign {assignment.board_member} as review lead for {assignment.item_title}."
        for assignment in (objective_assignments[:2] + project_assignments[:2])
    )[:limit]
    return BoardReview(
        review_type=review_type,
        findings=findings or ("No board findings generated.",),
        recommendations=recommendations or ("No board recommendations generated.",),
        risks=risks or ("No board risks generated.",),
        decisions=decisions or ("No board decisions proposed.",),
        proposed_actions=proposed_actions or ("No proposed actions generated.",),
        proposed_executive_updates=proposed_updates or ("No proposed executive updates generated.",),
    )


def _top_titles(items: tuple[Any, ...], limit: int, *, suffix: str) -> list[str]:
    values = []
    for item in items[:limit]:
        title = getattr(item, "title", "")
        if title:
            values.append(f"Board review required for {suffix} {title}.")
    return values


def _member(board: BoardGovernance, name: str) -> BoardMember:
    for member in board.board_members:
        if member.name == name:
            return member
    return board.board_members[0]


def _render_assignments(assignments: tuple[BoardAssignment, ...]) -> list[str]:
    if not assignments:
        return ["_None found._"]
    return [
        f"- {assignment.item_type}: {assignment.item_title} | Board Member: {assignment.board_member} | Rationale: {assignment.rationale}"
        for assignment in assignments
    ]


def _render_review(review: BoardReview) -> list[str]:
    return [
        f"### {review.review_type}",
        "- Findings: " + "; ".join(review.findings),
        "- Recommendations: " + "; ".join(review.recommendations),
        "- Risks: " + "; ".join(review.risks),
        "- Decisions: " + "; ".join(review.decisions),
        "- Proposed Actions: " + "; ".join(review.proposed_actions),
        "- Proposed Executive Updates: " + "; ".join(review.proposed_executive_updates),
        f"- Approval Required: {'YES' if review.approval_required else 'NO'}",
        "",
    ]
