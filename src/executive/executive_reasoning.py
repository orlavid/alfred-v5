"""Executive reasoning engine for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from executive.report import render as render_executive_review
from src.executive.executive_intelligence import ExecutiveIntelligence, build_executive_intelligence_from_state
from src.executive.intent_contract import CanonicalExecutiveIntent, build_executive_intents, intent_to_executive_action
from src.executive.read_model import build_unified_executive_read_model
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
    intents: tuple[CanonicalExecutiveIntent, ...] = ()


def build_executive_reasoning(
    evidence_root: Path,
    *,
    meeting_subject: str | None = None,
) -> ExecutiveReasoning:
    state = build_executive_state(evidence_root, meeting_subject=meeting_subject)
    return build_executive_reasoning_from_state(state)


def build_executive_reasoning_from_state(state: ExecutiveState) -> ExecutiveReasoning:
    read_model = build_unified_executive_read_model(state)
    engine_result = state.engine_result
    executive_review = render_executive_review(engine_result)
    intelligence = build_executive_intelligence_from_state(state)
    meeting = read_model.meetings[0] if read_model.meetings else None
    followups = read_model.followups
    open_loops = read_model.open_loops

    themes = _build_key_themes(intelligence, followups, open_loops)
    intents = build_executive_intents(read_model, intelligence)
    actions = _build_actions(intents)
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
        intents=intents,
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
    intents_or_intelligence,
    meeting=None,
    followups=None,
    open_loops=None,
) -> list[ExecutiveAction]:
    if isinstance(intents_or_intelligence, tuple):
        intents = intents_or_intelligence
    else:
        from src.executive.intent_contract import build_executive_intents
        from src.executive.read_model import build_unified_executive_read_model
        from src.executive.executive_state import ExecutiveState

        compatibility_state = ExecutiveState(
            meetings=(meeting,) if meeting is not None else (),
            followups=followups,
            open_loops=open_loops,
        )
        read_model = build_unified_executive_read_model(compatibility_state)
        intents = build_executive_intents(read_model, intents_or_intelligence)
    return [intent_to_executive_action(intent) for intent in intents[:10]]


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
