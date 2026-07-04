"""Pure Python dashboard API for Alfred."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.daily.daily_brief import DailyBrief, build_daily_brief_from_state
from src.executive.executive_reasoning import ExecutiveReasoning, build_executive_reasoning_from_state
from src.executive.executive_state import DEFAULT_MEETING_SUBJECT, ExecutiveState, build_executive_state

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_ROOT = ROOT / "evidence" / "alfred-inventory"


def get_dashboard_home(
    evidence_root: Path | None = None,
    *,
    meeting_subject: str = DEFAULT_MEETING_SUBJECT,
) -> dict[str, Any]:
    state = build_executive_state(evidence_root or DEFAULT_EVIDENCE_ROOT, meeting_subject=meeting_subject)
    reasoning = build_executive_reasoning_from_state(state)
    brief = build_daily_brief_from_state(state, reasoning=reasoning)

    burning_fires = get_burning_fires(state, reasoning=reasoning)
    plan_today = get_plan_today(state, reasoning=reasoning, brief=brief)
    next_best_action = get_next_best_action(state, reasoning=reasoning)
    operating_picture = get_operating_picture(state, reasoning=reasoning, brief=brief)
    navigation_priorities = get_navigation_priorities(state, reasoning=reasoning, brief=brief)

    return {
        "burning_fires": burning_fires,
        "plan_today": plan_today,
        "next_best_action": next_best_action,
        "operating_picture": operating_picture,
        "navigation_priorities": navigation_priorities,
        "interruption_policy": _build_interruption_policy(state, burning_fires, next_best_action),
        "generated_from": {
            "meeting_subject": meeting_subject,
            "runtime_model": "ExecutiveState",
            "sources": [
                "ExecutiveState",
                "Executive Reasoning",
                "Daily Brief",
                "Follow-up Intelligence",
                "Open Loop Intelligence",
                "Meeting Intelligence",
            ],
            "confidence": state.confidence,
        },
    }


def get_burning_fires(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
) -> list[dict[str, str]]:
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    items: list[dict[str, str]] = []

    for value in effective_reasoning.risks_requiring_immediate_attention[:3]:
        items.append({"type": "risk", "summary": value})

    for item in state.open_loops.critical_open_loops[:2]:
        items.append({"type": "open_loop", "summary": item.summary})

    return _dedupe_dicts(items, key_fields=("type", "summary"))[:5]


def get_plan_today(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
    brief: DailyBrief | None = None,
) -> list[str]:
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    effective_brief = brief or build_daily_brief_from_state(state, reasoning=effective_reasoning)
    return _dedupe_strings(
        effective_brief.top_three_priorities
        + effective_brief.recommended_agenda[:2]
    )[:5]


def get_next_best_action(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
) -> dict[str, str]:
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    if effective_reasoning.top_actions:
        action = effective_reasoning.top_actions[0]
        return {
            "priority": action.priority,
            "action": action.action,
            "why_it_matters": action.why_it_matters,
            "confidence": action.confidence,
        }
    return {
        "priority": "MEDIUM",
        "action": "Review the current executive recommendations and assign an owner.",
        "why_it_matters": "No ranked action was produced from the current reasoning set.",
        "confidence": state.confidence,
    }


def get_operating_picture(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
    brief: DailyBrief | None = None,
) -> dict[str, Any]:
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    effective_brief = brief or build_daily_brief_from_state(state, reasoning=effective_reasoning)
    meeting = state.meetings[0]
    return {
        "overall_health": effective_reasoning.overall_health,
        "confidence": effective_reasoning.confidence,
        "meeting_focus": meeting.subject,
        "followup_pressure": {
            "overdue": len(state.followups.overdue),
            "due_today": len(state.followups.due_today),
            "high_priority": len(state.followups.high_priority),
        },
        "open_loop_pressure": {
            "critical": len(state.open_loops.critical_open_loops),
            "waiting_for": len(state.open_loops.waiting_for),
            "missing_owners": len(state.open_loops.missing_owners),
        },
        "summary": effective_brief.one_page_executive_summary[:3],
    }


def get_navigation_priorities(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
    brief: DailyBrief | None = None,
) -> list[dict[str, str]]:
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    effective_brief = brief or build_daily_brief_from_state(state, reasoning=effective_reasoning)
    meeting = state.meetings[0]

    items = [
        {
            "label": "Priorities",
            "reason": effective_brief.top_three_priorities[0] if effective_brief.top_three_priorities else "Review the top-ranked executive action.",
        },
        {
            "label": "Meetings",
            "reason": meeting.recommended_discussion[0] if meeting.recommended_discussion else f"Prepare for {meeting.subject}.",
        },
        {
            "label": "Follow-ups",
            "reason": effective_brief.followups_due_today[0] if effective_brief.followups_due_today else "Work the highest-pressure follow-up next.",
        },
        {
            "label": "Open Loops",
            "reason": effective_brief.open_loops_blocking_progress[0] if effective_brief.open_loops_blocking_progress else "Assign owners to critical loops.",
        },
        {
            "label": "Decisions",
            "reason": effective_brief.decisions_awaiting_you[0] if effective_brief.decisions_awaiting_you else "Clear the next unresolved decision.",
        },
    ]
    return items


def _build_interruption_policy(
    state: ExecutiveState,
    burning_fires: list[dict[str, str]],
    next_best_action: dict[str, str],
) -> dict[str, Any]:
    level = "allow"
    rule = f"Default to the next best action: {next_best_action['action']}"
    if len(burning_fires) >= 5 or len(state.followups.overdue) >= 10 or len(state.open_loops.critical_open_loops) >= 10:
        level = "block"
        rule = "Do not accept new discretionary work until one burning fire has an owner and a dated next step."
    elif burning_fires:
        level = "filter"
        rule = "Only interrupt for decision, risk, or owner-blocking issues tied to current priorities."
    return {
        "level": level,
        "rule": rule,
    }


def _dedupe_strings(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen = set()
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def _dedupe_dicts(values: list[dict[str, str]], *, key_fields: tuple[str, ...]) -> list[dict[str, str]]:
    deduped: list[dict[str, str]] = []
    seen = set()
    for value in values:
        key = tuple(value[field] for field in key_fields)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(value)
    return deduped
