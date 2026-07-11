"""Pure Python dashboard API for Alfred."""

from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path
from typing import Any

from src.alfred.ask import ask_alfred_from_state
from src.board.board_registry import BoardMember
from src.daily.daily_brief import DailyBrief, build_daily_brief_from_state
from executive.knowledge.entity_contract import CanonicalExecutiveEntityContract
from src.executive.presentation_contract import build_executive_presentation_from_state
from src.executive.read_model import build_unified_executive_read_model
from src.executive.executive_reasoning import ExecutiveReasoning, build_executive_reasoning_from_state
from src.executive.executive_state import ExecutiveState, build_executive_state
from src.objectives.objective_intelligence import (
    ObjectiveView,
    build_objective_intelligence_from_state,
    build_objective_views_from_state,
)
from src.operations.doctor import build_operational_readiness
from src.operations.environment_discovery import build_doctor_summary, build_environment_inventory

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_ROOT = ROOT / "evidence" / "alfred-inventory"
ASK_ALFRED_QUESTIONS = (
    "What should I do today?",
    "What follow-ups are overdue?",
    "What is blocked right now?",
    "What meetings require preparation?",
)


def get_dashboard_home(
    evidence_root: Path | None = None,
    *,
    meeting_subject: str | None = None,
    vault_root: Path | None = None,
) -> dict[str, Any]:
    state = build_executive_state(
        evidence_root or DEFAULT_EVIDENCE_ROOT,
        meeting_subject=meeting_subject,
        vault_root=vault_root,
    )
    read_model = build_unified_executive_read_model(state)
    reasoning = build_executive_reasoning_from_state(state)
    brief = build_daily_brief_from_state(state, reasoning=reasoning)
    presentation = build_executive_presentation_from_state(state, reasoning=reasoning, read_model=read_model)

    burning_fires = get_burning_fires(state, reasoning=reasoning, presentation=presentation)
    plan_today = get_plan_today(state, reasoning=reasoning, brief=brief, presentation=presentation)
    next_best_action = get_next_best_action(state, reasoning=reasoning, presentation=presentation)
    operating_picture = get_operating_picture(state, reasoning=reasoning, brief=brief, presentation=presentation)
    navigation_priorities = get_navigation_priorities(state, reasoning=reasoning, brief=brief, presentation=presentation)

    return {
        "burning_fires": burning_fires,
        "plan_today": plan_today,
        "next_best_action": next_best_action,
        "operating_picture": operating_picture,
        "navigation_priorities": navigation_priorities,
        "interruption_policy": _build_interruption_policy(state, burning_fires, next_best_action),
        "objectives": _build_objectives_page(state),
        "projects": _build_projects_page(state),
        "meetings": _build_meetings_page(read_model, presentation),
        "board": _build_board_page(state),
        "ask_alfred": _build_ask_alfred_page(state),
        "daily_brief": _build_daily_brief_page(brief),
        "knowledge": _build_knowledge_page(state),
        "admin_configuration": _build_admin_configuration_page(),
        "generated_from": {
            "meeting_subject": meeting_subject,
            "runtime_model": "ExecutiveState",
            "production_mode": True,
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
    presentation=None,
) -> list[dict[str, str]]:
    read_model = build_unified_executive_read_model(state)
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    effective_presentation = presentation or build_executive_presentation_from_state(state, reasoning=effective_reasoning, read_model=read_model)
    items: list[dict[str, str]] = []

    for value in effective_presentation.sections["risks"].items[:3]:
        items.append(_evidence_card("risk", value.title, "executive_reasoning", state.confidence, list(value.evidence_paths)))

    for item in read_model.open_loops.critical_open_loops[:2]:
        items.append(_evidence_card("open_loop", item.summary, "open_loop_provider", state.confidence, [item.path], origin=item.source_kind))

    return _dedupe_dicts(items, key_fields=("type", "summary"))[:5]


def get_plan_today(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
    brief: DailyBrief | None = None,
    presentation=None,
) -> list[dict[str, Any]]:
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    effective_brief = brief or build_daily_brief_from_state(state, reasoning=effective_reasoning)
    effective_presentation = presentation or build_executive_presentation_from_state(state, reasoning=effective_reasoning)
    values = _dedupe_strings(
        [item.title for item in effective_presentation.sections["priorities"].items[:3]]
        + [item.title for item in effective_presentation.sections["recommended_actions"].items[:2]]
        + effective_brief.recommended_agenda[:2]
    )[:5]
    return [_evidence_card("plan", value, "daily_brief", state.confidence, []) for value in values if value not in {"No evidence found"}]


def get_next_best_action(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
    presentation=None,
) -> dict[str, str]:
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    effective_presentation = presentation or build_executive_presentation_from_state(state, reasoning=effective_reasoning)
    if effective_presentation.sections["recommended_actions"].items:
        item = effective_presentation.sections["recommended_actions"].items[0]
        return {
            "priority": item.extensions.get("priority", effective_reasoning.top_actions[0].priority if effective_reasoning.top_actions else "NONE"),
            "action": item.title,
            "why_it_matters": item.summary,
            "confidence": item.confidence,
            "origin": item.extensions.get("intent_type", "recommended_action"),
            "source_notes": list(item.evidence_paths),
            "provider": "executive_intent",
        }
    return {
        "priority": "NONE",
        "action": "No evidence found",
        "why_it_matters": "No ranked action was produced from evidence-backed reasoning.",
        "confidence": state.confidence,
        "origin": "no_evidence",
        "source_notes": [],
        "provider": "executive_state",
    }


def get_operating_picture(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
    brief: DailyBrief | None = None,
    presentation=None,
) -> dict[str, Any]:
    read_model = build_unified_executive_read_model(state)
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    effective_brief = brief or build_daily_brief_from_state(state, reasoning=effective_reasoning)
    effective_presentation = presentation or build_executive_presentation_from_state(state, reasoning=effective_reasoning, read_model=read_model)
    meeting = read_model.meetings[0] if read_model.meetings else None
    return {
        "overall_health": effective_reasoning.overall_health,
        "confidence": effective_reasoning.confidence,
        "meeting_focus": meeting.subject if meeting else "No active meeting identified.",
        "followup_pressure": {
            "overdue": len(read_model.followups.overdue),
            "due_today": len(read_model.followups.due_today),
            "high_priority": len(read_model.followups.high_priority),
        },
        "open_loop_pressure": {
            "critical": len(read_model.open_loops.critical_open_loops),
            "waiting_for": len(read_model.open_loops.waiting_for),
            "missing_owners": len(read_model.open_loops.missing_owners),
        },
        "summary": effective_brief.one_page_executive_summary[:2] + [item.title for item in effective_presentation.sections["recommended_actions"].items[:1]],
        "origin": "executive_state",
        "source_notes": [item.path for item in meeting.matched_entities] if meeting else [],
        "provider": "executive_state",
    }


def get_navigation_priorities(
    state: ExecutiveState,
    *,
    reasoning: ExecutiveReasoning | None = None,
    brief: DailyBrief | None = None,
    presentation=None,
) -> list[dict[str, str]]:
    read_model = build_unified_executive_read_model(state)
    effective_reasoning = reasoning or build_executive_reasoning_from_state(state)
    effective_brief = brief or build_daily_brief_from_state(state, reasoning=effective_reasoning)
    effective_presentation = presentation or build_executive_presentation_from_state(state, reasoning=effective_reasoning, read_model=read_model)
    meeting = read_model.meetings[0] if read_model.meetings else None

    items = [
        {
            "label": "Priorities",
            "reason": effective_presentation.sections["priorities"].items[0].title if effective_presentation.sections["priorities"].items else (effective_brief.top_three_priorities[0] if effective_brief.top_three_priorities else "No evidence found"),
            "origin": "daily_brief",
            "confidence": state.confidence,
            "source_notes": [],
            "provider": "daily_brief",
        },
        {
            "label": "Meetings",
            "reason": effective_presentation.sections["meetings"].items[0].summary if effective_presentation.sections["meetings"].items else (meeting.recommended_discussion[0] if meeting and meeting.recommended_discussion else "No active meeting identified."),
            "origin": "meeting_intelligence" if meeting else "no_evidence",
            "confidence": state.confidence,
            "source_notes": [item.path for item in meeting.matched_entities] if meeting else [],
            "provider": "meeting_intelligence" if meeting else "executive_state",
        },
        {
            "label": "Follow-ups",
            "reason": effective_presentation.sections["followups"].items[0].title if effective_presentation.sections["followups"].items else (effective_brief.followups_due_today[0] if effective_brief.followups_due_today else "No active follow-up identified."),
            "origin": "followup_intelligence",
            "confidence": state.confidence,
            "source_notes": [item.path for item in read_model.followups.due_today[:1]],
            "provider": "followup_provider",
        },
        {
            "label": "Open Loops",
            "reason": effective_brief.open_loops_blocking_progress[0] if effective_brief.open_loops_blocking_progress else "No active open loop identified.",
            "origin": "open_loop_intelligence",
            "confidence": state.confidence,
            "source_notes": [item.path for item in read_model.open_loops.waiting_for[:1]],
            "provider": "open_loop_provider",
        },
        {
            "label": "Decisions",
            "reason": effective_brief.decisions_awaiting_you[0] if effective_brief.decisions_awaiting_you else "No active decision identified.",
            "origin": "executive_reasoning",
            "confidence": state.confidence,
            "source_notes": [],
            "provider": "executive_reasoning",
        },
    ]
    return items


def _build_objectives_page(state: ExecutiveState) -> dict[str, Any]:
    report = build_objective_intelligence_from_state(state)
    objective_views = build_objective_views_from_state(state)
    objective_contracts = {
        entity.canonical_name: entity
        for entity in state.canonical_entities
        if entity.entity_type == "objective"
    }
    strategic_records = {item.title: item for item in report.strategic_objectives}
    details: dict[str, Any] = {}
    items: list[dict[str, Any]] = []

    for view in objective_views:
        contract = objective_contracts.get(view.objective.title)
        if contract is None:
            continue
        strategic = strategic_records.get(view.objective.title)
        objective_id = _stable_objective_id(contract.entity_id)
        detail = _build_objective_detail(
            state,
            contract=contract,
            view=view,
            strategic=strategic,
            objective_id=objective_id,
        )
        details[objective_id] = detail
        items.append(
            {
                "objective_id": objective_id,
                "title": detail["title"],
                "source_path": detail["source_path"],
                "source_entity_id": detail["source_entity_id"],
                "route": detail["route"],
                "lifecycle": detail["current_status"],
                "confidence": detail["evidence_confidence"],
                "supporting_projects": [item["title"] for item in detail["supporting_projects"]],
                "linked_decisions": [item["title"] for item in detail["linked_decisions"]],
                "stale_evidence": detail["stale_evidence"],
                "recommended_next_action": detail["recommended_next_action"],
                "health": detail["health"],
                "progress_indicator": detail["progress_assessment"],
                "owner": detail["owner"],
                "last_meaningful_activity": detail["last_meaningful_activity"],
                "next_checkpoint_or_deadline": detail["next_checkpoint_or_deadline"],
                "supporting_project_count": len(detail["supporting_projects"]),
                "linked_decision_count": len(detail["linked_decisions"]),
                "open_action_count": len(detail["open_actions"]),
                "key_risk_or_blocker": detail["key_risk_or_blocker"],
                "missing_fields": detail["missing_information"],
            }
        )
    return {
        "health": state.objective_health,
        "items": items,
        "details": details,
        "summary": report.executive_summary,
    }


def _build_objective_detail(
    state: ExecutiveState,
    *,
    contract: CanonicalExecutiveEntityContract,
    view: ObjectiveView,
    strategic,
    objective_id: str,
) -> dict[str, Any]:
    all_entities = {entity.id: entity for entity in state.entities}
    related_work_items = _related_work_items(state, contract)
    supporting_projects = _related_project_items(view)
    linked_decisions = _related_decision_items(view, state)
    relevant_meetings = _related_meeting_items(state, contract)
    related_people = _related_people_items(contract, state)
    blockers = _objective_blockers(contract, related_work_items)
    key_risk_or_blocker = blockers[0]["title"] if blockers else "No evidence found"
    evidence_sources = _objective_evidence_sources(contract, all_entities)
    smart_assessment = _build_smart_assessment(contract, view, supporting_projects, linked_decisions, blockers)
    recent_changes = _build_objective_recent_changes(contract, view, related_work_items)
    progress_assessment = _build_progress_assessment(contract, view, supporting_projects, linked_decisions, related_work_items)
    open_actions = _build_open_action_items(related_work_items)
    followups = [item for item in open_actions if item["type"] == "follow_up"]
    decision_refs = [item["title"] for item in linked_decisions]
    meeting_refs = [item["title"] for item in relevant_meetings]
    next_checkpoint = contract.due_date or _future_review_date(contract.review_date) or "Not defined"
    recommended_next_action = strategic.recommended_next_action if strategic is not None else view.objective.recommendation
    executive_definition = _objective_definition(contract, all_entities)
    last_review_date, next_review_date = _review_window(contract.review_date)
    missing_information = _objective_missing_information(
        contract,
        smart_assessment=smart_assessment,
        executive_definition=executive_definition,
    )

    return {
        "objective_id": objective_id,
        "route": f"/objectives/{objective_id}",
        "title": contract.canonical_name,
        "source_entity_id": contract.entity_id,
        "source_path": contract.primary_path,
        "executive_definition": executive_definition,
        "owner": contract.owner or "Not defined",
        "delegates": list(contract.delegates),
        "current_status": contract.status or view.objective.status or "Not defined",
        "health": _status_to_rag(contract.status or view.objective.status),
        "rag_rating": _status_to_rag(contract.status or view.objective.status),
        "progress_assessment": progress_assessment,
        "evidence_confidence": contract.confidence,
        "start_date": contract.created or "Not defined",
        "target_date": contract.due_date or "Not defined",
        "last_review_date": last_review_date,
        "next_review_date": next_review_date,
        "last_meaningful_activity": contract.last_activity or (view.latest_evidence_date.isoformat() if view.latest_evidence_date else "No evidence found"),
        "next_checkpoint_or_deadline": next_checkpoint,
        "supporting_projects": supporting_projects,
        "linked_decisions": linked_decisions,
        "risks_and_blockers": blockers,
        "open_actions": open_actions,
        "follow_ups": followups,
        "relevant_meetings": relevant_meetings,
        "related_people": related_people,
        "evidence_sources": evidence_sources,
        "recent_changes": recent_changes,
        "recommended_next_action": recommended_next_action,
        "key_risk_or_blocker": key_risk_or_blocker,
        "missing_information": missing_information,
        "smart_assessment": smart_assessment,
        "proposed_smart_refinement": _build_smart_refinement(contract, smart_assessment),
        "stale_evidence": view.stale_evidence,
        "linked_decision_titles": decision_refs,
        "relevant_meeting_titles": meeting_refs,
        "source_work_item_ids": [item["work_item_id"] for item in open_actions],
        "provenance": {
            "objective": list(contract.evidence_paths),
            "supporting_projects": [item["path"] for item in supporting_projects],
            "linked_decisions": [item["path"] for item in linked_decisions],
            "risks_and_blockers": [item["path"] for item in blockers if item["path"]],
            "open_actions": [item["path"] for item in open_actions],
        },
    }


def _related_project_items(view: ObjectiveView) -> list[dict[str, str]]:
    return [
        {
            "title": entity.title,
            "path": entity.path,
            "reason": "Linked to the objective in the executive knowledge graph.",
            "route": "/projects",
        }
        for entity in view.project_entities
    ]


def _related_decision_items(view: ObjectiveView, state: ExecutiveState) -> list[dict[str, str]]:
    decision_lookup = {item["title"]: item for item in state.decisions}
    items: list[dict[str, str]] = []
    for entity in view.decision_entities:
        decision = decision_lookup.get(entity.title)
        summary = "Linked decision requiring executive attention."
        if decision is not None:
            summary = (
                f"Importance {decision['importance']}; "
                f"linked to {decision['projects']} projects and {decision['objectives']} objectives."
            )
        items.append(
            {
                "title": entity.title,
                "path": entity.path,
                "reason": summary,
                "route": "/decisions",
            }
        )
    return items


def _related_meeting_items(state: ExecutiveState, contract: CanonicalExecutiveEntityContract) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for meeting in state.meetings:
        if contract.canonical_name not in [item.title for item in meeting.related_objectives]:
            continue
        items.append(
            {
                "title": meeting.subject,
                "path": meeting.matched_entities[0].path if meeting.matched_entities else "",
                "reason": meeting.recommended_discussion[0] if meeting.recommended_discussion else "Relevant meeting context exists.",
                "route": "/meetings",
            }
        )
    return items


def _related_people_items(contract: CanonicalExecutiveEntityContract, state: ExecutiveState) -> list[dict[str, str]]:
    entity_lookup = {entity.title: entity for entity in state.entities}
    items: list[dict[str, str]] = []
    for name in contract.related_people:
        entity = entity_lookup.get(name)
        items.append(
            {
                "title": name,
                "path": entity.path if entity is not None else "",
                "reason": "Connected to the objective through the executive knowledge graph.",
                "route": "/people",
            }
        )
    return items


def _related_work_items(state: ExecutiveState, contract: CanonicalExecutiveEntityContract) -> list[Any]:
    return [
        item
        for item in state.work_items
        if contract.canonical_name in item.related_objectives
        or contract.canonical_name in item.related_entities
    ]


def _build_open_action_items(related_work_items: list[Any]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for item in related_work_items:
        if item.work_item_type not in {"follow_up", "open_loop", "decision_review"}:
            continue
        items.append(
            {
                "work_item_id": item.work_item_id,
                "title": item.title,
                "type": item.work_item_type,
                "status": item.status or "Not defined",
                "priority": item.priority or "Not defined",
                "path": item.evidence_paths[0] if item.evidence_paths else "",
                "reason": _work_item_reason(item),
                "route": "/follow-ups" if item.work_item_type == "follow_up" else "/open-loops",
            }
        )
    return items


def _objective_blockers(contract: CanonicalExecutiveEntityContract, related_work_items: list[Any]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for item in related_work_items:
        if item.work_item_type not in {"open_loop", "decision_review"}:
            continue
        items.append(
            {
                "title": item.title,
                "path": item.evidence_paths[0] if item.evidence_paths else "",
                "reason": _work_item_reason(item),
                "type": item.work_item_type,
                "route": "/open-loops",
            }
        )
    for dependency in contract.dependencies:
        items.append(
            {
                "title": dependency,
                "path": "",
                "reason": "Dependency linked to the objective in canonical executive state.",
                "type": "dependency",
                "route": "/open-loops",
            }
        )
    deduped: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        key = (item["title"], item["type"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped[:10]


def _objective_evidence_sources(
    contract: CanonicalExecutiveEntityContract,
    raw_entities: dict[str, Any],
) -> list[dict[str, str]]:
    labels_by_path: dict[str, str] = {}
    for source_id in contract.extensions.get("source_entity_ids", ()):
        entity = raw_entities.get(source_id)
        if entity is None:
            continue
        labels_by_path[entity.path] = entity.title
    return [
        {
            "label": labels_by_path.get(path, _path_label(path)),
            "path": path,
            "reason": "Canonical objective evidence source.",
        }
        for path in contract.evidence_paths
    ]


def _objective_definition(
    contract: CanonicalExecutiveEntityContract,
    raw_entities: dict[str, Any],
) -> str:
    snippets: list[str] = []
    for source_id in contract.extensions.get("source_entity_ids", ()):
        entity = raw_entities.get(source_id)
        text = getattr(entity, "source_text", "") if entity is not None else ""
        for line in text.splitlines():
            cleaned = line.strip().lstrip("-* ").strip()
            if not cleaned or cleaned.startswith("#"):
                continue
            if contract.canonical_name.lower() in cleaned.lower():
                continue
            if len(cleaned) < 20:
                continue
            snippets.append(cleaned.rstrip(".") + ".")
            break
    return snippets[0] if snippets else "No evidence found."


def _build_progress_assessment(
    contract: CanonicalExecutiveEntityContract,
    view: ObjectiveView,
    supporting_projects: list[dict[str, str]],
    linked_decisions: list[dict[str, str]],
    related_work_items: list[Any],
) -> str:
    signals = []
    if contract.status:
        signals.append(contract.status)
    if supporting_projects:
        signals.append(f"{len(supporting_projects)} supporting project(s)")
    if linked_decisions:
        signals.append(f"{len(linked_decisions)} linked decision(s)")
    if related_work_items:
        signals.append(f"{len(related_work_items)} open work item(s)")
    if view.stale_evidence:
        signals.append("stale evidence")
    return ", ".join(signals) if signals else "No evidence found."


def _build_objective_recent_changes(
    contract: CanonicalExecutiveEntityContract,
    view: ObjectiveView,
    related_work_items: list[Any],
) -> list[str]:
    changes: list[str] = []
    if contract.last_activity:
        changes.append(f"Last meaningful activity recorded on {contract.last_activity}.")
    if view.latest_evidence_date:
        changes.append(f"Latest dated evidence is {view.latest_evidence_date.isoformat()}.")
    if related_work_items:
        changes.append(f"{len(related_work_items)} open work item(s) remain linked to this objective.")
    return changes or ["No evidence found."]


def _build_smart_assessment(
    contract: CanonicalExecutiveEntityContract,
    view: ObjectiveView,
    supporting_projects: list[dict[str, str]],
    linked_decisions: list[dict[str, str]],
    blockers: list[dict[str, str]],
) -> dict[str, dict[str, Any]]:
    return {
        "specific": _smart_dimension(
            condition=bool(contract.canonical_name and (supporting_projects or linked_decisions)),
            evidence=[contract.primary_path, *[item["path"] for item in supporting_projects[:2]]],
            missing="No supporting project or decision evidence clearly defines scope." if not (supporting_projects or linked_decisions) else "",
            improvement="Link the objective to the delivery programme or decision set that defines its scope.",
        ),
        "measurable": _smart_dimension(
            condition=bool(contract.status or contract.due_date or contract.review_date),
            evidence=[path for path in (contract.primary_path, *contract.provenance.get("status", ()), *contract.provenance.get("due_date", ())) if path],
            missing="No explicit status, checkpoint, or deadline evidence." if not (contract.status or contract.due_date or contract.review_date) else "",
            improvement="Add explicit status checkpoints, target measures, or dated review points.",
        ),
        "achievable": _smart_dimension(
            condition=bool(contract.owner or supporting_projects),
            evidence=[path for path in (contract.provenance.get("owner", ()) + tuple(item["path"] for item in supporting_projects[:2])) if path],
            missing="No accountable owner or supporting delivery plan is defined." if not (contract.owner or supporting_projects) else "",
            improvement="Name the accountable owner and attach the objective to active delivery work.",
        ),
        "relevant": _smart_dimension(
            condition=bool(contract.related_projects or contract.related_people or blockers),
            evidence=[path for path in (contract.provenance.get("related_projects", ()) + contract.provenance.get("related_people", ())) if path],
            missing="Objective is weakly connected to current executive work." if not (contract.related_projects or contract.related_people or blockers) else "",
            improvement="Strengthen links to active projects, decision-makers, and blockers.",
        ),
        "time_bound": _smart_dimension(
            condition=bool(contract.due_date or contract.review_date),
            evidence=[path for path in (contract.provenance.get("due_date", ()) + contract.provenance.get("review_date", ())) if path],
            missing="No target or review date is defined." if not (contract.due_date or contract.review_date) else "",
            improvement="Add a next review date or explicit target deadline.",
        ),
    }


def _smart_dimension(
    *,
    condition: bool,
    evidence: list[str],
    missing: str,
    improvement: str,
) -> dict[str, Any]:
    filtered_evidence = [path for path in evidence if path]
    return {
        "current_assessment": "Evidence-backed" if condition else "Weak or not defined",
        "evidence": filtered_evidence or ["No evidence found."],
        "missing_or_weak_definition": missing or "None identified from current evidence.",
        "suggested_improvement": improvement,
    }


def _build_smart_refinement(
    contract: CanonicalExecutiveEntityContract,
    smart_assessment: dict[str, dict[str, Any]],
) -> list[str]:
    refinements = [f"Retain the current objective title: {contract.canonical_name}."]
    for dimension, payload in smart_assessment.items():
        if payload["current_assessment"] == "Evidence-backed":
            continue
        refinements.append(f"{dimension.capitalize()}: {payload['suggested_improvement']}")
    return refinements


def _objective_missing_information(
    contract: CanonicalExecutiveEntityContract,
    *,
    smart_assessment: dict[str, dict[str, Any]],
    executive_definition: str,
) -> list[str]:
    items: list[str] = []
    for field in contract.missing_fields:
        if field == "owner":
            items.append("Accountable owner is not defined.")
        elif field == "due_date":
            items.append("Target date is not defined.")
        elif field == "review_date":
            items.append("Review cadence is not defined.")
        elif field == "status":
            items.append("Current status is not defined.")
        elif field == "related_projects":
            items.append("No supporting projects are linked.")
        elif field == "related_people":
            items.append("No related people are linked.")
    if executive_definition == "No evidence found.":
        items.append("Executive definition is not explicit in the current evidence.")
    for dimension, payload in smart_assessment.items():
        if payload["current_assessment"] != "Evidence-backed":
            items.append(f"{dimension.capitalize()} is weakly defined.")
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped or ["No material missing information identified."]


def _stable_objective_id(entity_id: str) -> str:
    return hashlib.sha1(entity_id.encode("utf-8")).hexdigest()[:12]


def _status_to_rag(status: str | None) -> str:
    if status == "AT RISK":
        return "RED"
    if status == "WATCH":
        return "AMBER"
    if status == "SUPPORTED":
        return "GREEN"
    return "Not defined"


def _path_label(path: str) -> str:
    value = path.split("#", 1)[0].rsplit("/", 1)[-1]
    return value[:-3] if value.lower().endswith(".md") else value


def _work_item_reason(item: Any) -> str:
    if item.work_item_type == "follow_up":
        return f"Follow-up action; due {item.due_date or 'Not defined'}; priority {item.priority or 'Not defined'}."
    return f"{item.work_item_type.replace('_', ' ').title()}; status {item.status or 'Not defined'}; priority {item.priority or 'Not defined'}."


def _review_window(review_date: str | None) -> tuple[str, str]:
    if not review_date:
        return "Not defined", "Not defined"
    if review_date >= date.today().isoformat():
        return "Not defined", review_date
    return review_date, "Not defined"


def _future_review_date(review_date: str | None) -> str | None:
    if not review_date:
        return None
    return review_date if review_date >= date.today().isoformat() else None


def _build_projects_page(state: ExecutiveState) -> dict[str, Any]:
    entity_lookup = {entity.id: entity for entity in state.entities}
    items = []
    for project in state.projects:
        linked_titles = sorted(
            entity_lookup[entity_id].title
            for entity_id in state.neighbours.get(project.path, ())
            if entity_id in entity_lookup and getattr(entity_lookup[entity_id], "type", None) == "objective"
        )
        items.append(
            {
                "title": project.title,
                "status": project.status,
                "objective_linkage": linked_titles,
                "risk": getattr(project, "risk", "Unknown"),
                "recommendation": project.recommendation,
            }
        )
    return {
        "health": state.project_health,
        "items": items[:12],
        "summary": [
            f"Projects tracked: {len(state.projects)}.",
            f"Projects at risk: {state.project_health.get('at_risk', 0)}.",
        ],
    }


def _build_meetings_page(read_model, presentation=None) -> dict[str, Any]:
    if not read_model.meetings:
        return {
            "subject": "No active meeting identified.",
            "meeting_purpose": [],
            "executive_summary": ["No evidence found."],
            "relationship_history": [],
            "related_people": [],
            "related_projects": [],
            "related_companies": [],
            "related_objectives": [],
            "related_decisions": [],
            "risks": [],
            "commercial_issues": [],
            "recent_changes": [],
            "open_loops": [],
            "follow_ups": [],
            "dependencies": [],
            "recommended_discussion": [],
            "recommended_questions": [],
            "recommended_decisions": [],
            "evidence_references": [],
            "confidence": "LOW",
        }
    if presentation is None:
        meeting_item = None
    else:
        meeting_item = presentation.sections["meetings"].items[0] if presentation.sections["meetings"].items else None
    meeting = read_model.meetings[0]
    return {
        "subject": meeting.subject,
        "meeting_purpose": list(meeting_item.extensions.get("meeting_purpose", meeting.meeting_purpose)) if meeting_item else meeting.meeting_purpose,
        "executive_summary": list(meeting_item.extensions.get("executive_summary", meeting.executive_summary)) if meeting_item else meeting.executive_summary,
        "relationship_history": list(meeting_item.extensions.get("relationship_history", meeting.relationship_history)) if meeting_item else meeting.relationship_history,
        "related_people": list(meeting_item.extensions.get("related_people", [item.title for item in meeting.related_people])) if meeting_item else [item.title for item in meeting.related_people],
        "related_projects": list(meeting_item.extensions.get("related_projects", [item.title for item in meeting.related_projects])) if meeting_item else [item.title for item in meeting.related_projects],
        "related_companies": list(meeting_item.extensions.get("related_companies", [item.title for item in meeting.related_companies])) if meeting_item else [item.title for item in meeting.related_companies],
        "related_objectives": list(meeting_item.extensions.get("related_objectives", [item.title for item in meeting.related_objectives])) if meeting_item else [item.title for item in meeting.related_objectives],
        "related_decisions": list(meeting_item.extensions.get("related_decisions", [item.title for item in meeting.related_decisions])) if meeting_item else [item.title for item in meeting.related_decisions],
        "risks": list(meeting_item.extensions.get("risks", meeting.risks)) if meeting_item else meeting.risks,
        "commercial_issues": list(meeting_item.extensions.get("commercial_issues", meeting.commercial_issues)) if meeting_item else meeting.commercial_issues,
        "recent_changes": list(meeting_item.extensions.get("recent_changes", meeting.recent_changes)) if meeting_item else meeting.recent_changes,
        "open_loops": list(meeting_item.extensions.get("open_loops", [item.title for item in meeting.open_loops])) if meeting_item else [item.title for item in meeting.open_loops],
        "follow_ups": list(meeting_item.extensions.get("follow_ups", [item.title for item in meeting.follow_ups])) if meeting_item else [item.title for item in meeting.follow_ups],
        "dependencies": list(meeting_item.extensions.get("dependencies", meeting.dependencies)) if meeting_item else meeting.dependencies,
        "recommended_discussion": list(meeting_item.extensions.get("recommended_discussion", meeting.recommended_discussion)) if meeting_item else meeting.recommended_discussion,
        "recommended_questions": list(meeting_item.extensions.get("recommended_questions", meeting.recommended_questions)) if meeting_item else meeting.recommended_questions,
        "recommended_decisions": list(meeting_item.extensions.get("recommended_decisions", meeting.recommended_decisions)) if meeting_item else meeting.recommended_decisions,
        "evidence_references": list(meeting_item.extensions.get("evidence_references", meeting.evidence_references)) if meeting_item else meeting.evidence_references,
        "confidence": meeting_item.confidence if meeting_item else meeting.confidence,
    }


def _build_board_page(state: ExecutiveState) -> dict[str, Any]:
    board = state.board
    return {
        "summary": list(board.registry_summary),
        "members": [_serialize_board_member(member) for member in board.board_members],
        "weekly_meeting": list(board.weekly_board_meeting),
        "monthly_meeting": list(board.monthly_board_meeting),
        "standing_agenda": list(board.standing_agenda),
    }


def _filter_components(components: list[dict[str, Any]], categories: set[str]) -> list[dict[str, Any]]:
    return [component for component in components if component["category"] in categories]


def _operational_action(label: str, command: str, summary: str, work_instruction_link: str) -> dict[str, str]:
    return {
        "label": label,
        "command": command,
        "summary": summary,
        "work_instruction_link": work_instruction_link,
        "mode": "CLI-backed",
    }


def _build_admin_configuration_page() -> dict[str, Any]:
    inventory = build_environment_inventory()
    doctor_summary = build_doctor_summary(inventory)
    readiness = build_operational_readiness()
    components = [component for component in inventory.as_dict()["components"]]
    actions = [
        _operational_action("Discover Environment", "python build_environment_inventory.py", "Re-scan the runtime and refresh the persistent environment inventory.", "docs/deployment/INSTALLATION_GUIDE.md"),
        _operational_action("Auto Configure", "scripts/install/install_alfred_platform.sh --mode local --source-dir .", "Apply high-confidence discovered configuration during installation.", "docs/deployment/INSTALLATION_GUIDE.md"),
        _operational_action("Run Health Check", "python build_operational_readiness.py", "Refresh Alfred Doctor and platform health state.", "docs/deployment/POST_INSTALL_VALIDATION.md"),
        _operational_action("Run Operational Readiness", "python build_operational_readiness.py", "Rebuild the operational readiness report and JSON payload.", "docs/deployment/POST_INSTALL_VALIDATION.md"),
        _operational_action("Run Live Knowledge Certification", "python build_live_knowledge_certification.py", "Certify that Alfred is reading live Obsidian executive knowledge.", "docs/deployment/POST_INSTALL_VALIDATION.md"),
        _operational_action("Generate Deployment Report", "python build_everything.py", "Regenerate the full deployment-facing report set.", "docs/deployment/INSTALLATION_GUIDE.md"),
    ]
    return {
        "overview": {
            "environment_score": doctor_summary["environment_score"],
            "overall_health": readiness.overall_health,
            "architecture_rule": inventory.architecture_rule,
            "summary_lines": doctor_summary["summary_lines"],
        },
        "sections": {
            "core_configuration": _filter_components(components, {"Runtime"}),
            "vault": _filter_components(components, {"Vault"}),
            "ai_providers": _filter_components(components, {"AI Providers"}),
            "knowledge_sources": _filter_components(components, {"Knowledge Sources"}),
            "runtime": _filter_components(components, {"Runtime"}),
            "services": _filter_components(components, {"Services"}),
            "security": [
                {
                    "name": "Secrets Exposure Policy",
                    "status": "CONFIGURED",
                    "health": "HEALTHY",
                    "version": "n/a",
                    "install_location": "",
                    "configuration_source": "product policy",
                    "required": True,
                    "dependencies": [],
                    "last_checked": inventory.generated_at,
                    "last_changed": "",
                    "recommended_action": "Keep secrets in environment or secret stores; never render values in Alfred.",
                    "work_instruction_link": "docs/deployment/INSTALLATION_GUIDE.md",
                }
            ],
            "diagnostics": [
                {
                    "name": "Alfred Doctor",
                    "status": readiness.overall_health,
                    "health": readiness.overall_health,
                    "version": "n/a",
                    "install_location": "output/Operational_Readiness_Report.md",
                    "configuration_source": "build_operational_readiness.py",
                    "required": True,
                    "dependencies": ["Environment Inventory", "Executive Pipeline"],
                    "last_checked": readiness.generated_at,
                    "last_changed": "",
                    "recommended_action": doctor_summary["recommended_actions"][0] if doctor_summary["recommended_actions"] else "No action required.",
                    "work_instruction_link": "docs/deployment/POST_INSTALL_VALIDATION.md",
                }
            ],
            "deployment": actions,
            "required_actions": list(inventory.required_actions),
        },
        "auto_configured": {
            key: {
                "value": value.value,
                "discovery_method": value.discovery_method,
                "confidence": value.confidence,
                "timestamp": value.timestamp,
            }
            for key, value in inventory.auto_configured.items()
        },
        "doctor_summary": doctor_summary,
        "actions": actions,
    }


def _build_ask_alfred_page(state: ExecutiveState) -> dict[str, Any]:
    responses = []
    for question in ASK_ALFRED_QUESTIONS:
        response = ask_alfred_from_state(question, state)
        responses.append(
            {
                "question": question,
                "executive_answer": response.executive_answer,
                "supporting_evidence": response.supporting_evidence,
                "confidence": response.confidence,
                "recommended_next_actions": response.recommended_next_actions,
            }
        )
    return {
        "questions": list(ASK_ALFRED_QUESTIONS),
        "responses": responses,
    }


def _build_daily_brief_page(brief: DailyBrief) -> dict[str, Any]:
    return {
        "executive_health": brief.executive_health,
        "overnight_changes": brief.overnight_changes,
        "top_three_priorities": brief.top_three_priorities,
        "meetings_requiring_preparation": brief.meetings_requiring_preparation,
        "followups_due_today": brief.followups_due_today,
        "open_loops_blocking_progress": brief.open_loops_blocking_progress,
        "risks_escalating": brief.risks_escalating,
        "decisions_awaiting_you": brief.decisions_awaiting_you,
        "recommended_agenda": brief.recommended_agenda,
        "one_page_executive_summary": brief.one_page_executive_summary,
        "confidence": brief.confidence,
    }


def _build_knowledge_page(state: ExecutiveState) -> dict[str, Any]:
    graph = state.relationship_graph
    return {
        "summary": list(state.summary),
        "entity_counts": {
            "objectives": len(state.objectives),
            "projects": len(state.projects),
            "companies": len(state.companies),
            "people": len(state.people),
            "decisions": len(state.decisions),
            "policies": len(state.policies),
        },
        "graph": {
            "node_count": graph.statistics["node_count"],
            "edge_count": graph.statistics["edge_count"],
            "top_nodes": [node.label for node in graph.highest_connectivity[:5]],
        },
    }


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


def _evidence_card(
    item_type: str,
    summary: str,
    provider: str,
    confidence: str,
    source_notes: list[str],
    *,
    origin: str | None = None,
) -> dict[str, Any]:
    return {
        "type": item_type,
        "summary": summary,
        "origin": origin or provider,
        "confidence": confidence,
        "source_notes": source_notes,
        "provider": provider,
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


def _serialize_board_member(member: BoardMember) -> dict[str, Any]:
    return {
        "name": member.name,
        "role": member.role,
        "purpose": member.purpose,
        "responsibilities": list(member.responsibilities),
        "authority": member.authority,
        "meeting_role": member.meeting_role,
        "weekly_board_contribution": member.weekly_board_contribution,
        "monthly_board_contribution": member.monthly_board_contribution,
        "prompt_profile": member.prompt_profile,
        "communication_style": member.communication_style,
        "portrait_placeholder": member.portrait_placeholder,
        "status": member.status,
    }
