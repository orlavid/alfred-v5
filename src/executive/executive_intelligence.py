"""Unified executive intelligence report for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from executive.engine import execute
from src.followups.followup_intelligence import FollowupItem, build_followup_intelligence
from src.meeting.meeting_intelligence import MeetingBrief, build_meeting_brief
from src.openloops.open_loop_intelligence import OpenLoopItem, build_open_loop_intelligence

DEFAULT_MEETING_SUBJECT = "Barclays"

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
    meeting_subject: str = DEFAULT_MEETING_SUBJECT,
) -> ExecutiveIntelligence:
    result = execute(evidence_root)
    vault = result["knowledge"]["vault"]

    meeting = build_meeting_brief(meeting_subject)
    followups = build_followup_intelligence()
    open_loops = build_open_loop_intelligence()

    health = _build_health_lines(result, vault, meeting_subject)
    top_priorities = _build_top_priorities(vault)
    objectives = _build_objectives(vault)
    meetings = _build_meetings(meeting)
    projects = _build_projects(vault)
    followup_items = _build_followups(followups)
    open_loop_items = _build_open_loops(open_loops)
    people = _build_people(vault)
    supplier_risks = _build_supplier_risks(vault)
    decisions = _build_decisions(vault, open_loops)
    actions = _build_actions(vault, meeting, followups, open_loops)
    summary = _build_summary(
        result=result,
        meeting=meeting,
        followups=followups,
        open_loops=open_loops,
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


def _build_health_lines(result: dict, vault: dict, meeting_subject: str) -> list[str]:
    health = result["health"]
    projects = vault["projects"]
    objectives = vault["objectives"]
    return [
        f"Platform health is {health['status']} with score {health['score']} / 100 and {health['failed']} failed services.",
        f"Knowledge graph covers {vault['graph']['entity_count']} entities and {vault['graph']['edge_count']} edges.",
        f"Projects at risk: {projects.get('at_risk', 0)}; objectives at risk: {objectives.get('at_risk', 0)}.",
        f"Meeting intelligence is currently anchored on {meeting_subject}.",
    ]


def _build_top_priorities(vault: dict) -> list[ExecutiveLineItem]:
    items = []
    for priority in vault["priorities"].get("top_priorities", [])[:10]:
        detail = f"{priority['priority']} score {priority['priority_score']}. {priority['recommended_actions'][0]}"
        items.append(ExecutiveLineItem(priority["title"], detail))
    return items


def _build_objectives(vault: dict) -> list[ExecutiveLineItem]:
    items = []
    for objective in vault["objectives"].get("insights", []):
        if objective.status not in {"AT RISK", "WATCH"}:
            continue
        items.append(ExecutiveLineItem(objective.title, f"{objective.status}. {objective.recommendation}"))
    return items[:10]


def _build_meetings(meeting: MeetingBrief) -> list[ExecutiveLineItem]:
    items = [
        ExecutiveLineItem(
            meeting.subject,
            meeting.recommended_discussion[0] if meeting.recommended_discussion else "Review current meeting priorities.",
        )
    ]
    for risk in meeting.risks[:4]:
        items.append(ExecutiveLineItem(meeting.subject, risk))
    return items[:10]


def _build_projects(vault: dict) -> list[ExecutiveLineItem]:
    items = []
    for project in vault["projects"].get("insights", []):
        if project.status not in {"AT RISK", "WATCH"}:
            continue
        items.append(ExecutiveLineItem(project.title, f"{project.status}. {project.recommendation}"))
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
        items.append(ExecutiveLineItem(item.title, f"{item.summary} Due: {due}; Priority: {item.priority}."))
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
        items.append(ExecutiveLineItem(item.title, f"{item.summary} Status: {item.status}; Owner: {item.owner}."))
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


def _build_people(vault: dict) -> list[ExecutiveLineItem]:
    items = []
    for person in vault["people"].get("insights", [])[:10]:
        items.append(ExecutiveLineItem(person.title, f"{person.risk} influence {person.influence}; companies {person.companies}; projects {person.projects}."))
    return items


def _build_supplier_risks(vault: dict) -> list[ExecutiveLineItem]:
    items = []
    for company in vault["companies"].get("insights", []):
        if company.status not in {"CRITICAL", "IMPORTANT"}:
            continue
        if not company.path.startswith("04 Companies/"):
            continue
        items.append(ExecutiveLineItem(company.title, f"{company.status}; links {company.links}; projects {company.projects}; people {company.people}."))
    return items[:10]


def _build_decisions(vault: dict, open_loops) -> list[ExecutiveLineItem]:
    items = []
    for item in open_loops.missing_decisions[:5]:
        items.append(ExecutiveLineItem(item.title, f"{item.summary} Owner: {item.owner}."))
    for decision in vault["decisions"].get("top_decisions", [])[:5]:
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


def _build_actions(vault: dict, meeting: MeetingBrief, followups, open_loops) -> list[str]:
    actions = []
    for item in vault["do_next"].get("top_10", [])[:3]:
        actions.append(item["action"])
    actions.extend(meeting.recommended_discussion[:2])
    actions.extend(followups.recommendations[:2])
    actions.extend(open_loops.recommended_actions[:2])

    deduped = []
    seen = set()
    for action in actions:
        if action in seen:
            continue
        seen.add(action)
        deduped.append(action)
    return deduped[:10]


def _build_summary(
    *,
    result: dict,
    meeting: MeetingBrief,
    followups,
    open_loops,
    top_priorities: list[ExecutiveLineItem],
    projects: list[ExecutiveLineItem],
    supplier_risks: list[ExecutiveLineItem],
    decisions: list[ExecutiveLineItem],
) -> list[str]:
    health = result["health"]
    return [
        f"Overall posture is {health['status']} with {health['failed']} failed services and score {health['score']} / 100.",
        f"Top executive pressure points: {len(top_priorities)} priorities, {len(projects)} projects at risk, and {len(open_loops.critical_open_loops)} critical open loops.",
        f"Follow-up load remains active with {len(followups.overdue)} overdue items and {len(followups.high_priority)} high-priority follow-ups.",
        f"Current meeting focus is {meeting.subject}, with {len(meeting.risks)} meeting risks and {len(supplier_risks)} supplier risks in the wider briefing.",
        f"Decisions awaiting attention total {len(decisions)} across explicit decision items and open-loop governance gaps.",
    ]
