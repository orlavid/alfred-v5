"""Ask Alfred CLI response builder."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.executive.executive_intelligence import build_executive_intelligence_from_state
from src.executive.presentation_contract import build_executive_presentation_from_state
from src.executive.executive_reasoning import build_executive_reasoning_from_state
from src.executive.read_model import build_unified_executive_read_model
from src.executive.executive_state import ExecutiveState, build_executive_state


@dataclass(frozen=True)
class AskAlfredResponse:
    question: str
    executive_answer: list[str]
    supporting_evidence: list[str]
    confidence: str
    recommended_next_actions: list[str]


def ask_alfred(
    question: str,
    evidence_root: Path,
    *,
    meeting_subject: str | None = None,
) -> AskAlfredResponse:
    state = build_executive_state(evidence_root, meeting_subject=meeting_subject)
    return ask_alfred_from_state(question, state)


def ask_alfred_from_state(
    question: str,
    state: ExecutiveState,
) -> AskAlfredResponse:
    cleaned_question = question.strip()
    if not cleaned_question:
        raise ValueError("Question is required.")

    read_model = build_unified_executive_read_model(state)
    reasoning = build_executive_reasoning_from_state(state)
    intelligence = build_executive_intelligence_from_state(state)
    presentation = build_executive_presentation_from_state(state, reasoning=reasoning, read_model=read_model)
    meeting = read_model.meetings[0] if read_model.meetings else None
    followups = read_model.followups
    open_loops = read_model.open_loops

    focus = _detect_focus(cleaned_question)
    answer = _build_answer(cleaned_question, focus, reasoning, intelligence, meeting, followups, open_loops, presentation)
    evidence = _build_supporting_evidence(focus, reasoning, intelligence, meeting, followups, open_loops, presentation)
    actions = _build_next_actions(focus, reasoning, intelligence, meeting, presentation)

    return AskAlfredResponse(
        question=cleaned_question,
        executive_answer=answer,
        supporting_evidence=evidence,
        confidence=reasoning.confidence,
        recommended_next_actions=actions,
    )


def render_ask_alfred(response: AskAlfredResponse) -> str:
    parts = [
        "Executive Answer",
        "",
    ]
    parts.extend(_render_bullets(response.executive_answer))
    parts.extend(["", "Supporting Evidence", ""])
    parts.extend(_render_bullets(response.supporting_evidence))
    parts.extend(["", "Confidence", "", f"- {response.confidence}", "", "Recommended Next Actions", ""])
    parts.extend(_render_bullets(response.recommended_next_actions))
    parts.append("")
    return "\n".join(parts)


def _render_bullets(values: list[str]) -> list[str]:
    items = [f"- {value}" for value in values if value]
    return items or ["_None found._"]


def _detect_focus(question: str) -> str:
    lowered = question.lower()
    if any(token in lowered for token in ("meeting", "discuss", "prepare me")):
        return "meeting"
    if any(token in lowered for token in ("follow-up", "follow up", "overdue", "due today")):
        return "followups"
    if any(token in lowered for token in ("decision", "approve", "approval")):
        return "decisions"
    if any(token in lowered for token in ("open loop", "blocked", "waiting")):
        return "open_loops"
    if any(token in lowered for token in ("supplier", "vendor", "third party")):
        return "suppliers"
    if any(token in lowered for token in ("project", "priority", "today", "do today")):
        return "today"
    return "general"


def _build_answer(question, focus, reasoning, intelligence, meeting, followups, open_loops, presentation) -> list[str]:
    if focus == "meeting":
        if meeting is None:
            return ["No active meeting identified."]
        return [
            f"Use the {meeting.subject} meeting to resolve ownership, objective linkage, and the next dated action.",
            meeting.recommended_discussion[0] if meeting.recommended_discussion else "Prepare the meeting around the highest-friction issue.",
            meeting.risks[0] if meeting.risks else "Confirm the main risk before the meeting starts.",
        ]
    if focus == "followups":
        if not reasoning.top_actions:
            return ["No active follow-up identified."]
        return [
            f"There are {len(followups.overdue)} overdue follow-ups and {len(followups.high_priority)} high-priority items requiring attention.",
            reasoning.top_actions[0].action,
            reasoning.top_actions[1].action if len(reasoning.top_actions) > 1 else (intelligence.recommended_actions_today[0] if intelligence.recommended_actions_today else "No active follow-up identified."),
        ]
    if focus == "open_loops":
        if not reasoning.top_actions:
            return ["No active open loop identified."]
        return [
            f"There are {len(open_loops.critical_open_loops)} critical open loops and {len(open_loops.missing_owners)} owner gaps.",
            reasoning.top_actions[0].action,
            open_loops.recommended_actions[0] if open_loops.recommended_actions else "No active open loop identified.",
        ]
    if focus == "decisions":
        return [
            f"There are {len(reasoning.decisions_required)} decisions awaiting attention in the current intelligence stack.",
            reasoning.decisions_required[0] if reasoning.decisions_required else "Review the highest-importance decision item first.",
            "Clear the highest-importance unresolved decision before adding new work.",
        ]
    if focus == "suppliers":
        supplier_intent = next((item for item in reasoning.intents if item.intent_type == "supplier"), None)
        if not intelligence.supplier_risks and supplier_intent is None:
            return ["No active supplier risk identified."]
        lead_supplier = intelligence.supplier_risks[0] if intelligence.supplier_risks else None
        return [
            f"Supplier governance remains elevated across {len(intelligence.supplier_risks)} critical or important suppliers.",
            supplier_intent.recommended_action if supplier_intent is not None else f"{lead_supplier.title}: {lead_supplier.detail}",
            (
                f"{lead_supplier.title}: {lead_supplier.detail}"
                if lead_supplier is not None
                else "Prioritise the most connected supplier relationships for immediate governance review."
            ),
        ]
    if not reasoning.top_actions:
        return ["No evidence found."]
    return [
        f"Today’s executive focus should start with the top-ranked actions from the reasoning engine.",
        presentation.sections["recommended_actions"].items[0].title if presentation.sections["recommended_actions"].items else reasoning.top_actions[0].action,
        presentation.sections["recommended_actions"].items[1].title if len(presentation.sections["recommended_actions"].items) > 1 else (intelligence.recommended_actions_today[0] if intelligence.recommended_actions_today else "No evidence found."),
    ]


def _build_supporting_evidence(focus, reasoning, intelligence, meeting, followups, open_loops, presentation) -> list[str]:
    evidence = [
        f"Overall health: {reasoning.overall_health}.",
        f"Key theme: {reasoning.key_themes[0]}" if reasoning.key_themes else "",
    ]

    if focus == "meeting":
        if meeting:
            evidence.extend(meeting.executive_summary[:2])
    elif focus == "followups":
        evidence.append(f"Overdue follow-ups: {len(followups.overdue)}; high priority follow-ups: {len(followups.high_priority)}.")
        if intelligence.followups_requiring_action:
            evidence.append(intelligence.followups_requiring_action[0].detail)
    elif focus == "open_loops":
        evidence.append(f"Critical open loops: {len(open_loops.critical_open_loops)}; missing owners: {len(open_loops.missing_owners)}.")
        if intelligence.open_loops:
            evidence.append(intelligence.open_loops[0].detail)
    elif focus == "decisions":
        evidence.extend(reasoning.decisions_required[:2])
    elif focus == "suppliers":
        evidence.extend(item.detail for item in intelligence.supplier_risks[:2])
    else:
        if presentation.sections["recommended_actions"].items:
            evidence.extend(
                ", ".join(item.evidence_paths[:3]) if item.evidence_paths else item.summary
                for item in presentation.sections["recommended_actions"].items[:2]
            )
        else:
            evidence.extend(action.supporting_evidence for action in reasoning.top_actions[:2])
        if not reasoning.top_actions:
            evidence.extend(item.detail for item in intelligence.top_priorities[:2])

    return [item for item in evidence if item][:5]


def _build_next_actions(focus, reasoning, intelligence, meeting, presentation) -> list[str]:
    if focus == "meeting":
        actions = (list(meeting.recommended_discussion[:3]) if meeting else []) + list(intelligence.recommended_actions_today[:2])
    else:
        actions = (
            [item.title for item in presentation.sections["recommended_actions"].items[:3]]
            if presentation.sections["recommended_actions"].items
            else [item.action for item in reasoning.top_actions[:3]]
        ) + list(intelligence.recommended_actions_today[:3])

    deduped = []
    seen = set()
    for action in actions:
        if action in seen:
            continue
        seen.add(action)
        deduped.append(action)
    return deduped[:5] or ["No evidence found."]
