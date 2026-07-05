"""Daily executive briefing for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from src.executive.executive_reasoning import build_executive_reasoning_from_state
from src.executive.executive_state import build_executive_state

SECTION_HEADINGS = [
    "Executive Health",
    "Overnight Changes",
    "Top Three Priorities",
    "Meetings Requiring Preparation",
    "Follow-ups Due Today",
    "Open Loops Blocking Progress",
    "Risks Escalating",
    "Decisions Awaiting You",
    "Recommended Agenda",
    "One-page Executive Summary",
]


@dataclass(frozen=True)
class DailyBrief:
    executive_health: list[str]
    overnight_changes: list[str]
    top_three_priorities: list[str]
    meetings_requiring_preparation: list[str]
    followups_due_today: list[str]
    open_loops_blocking_progress: list[str]
    risks_escalating: list[str]
    decisions_awaiting_you: list[str]
    recommended_agenda: list[str]
    one_page_executive_summary: list[str]
    confidence: str


def build_daily_brief(
    evidence_root: Path,
    *,
    meeting_subject: str | None = None,
) -> DailyBrief:
    state = build_executive_state(evidence_root, meeting_subject=meeting_subject)
    return build_daily_brief_from_state(state)


def build_daily_brief_from_state(
    state,
    *,
    reasoning=None,
) -> DailyBrief:
    reasoning = reasoning or build_executive_reasoning_from_state(state)
    meeting = state.meetings[0] if state.meetings else None
    followups = state.followups
    open_loops = state.open_loops

    executive_health = [
        f"Overall health: {reasoning.overall_health}.",
        f"Confidence: {reasoning.confidence}.",
    ]

    overnight_changes = [
        reasoning.key_themes[0] if reasoning.key_themes else "No material change summary available.",
        reasoning.key_themes[2] if len(reasoning.key_themes) > 2 else "Follow-up load unchanged.",
        reasoning.key_themes[3] if len(reasoning.key_themes) > 3 else "Open loop posture unchanged.",
    ]

    top_three_priorities = [action.action for action in reasoning.top_actions[:3]] or ["No evidence found."]

    meetings_requiring_preparation = _dedupe(
        ([meeting.recommended_discussion[0]] + meeting.risks[:2]) if meeting and meeting.recommended_discussion else (meeting.risks[:3] if meeting else [])
    )[:3] or ["No active meeting identified."]

    followups_due_today = _dedupe(
        [item.summary for item in followups.due_today]
        + [item.summary for item in followups.overdue[:3]]
    )[:3] or ["No active follow-up identified."]

    open_loops_blocking_progress = _dedupe(
        [item.summary for item in open_loops.waiting_for[:3]]
        + [item.summary for item in open_loops.missing_owners[:2]]
    )[:3] or ["No active open loop identified."]

    risks_escalating = reasoning.risks_requiring_immediate_attention[:3]

    decisions_awaiting_you = reasoning.decisions_required[:3]

    recommended_agenda = reasoning.recommended_agenda_for_today[:5]

    one_page_executive_summary = [
        reasoning.executive_conclusion[0] if reasoning.executive_conclusion else "No evidence found.",
        f"Top priority today: {top_three_priorities[0]}" if top_three_priorities else "No evidence found.",
        f"Meeting focus: {meeting.subject}." if meeting else "No active meeting identified.",
        f"Follow-up pressure: {len(followups.overdue)} overdue, {len(followups.high_priority)} high priority.",
        f"Open loop pressure: {len(open_loops.critical_open_loops)} critical, {len(open_loops.missing_owners)} missing owners.",
    ]

    return DailyBrief(
        executive_health=executive_health,
        overnight_changes=overnight_changes,
        top_three_priorities=top_three_priorities,
        meetings_requiring_preparation=meetings_requiring_preparation,
        followups_due_today=followups_due_today,
        open_loops_blocking_progress=open_loops_blocking_progress,
        risks_escalating=risks_escalating,
        decisions_awaiting_you=decisions_awaiting_you,
        recommended_agenda=recommended_agenda,
        one_page_executive_summary=one_page_executive_summary,
        confidence=reasoning.confidence,
    )


def render_daily_brief(brief: DailyBrief) -> str:
    parts = [
        "# Good Morning Phillip",
        "",
        "## Executive Health",
        "",
    ]
    parts.extend(_render_bullets(brief.executive_health))
    parts.extend(["", "## Overnight Changes", ""])
    parts.extend(_render_bullets(brief.overnight_changes))
    parts.extend(["", "## Top Three Priorities", ""])
    parts.extend(_render_bullets(brief.top_three_priorities))
    parts.extend(["", "## Meetings Requiring Preparation", ""])
    parts.extend(_render_bullets(brief.meetings_requiring_preparation))
    parts.extend(["", "## Follow-ups Due Today", ""])
    parts.extend(_render_bullets(brief.followups_due_today))
    parts.extend(["", "## Open Loops Blocking Progress", ""])
    parts.extend(_render_bullets(brief.open_loops_blocking_progress))
    parts.extend(["", "## Risks Escalating", ""])
    parts.extend(_render_bullets(brief.risks_escalating))
    parts.extend(["", "## Decisions Awaiting You", ""])
    parts.extend(_render_bullets(brief.decisions_awaiting_you))
    parts.extend(["", "## Recommended Agenda", ""])
    parts.extend(_render_bullets(brief.recommended_agenda))
    parts.extend(["", "## One-page Executive Summary", ""])
    parts.extend(_render_bullets(brief.one_page_executive_summary))
    parts.extend(["", f"Confidence: {brief.confidence}", ""])
    return "\n".join(parts)


def _render_bullets(values: Iterable[str]) -> list[str]:
    items = [f"- {value}" for value in values if value]
    return items or ["_None found._"]


def _dedupe(values: Iterable[str]) -> list[str]:
    deduped: list[str] = []
    seen = set()
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped
