"""Executive reasoning engine for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable

from executive.report import render as render_executive_review
from src.executive.executive_intelligence import ExecutiveIntelligence, build_executive_intelligence_from_state
from src.executive.executive_state import ExecutiveState, build_executive_state

SECTION_HEADINGS = [
    "Executive Assessment",
    "Top 10 Executive Actions",
    "Risks Requiring Immediate Attention",
    "Opportunities",
    "Decisions Required",
    "Recommended Agenda For Today",
    "Executive Conclusion",
]
PRIORITY_DETAIL_RE = re.compile(r"^(?P<priority>[A-Z]+) score (?P<score>\d+)\.\s*(?P<action>.+)$")


@dataclass(frozen=True)
class ExecutiveAction:
    priority: str
    action: str
    why_it_matters: str
    supporting_evidence: str
    expected_impact: str
    confidence: str
    score: int


@dataclass(frozen=True)
class ExecutiveReasoning:
    overall_health: str
    confidence: str
    key_themes: list[str]
    top_actions: list[ExecutiveAction]
    risks_requiring_immediate_attention: list[str]
    opportunities: list[str]
    decisions_required: list[str]
    recommended_agenda_for_today: list[str]
    executive_conclusion: list[str]


def build_executive_reasoning(
    evidence_root: Path,
    *,
    meeting_subject: str | None = None,
) -> ExecutiveReasoning:
    state = build_executive_state(evidence_root, meeting_subject=meeting_subject)
    return build_executive_reasoning_from_state(state)


def build_executive_reasoning_from_state(state: ExecutiveState) -> ExecutiveReasoning:
    engine_result = state.engine_result
    executive_review = render_executive_review(engine_result)
    intelligence = build_executive_intelligence_from_state(state)
    meeting = state.meetings[0] if state.meetings else None
    followups = state.followups
    open_loops = state.open_loops

    themes = _build_key_themes(intelligence, followups, open_loops)
    actions = _build_actions(intelligence, meeting, followups, open_loops)
    risks = _build_risks(intelligence, meeting, open_loops)
    opportunities = _build_opportunities(intelligence, meeting)
    decisions = _build_decisions(intelligence)
    agenda = _build_agenda(actions, decisions, risks)
    conclusion = _build_conclusion(engine_result, executive_review, actions, risks, opportunities)
    confidence = _build_confidence(engine_result, actions, risks)

    return ExecutiveReasoning(
        overall_health=f"{engine_result['health']['status']} ({engine_result['health']['score']} / 100)",
        confidence=confidence,
        key_themes=themes,
        top_actions=actions,
        risks_requiring_immediate_attention=risks,
        opportunities=opportunities,
        decisions_required=decisions,
        recommended_agenda_for_today=agenda,
        executive_conclusion=conclusion,
    )


def render_executive_reasoning(report: ExecutiveReasoning) -> str:
    parts = [
        "# Executive Reasoning",
        "",
        "## Executive Assessment",
        "",
        "### Overall Health",
        "",
        f"- {report.overall_health}",
        "",
        "### Confidence",
        "",
        f"- {report.confidence}",
        "",
        "### Key Themes",
        "",
    ]
    parts.extend(_render_bullets(report.key_themes))
    parts.extend(["", "## Top 10 Executive Actions", ""])
    parts.extend(_render_actions(report.top_actions))
    parts.extend(["", "## Risks Requiring Immediate Attention", ""])
    parts.extend(_render_bullets(report.risks_requiring_immediate_attention))
    parts.extend(["", "## Opportunities", ""])
    parts.extend(_render_bullets(report.opportunities))
    parts.extend(["", "## Decisions Required", ""])
    parts.extend(_render_bullets(report.decisions_required))
    parts.extend(["", "## Recommended Agenda For Today", ""])
    parts.extend(_render_bullets(report.recommended_agenda_for_today))
    parts.extend(["", "## Executive Conclusion", ""])
    parts.extend(_render_bullets(report.executive_conclusion))
    parts.append("")
    return "\n".join(parts)


def _render_bullets(values: Iterable[str]) -> list[str]:
    items = [f"- {value}" for value in values if value]
    return items or ["_None found._"]


def _render_actions(actions: Iterable[ExecutiveAction]) -> list[str]:
    lines: list[str] = []
    for item in actions:
        lines.extend(
            [
                f"### {item.action}",
                f"- Priority: {item.priority}",
                f"- Action: {item.action}",
                f"- Why it matters: {item.why_it_matters}",
                f"- Supporting evidence: {item.supporting_evidence}",
                f"- Expected impact: {item.expected_impact}",
                f"- Confidence: {item.confidence}",
                "",
            ]
        )
    return lines or [
        "### No evidence found",
        "- Priority: NONE",
        "- Action: No active action identified.",
        "- Why it matters: No evidence found.",
        "- Supporting evidence: No evidence found.",
        "- Expected impact: No evidence found.",
        "- Confidence: LOW",
        "",
    ]


def _build_key_themes(
    intelligence: ExecutiveIntelligence,
    followups,
    open_loops,
) -> list[str]:
    return [
        f"{len(intelligence.top_priorities)} top priorities need active triage.",
        f"{len(intelligence.projects_at_risk)} projects are already flagged at risk or on watch.",
        f"{len(followups.overdue)} overdue follow-ups remain unresolved.",
        f"{len(open_loops.critical_open_loops)} critical open loops are still open.",
        f"{len(intelligence.supplier_risks)} supplier relationships show elevated governance pressure.",
    ]


def _build_actions(
    intelligence: ExecutiveIntelligence,
    meeting,
    followups,
    open_loops,
) -> list[ExecutiveAction]:
    candidates = [
        _action_from_priority(intelligence.top_priorities[0], intelligence) if intelligence.top_priorities and _priority_actionable(intelligence.top_priorities[0]) else None,
        _action_from_project(intelligence.projects_at_risk[0]) if intelligence.projects_at_risk else None,
        _action_from_followup(intelligence.followups_requiring_action[0]) if intelligence.followups_requiring_action else None,
        _action_from_open_loop(intelligence.open_loops[0]) if intelligence.open_loops else None,
        _action_from_meeting(meeting) if meeting and meeting.recommended_discussion else None,
        _action_from_decision(intelligence.decisions_awaiting_attention[0]) if intelligence.decisions_awaiting_attention else None,
        _action_from_supplier(intelligence.supplier_risks[0]) if intelligence.supplier_risks else None,
        _action_from_priority(intelligence.top_priorities[1], intelligence) if len(intelligence.top_priorities) > 1 and _priority_actionable(intelligence.top_priorities[1]) else None,
        _action_from_followup(intelligence.followups_requiring_action[1]) if len(intelligence.followups_requiring_action) > 1 else None,
        _action_from_open_loop(intelligence.open_loops[1]) if len(intelligence.open_loops) > 1 else None,
        _action_from_recommendation(intelligence.recommended_actions_today[0], "HIGH") if intelligence.recommended_actions_today else None,
        _action_from_recommendation(open_loops.recommended_actions[0], "HIGH") if open_loops.recommended_actions else None,
        _action_from_recommendation(followups.recommendations[0], "HIGH") if followups.recommendations else None,
    ]

    deduped: list[ExecutiveAction] = []
    seen = set()
    for action in candidates:
        if action is None:
            continue
        key = action.action
        if key in seen:
            continue
        seen.add(key)
        deduped.append(action)

    deduped.sort(key=lambda item: (-item.score, item.action))
    return deduped[:10]


def _action_from_priority(item, intelligence: ExecutiveIntelligence) -> ExecutiveAction:
    action = _priority_recommended_action(item)
    priority = _priority_level(item)
    score = _priority_score(item)
    return ExecutiveAction(
        priority=priority,
        action=f"{action} for {item.title}",
        why_it_matters=item.detail,
        supporting_evidence=f"Priority list elevates {item.title} with score {score}.",
        expected_impact="Reduces governance drift and improves delivery accountability.",
        confidence="HIGH" if priority in {"CRITICAL", "HIGH"} else "MEDIUM",
        score=score,
    )


def _action_from_project(item) -> ExecutiveAction:
    return ExecutiveAction(
        priority="HIGH",
        action=f"Review recovery path for project {item.title}",
        why_it_matters=item.detail,
        supporting_evidence=f"Project risk intelligence: {item.detail}",
        expected_impact="Stops further slippage in project execution and clarifies next steps.",
        confidence="HIGH",
        score=92,
    )


def _action_from_followup(item) -> ExecutiveAction:
    return ExecutiveAction(
        priority="HIGH",
        action=f"Close follow-up from {item.title}",
        why_it_matters=item.detail,
        supporting_evidence=f"Follow-up intelligence flags this as requiring action: {item.detail}",
        expected_impact="Reduces overdue operational debt and improves execution cadence.",
        confidence="MEDIUM",
        score=88,
    )


def _action_from_open_loop(item) -> ExecutiveAction:
    return ExecutiveAction(
        priority="HIGH",
        action=f"Convert open loop into owned action: {item.title}",
        why_it_matters=item.detail,
        supporting_evidence=f"Open loop intelligence identifies a critical or ownerless loop: {item.detail}",
        expected_impact="Moves unresolved governance risk into accountable delivery.",
        confidence="HIGH",
        score=90,
    )


def _action_from_meeting(meeting) -> ExecutiveAction:
    return ExecutiveAction(
        priority="HIGH",
        action=f"Prepare {meeting.subject} discussion around ownership and risk",
        why_it_matters=meeting.recommended_discussion[0],
        supporting_evidence="Meeting intelligence highlights unresolved owner, objective, and supplier linkage gaps.",
        expected_impact="Improves meeting quality and turns relationship time into concrete decisions.",
        confidence="MEDIUM",
        score=84,
    )


def _action_from_decision(item) -> ExecutiveAction:
    return ExecutiveAction(
        priority="MEDIUM",
        action=f"Resolve decision attention item: {item.title}",
        why_it_matters=item.detail,
        supporting_evidence=f"Decision intelligence flags this as awaiting attention: {item.detail}",
        expected_impact="Prevents unresolved decisions from slowing dependent work.",
        confidence="MEDIUM",
        score=78,
    )


def _action_from_supplier(item) -> ExecutiveAction:
    return ExecutiveAction(
        priority="MEDIUM",
        action=f"Review supplier risk posture for {item.title}",
        why_it_matters=item.detail,
        supporting_evidence=f"Supplier risk list ranks {item.title} as elevated: {item.detail}",
        expected_impact="Improves third-party governance and narrows compliance exposure.",
        confidence="MEDIUM",
        score=76,
    )


def _action_from_recommendation(text: str, priority: str) -> ExecutiveAction:
    score = 82 if priority == "HIGH" else 70
    return ExecutiveAction(
        priority=priority,
        action=text,
        why_it_matters=text,
        supporting_evidence="Derived from existing intelligence recommendations.",
        expected_impact="Focuses executive attention on already-evidenced next actions.",
        confidence="MEDIUM",
        score=score,
    )


def _priority_actionable(item) -> bool:
    return _priority_score(item) >= 40 and _priority_level(item) in {"CRITICAL", "HIGH", "MEDIUM"}


def _priority_match(item) -> re.Match[str] | None:
    detail = getattr(item, "detail", "")
    return PRIORITY_DETAIL_RE.match(detail)


def _priority_score(item) -> int:
    match = _priority_match(item)
    return int(match.group("score")) if match else 0


def _priority_level(item) -> str:
    match = _priority_match(item)
    return match.group("priority") if match else "LOW"


def _priority_recommended_action(item) -> str:
    match = _priority_match(item)
    return match.group("action") if match else "Review and confirm executive treatment"


def _build_risks(intelligence: ExecutiveIntelligence, meeting, open_loops) -> list[str]:
    risks = []
    risks.extend(item.detail for item in intelligence.projects_at_risk[:3])
    if meeting:
        risks.extend(meeting.risks[:3])
    risks.extend(item.summary for item in open_loops.critical_open_loops[:3])
    return _dedupe_strings(risks)[:10]


def _build_opportunities(intelligence: ExecutiveIntelligence, meeting) -> list[str]:
    opportunities = [
        "Use top-priority triage to assign owners across currently unowned critical work.",
        "Tighten supplier governance around the most connected third parties first.",
    ]
    if meeting:
        opportunities.insert(0, f"Use {meeting.subject} meeting to resolve ownership and convert relationship context into actions.")
    if intelligence.key_people:
        opportunities.append(f"Leverage {intelligence.key_people[0].title} as a high-influence relationship node.")
    return opportunities[:10]


def _build_decisions(intelligence: ExecutiveIntelligence) -> list[str]:
    return [f"{item.title}: {item.detail}" for item in intelligence.decisions_awaiting_attention[:10]]


def _build_agenda(actions: list[ExecutiveAction], decisions: list[str], risks: list[str]) -> list[str]:
    agenda = []
    agenda.extend(action.action for action in actions[:5])
    agenda.extend(decisions[:2])
    agenda.extend(risks[:2])
    return _dedupe_strings(agenda)[:10]


def _build_conclusion(
    engine_result: dict,
    executive_review: str,
    actions: list[ExecutiveAction],
    risks: list[str],
    opportunities: list[str],
) -> list[str]:
    health = engine_result["health"]
    return [
        f"Executive posture remains {health['status']} and requires active intervention rather than passive monitoring.",
        f"The reasoning engine prioritised {len(actions)} actions from review, meeting, follow-up, open-loop, and executive intelligence evidence.",
        f"Immediate pressure is concentrated in execution risk, governance debt, and unresolved supplier-linked issues.",
        f"Main opportunity: {opportunities[0] if opportunities else 'Use today’s agenda to close the highest-friction item.'}",
        f"Executive review remains available as the base evidence pack ({len(executive_review.splitlines())} rendered lines).",
    ]


def _build_confidence(engine_result: dict, actions: list[ExecutiveAction], risks: list[str]) -> str:
    if engine_result["health"]["status"] == "AMBER" and len(actions) >= 8 and len(risks) >= 5:
        return "HIGH"
    if len(actions) >= 5:
        return "MEDIUM"
    return "LOW"


def _dedupe_strings(values: Iterable[str]) -> list[str]:
    deduped: list[str] = []
    seen = set()
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped
