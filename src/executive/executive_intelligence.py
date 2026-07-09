"""Unified executive intelligence report for Alfred."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from src.executive.read_model import UnifiedExecutiveReadModel, build_unified_executive_read_model
from src.executive.executive_state import ExecutiveState, build_executive_state
from src.followups.followup_intelligence import FollowupItem
from src.openloops.open_loop_intelligence import OpenLoopItem

SECTION_HEADINGS = [
    "Executive Health",
    "Top Priorities",
    "Objectives Requiring Attention",
    "Critical Meetings",
    "Projects At Risk",
    "Follow-ups Requiring Action",
    "Open Loops",
    "Key People",
    "Supplier Risks",
    "Decisions Awaiting Attention",
    "Recommended Actions Today",
    "Executive Summary",
]


@dataclass(frozen=True)
class ExecutiveLineItem:
    title: str
    detail: str
    context: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutiveIntelligence:
    executive_health: list[str]
    top_priorities: list[ExecutiveLineItem]
    objectives_requiring_attention: list[ExecutiveLineItem]
    critical_meetings: list[ExecutiveLineItem]
    projects_at_risk: list[ExecutiveLineItem]
    followups_requiring_action: list[ExecutiveLineItem]
    open_loops: list[ExecutiveLineItem]
    key_people: list[ExecutiveLineItem]
    supplier_risks: list[ExecutiveLineItem]
    decisions_awaiting_attention: list[ExecutiveLineItem]
    recommended_actions_today: list[str]
    executive_summary: list[str]


def build_executive_intelligence(
    evidence_root: Path,
    *,
    meeting_subject: str | None = None,
) -> ExecutiveIntelligence:
    state = build_executive_state(evidence_root, meeting_subject=meeting_subject)
    return build_executive_intelligence_from_state(state)


def build_executive_intelligence_from_state(state: ExecutiveState) -> ExecutiveIntelligence:
    read_model = build_unified_executive_read_model(state)
    meeting = read_model.meetings[0] if read_model.meetings else None
    followups = read_model.followups
    open_loops = read_model.open_loops

    health = _build_health_lines(state, meeting.subject if meeting else None)
    top_priorities = _build_top_priorities(read_model)
    objectives = _build_objectives(read_model)
    meetings = _build_meetings(read_model)
    projects = _build_projects(read_model)
    followup_items = _build_followups(followups)
    open_loop_items = _build_open_loops(open_loops)
    people = _build_people(read_model)
    supplier_risks = _build_supplier_risks(read_model)
    decisions = _build_decisions(read_model)
    actions = _build_actions(read_model)
    summary = _build_summary(
        state=state,
        top_priorities=top_priorities,
        projects=projects,
        supplier_risks=supplier_risks,
        decisions=decisions,
    )

    return ExecutiveIntelligence(
        executive_health=health,
        top_priorities=top_priorities,
        objectives_requiring_attention=objectives,
        critical_meetings=meetings,
        projects_at_risk=projects,
        followups_requiring_action=followup_items,
        open_loops=open_loop_items,
        key_people=people,
        supplier_risks=supplier_risks,
        decisions_awaiting_attention=decisions,
        recommended_actions_today=actions,
        executive_summary=summary,
    )


def render_executive_intelligence(report: ExecutiveIntelligence) -> str:
    parts = [
        "# Executive Intelligence",
        "",
        "## Executive Health",
        "",
    ]
    parts.extend(_render_bullets(report.executive_health))
    parts.extend(["", "## Top Priorities", ""])
    parts.extend(_render_items(report.top_priorities))
    parts.extend(["", "## Objectives Requiring Attention", ""])
    parts.extend(_render_items(report.objectives_requiring_attention))
    parts.extend(["", "## Critical Meetings", ""])
    parts.extend(_render_items(report.critical_meetings))
    parts.extend(["", "## Projects At Risk", ""])
    parts.extend(_render_items(report.projects_at_risk))
    parts.extend(["", "## Follow-ups Requiring Action", ""])
    parts.extend(_render_items(report.followups_requiring_action))
    parts.extend(["", "## Open Loops", ""])
    parts.extend(_render_items(report.open_loops))
    parts.extend(["", "## Key People", ""])
    parts.extend(_render_items(report.key_people))
    parts.extend(["", "## Supplier Risks", ""])
    parts.extend(_render_items(report.supplier_risks))
    parts.extend(["", "## Decisions Awaiting Attention", ""])
    parts.extend(_render_items(report.decisions_awaiting_attention))
    parts.extend(["", "## Recommended Actions Today", ""])
    parts.extend(_render_bullets(report.recommended_actions_today))
    parts.extend(["", "## Executive Summary", ""])
    parts.extend(_render_bullets(report.executive_summary))
    parts.append("")
    return "\n".join(parts)


def _render_bullets(values: Iterable[str]) -> list[str]:
    items = [f"- {value}" for value in values if value]
    return items or ["_None found._"]


def _render_items(values: Iterable[ExecutiveLineItem]) -> list[str]:
    items = [f"- {value.title}: {value.detail}" for value in values]
    return items or ["_None found._"]


def _build_health_lines(state: ExecutiveState, meeting_subject: str | None) -> list[str]:
    health = state.executive_health
    graph_stats = state.relationship_graph.statistics if state.relationship_graph is not None else {}
    return [
        f"Platform health is {health['status']} with score {health['score']} / 100 and {health['failed']} failed services.",
        f"Knowledge graph covers {graph_stats.get('node_count', 0)} entities and {graph_stats.get('edge_count', 0)} edges.",
        f"Projects at risk: {state.project_health.get('at_risk', 0)}; objectives at risk: {state.objective_health.get('at_risk', 0)}.",
        f"Meeting intelligence is currently anchored on {meeting_subject}." if meeting_subject else "No active meeting identified.",
    ]


def _build_top_priorities(read_model: UnifiedExecutiveReadModel) -> list[ExecutiveLineItem]:
    items = []
    for priority in read_model.priorities[:10]:
        detail_parts = [
            f"{priority['priority']} score {priority['priority_score']}. {priority['next_step']}",
            f"Status: {priority.get('status', 'ACTIVE')}",
        ]
        if priority.get("owner"):
            detail_parts.append(f"Owner: {priority['owner']}")
        if priority.get("deadline_or_recency"):
            detail_parts.append(f"Timing: {priority['deadline_or_recency']}")
        if priority.get("evidence_paths"):
            detail_parts.append(f"Evidence: {', '.join(priority['evidence_paths'][:2])}")
        items.append(
            ExecutiveLineItem(
                priority["title"],
                "; ".join(detail_parts),
                context=dict(priority),
            )
        )
    return items


def _build_objectives(read_model: UnifiedExecutiveReadModel) -> list[ExecutiveLineItem]:
    items = []
    for objective in read_model.objectives:
        if objective.status not in {"AT RISK", "WATCH"}:
            continue
        items.append(
            ExecutiveLineItem(
                objective.title,
                f"{objective.status}. {objective.recommendation}",
                context={
                    "entity_type": "objective",
                    "status": objective.status,
                    "next_step": objective.recommendation,
                    "evidence_paths": [objective.path],
                },
            )
        )
    return items[:10]


def _build_meetings(read_model: UnifiedExecutiveReadModel) -> list[ExecutiveLineItem]:
    meeting_items = [item for item in read_model.work_items if item.work_item_type == "meeting"]
    if not meeting_items:
        return []
    meeting = read_model.meetings[0]
    work_item = meeting_items[0]
    items = [
        ExecutiveLineItem(
            meeting.subject,
            meeting.recommended_discussion[0] if meeting.recommended_discussion else "No evidence found.",
            context={
                "entity_type": "meeting",
                "evidence_paths": list(work_item.evidence_paths[:3]),
                "why_now": list(meeting.risks[:2]) or list(meeting.recommended_discussion[:2]),
                "next_step": meeting.recommended_discussion[0] if meeting.recommended_discussion else "Prepare the meeting around the highest-friction issue.",
            },
        )
    ]
    for risk in meeting.risks[:4]:
        items.append(ExecutiveLineItem(meeting.subject, risk))
    return items[:10]


def _build_projects(read_model: UnifiedExecutiveReadModel) -> list[ExecutiveLineItem]:
    items = []
    for project in read_model.projects:
        if project.status not in {"AT RISK", "WATCH"}:
            continue
        items.append(
            ExecutiveLineItem(
                project.title,
                f"{project.status}. {project.recommendation}",
                context={
                    "entity_type": "project",
                    "status": project.status,
                    "next_step": project.recommendation,
                    "evidence_paths": [project.path],
                },
            )
        )
    return items[:10]


def _build_followups(followups) -> list[ExecutiveLineItem]:
    items = []
    for item in _merge_followup_lists(
        followups.overdue,
        followups.due_today,
        followups.due_this_week,
        followups.high_priority,
    ):
        due = item.due_date or "no explicit due date"
        items.append(
            ExecutiveLineItem(
                item.title,
                f"{item.summary} Due: {due}; Priority: {item.priority}.",
                context={
                    "entity_type": "follow_up",
                    "status": item.priority,
                    "deadline_or_recency": due if item.due_date else None,
                    "next_step": item.summary,
                    "evidence_paths": [item.path],
                },
            )
        )
    return items[:10]


def _merge_followup_lists(*groups: list[FollowupItem]) -> list[FollowupItem]:
    merged: list[FollowupItem] = []
    seen = set()
    for group in groups:
        for item in group:
            key = (item.path, item.summary)
            if key in seen:
                continue
            seen.add(key)
            merged.append(item)
    return merged


def _build_open_loops(open_loops) -> list[ExecutiveLineItem]:
    items = []
    for item in _merge_open_loop_lists(
        open_loops.critical_open_loops,
        open_loops.waiting_for,
        open_loops.missing_owners,
    ):
        items.append(
            ExecutiveLineItem(
                item.title,
                f"{item.summary} Status: {item.status}; Owner: {item.owner}.",
                context={
                    "entity_type": "open_loop",
                    "status": item.status,
                    "owner": item.owner,
                    "next_step": item.summary,
                    "evidence_paths": [item.path],
                },
            )
        )
    return items[:10]


def _merge_open_loop_lists(*groups: list[OpenLoopItem]) -> list[OpenLoopItem]:
    merged: list[OpenLoopItem] = []
    seen = set()
    for group in groups:
        for item in group:
            key = (item.path, item.summary)
            if key in seen:
                continue
            seen.add(key)
            merged.append(item)
    return merged


def _build_people(read_model: UnifiedExecutiveReadModel) -> list[ExecutiveLineItem]:
    items = []
    for person in read_model.people[:10]:
        items.append(ExecutiveLineItem(person.title, f"{person.risk} influence {person.influence}; companies {person.companies}; projects {person.projects}."))
    return items


def _build_supplier_risks(read_model: UnifiedExecutiveReadModel) -> list[ExecutiveLineItem]:
    items = []
    for company in read_model.suppliers:
        items.append(
            ExecutiveLineItem(
                company.title,
                f"{company.status}; links {company.links}; projects {company.projects}; people {company.people}.",
                context={
                    "entity_type": "company",
                    "status": company.status,
                    "next_step": "Validate ownership, dependency and supplier governance",
                    "evidence_paths": [company.path],
                },
            )
        )
    return items[:10]


def _build_decisions(read_model: UnifiedExecutiveReadModel) -> list[ExecutiveLineItem]:
    items = []
    for item in read_model.open_loops.missing_decisions[:5]:
        items.append(
            ExecutiveLineItem(
                item.title,
                f"{item.summary} Owner: {item.owner}.",
                context={
                    "entity_type": "decision",
                    "owner": item.owner,
                    "next_step": item.summary,
                },
            )
        )
    for decision in read_model.decisions[:5]:
        items.append(
            ExecutiveLineItem(
                decision["title"],
                f"Importance {decision['importance']}; projects {decision['projects']}; objectives {decision['objectives']}.",
            )
        )
    deduped = []
    seen = set()
    for item in items:
        key = item.title, item.detail
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped[:10]


def _build_actions(read_model: UnifiedExecutiveReadModel) -> list[str]:
    return list(read_model.actions[:10])


def _build_summary(
    *,
    state: ExecutiveState,
    top_priorities: list[ExecutiveLineItem],
    projects: list[ExecutiveLineItem],
    supplier_risks: list[ExecutiveLineItem],
    decisions: list[ExecutiveLineItem],
) -> list[str]:
    health = state.executive_health
    followups = state.followups
    open_loops = state.open_loops
    return [
        f"Overall posture is {health['status']} with {health['failed']} failed services and score {health['score']} / 100.",
        f"Top executive pressure points: {len(top_priorities)} priorities, {len(projects)} projects at risk, and {len(open_loops.critical_open_loops)} critical open loops.",
        f"Follow-up load remains active with {len(followups.overdue)} overdue items and {len(followups.high_priority)} high-priority follow-ups.",
        (
            f"Current meeting focus is {state.meetings[0].subject}, with {len(state.meetings[0].risks)} meeting risks and {len(supplier_risks)} supplier risks in the wider briefing."
            if state.meetings
            else "No active meeting identified."
        ),
        f"Decisions awaiting attention total {len(decisions)} across explicit decision items and open-loop governance gaps.",
    ]
