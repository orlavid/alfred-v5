"""Pure Python dashboard API for Alfred."""

from __future__ import annotations

import hashlib
import re
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
from src.management.objectives import load_objective_management_store, merge_objective_detail
from src.management.projects import load_project_management_store, merge_project_detail
from src.objectives.objective_intelligence import (
    ObjectiveView,
    build_objective_intelligence_from_state,
    build_objective_views_from_state,
)
from src.operations.doctor import build_operational_readiness
from src.operations.environment_discovery import build_doctor_summary, build_environment_inventory
from executive.knowledge.resolver import normalise_name

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
        "decisions": _build_decisions_page(state, read_model=read_model),
        "followups": _build_followups_page(state),
        "open_loops": _build_open_loops_page(state),
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
    management_store = load_objective_management_store()
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
        detail["relationship_options"] = _build_objective_relationship_options(state)
        detail = merge_objective_detail(detail, management_store.get("objectives", {}).get(objective_id))
        detail["missing_information"] = _recalculate_objective_missing_information(detail)
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
    open_loops = [item for item in open_actions if item["type"] != "follow_up"]
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
        "open_loops": open_loops,
        "dependencies": list(contract.dependencies),
        "relevant_meetings": relevant_meetings,
        "related_people": related_people,
        "evidence_sources": evidence_sources,
        "recent_changes": recent_changes,
        "recommended_next_action": recommended_next_action,
        "key_risk_or_blocker": key_risk_or_blocker,
        "missing_information": missing_information,
        "smart_assessment": smart_assessment,
        "proposed_smart_refinement": _build_smart_refinement(contract, smart_assessment),
        "contributors": [],
        "priority": "Not defined",
        "progress_percentage": None,
        "success_measures": [],
        "milestones": [],
        "resources": [],
        "management_notes": [],
        "audit_history": [],
        "smart_enrichment_proposal": None,
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


def _recalculate_objective_missing_information(detail: dict[str, Any]) -> list[str]:
    items: list[str] = []
    if detail.get("owner", "Not defined") == "Not defined":
        items.append("Accountable owner is not defined.")
    if detail.get("target_date", "Not defined") == "Not defined":
        items.append("Target date is not defined.")
    if detail.get("last_review_date", "Not defined") == "Not defined" and detail.get("next_review_date", "Not defined") == "Not defined":
        items.append("Review cadence is not defined.")
    if not detail.get("supporting_projects"):
        items.append("No supporting projects are linked.")
    if not detail.get("related_people"):
        items.append("No related people are linked.")
    for dimension, payload in detail.get("smart_assessment", {}).items():
        if payload.get("current_assessment") != "Evidence-backed":
            items.append(f"{dimension.capitalize()} is weakly defined.")
    return list(dict.fromkeys(items)) or ["No material missing information identified."]


def _build_objective_relationship_options(state: ExecutiveState) -> dict[str, list[dict[str, str]]]:
    return {
        "supporting_projects": [
            {
                "id": _stable_related_id("project", project.path),
                "title": project.title,
                "path": project.path,
                "reason": project.recommendation,
                "route": "/projects",
            }
            for project in state.projects
        ],
        "linked_decisions": [
            {
                "id": _stable_related_id("decision", item.get("path", item["title"])),
                "title": item["title"],
                "path": item.get("path", ""),
                "reason": f"Importance {item['importance']}; linked to {item['projects']} projects and {item['objectives']} objectives.",
                "route": "/decisions",
            }
            for item in state.decisions
        ],
        "follow_ups": [
            {
                "id": _stable_related_id("follow_up", f"{item.path}:{normalise_name(item.summary)}"),
                "title": item.title,
                "path": item.path,
                "reason": item.summary,
                "route": "/follow-ups",
            }
            for item in (state.followups.all_items if state.followups is not None else ())
        ],
        "open_loops": [
            {
                "id": _stable_related_id("open_loop", f"{item.path}:{normalise_name(item.summary)}"),
                "title": item.title,
                "path": item.path,
                "reason": item.summary,
                "route": "/open-loops",
            }
            for item in (state.open_loops.all_items if state.open_loops is not None else ())
        ],
        "related_people": [
            {
                "id": _stable_related_id("person", person.path),
                "title": person.title,
                "path": person.path,
                "reason": f"Linked to {person.projects} projects, {person.objectives} objectives, and {person.decisions} decisions.",
                "route": "/people",
            }
            for person in state.people
        ],
        "relevant_meetings": [
            {
                "id": _stable_related_id("meeting", meeting.subject),
                "title": meeting.subject,
                "path": meeting.matched_entities[0].path if meeting.matched_entities else "",
                "reason": meeting.recommended_discussion[0] if meeting.recommended_discussion else "Relevant meeting context exists.",
                "route": "/meetings",
            }
            for meeting in state.meetings
        ],
    }


def _build_project_relationship_options(state: ExecutiveState) -> dict[str, list[dict[str, str]]]:
    return {
        "linked_objectives": [
            {
                "id": _stable_related_id("objective", objective.path),
                "title": objective.title,
                "path": objective.path,
                "reason": objective.recommendation,
                "route": f"/objectives/{_stable_objective_id(_project_entity_id_by_path(state, objective.path, 'objective'))}" if _project_entity_id_by_path(state, objective.path, "objective") else "/objectives",
            }
            for objective in state.objectives
        ],
        "linked_decisions": [
            {
                "id": _stable_related_id("decision", item.get("path", item["title"])),
                "title": item["title"],
                "path": item.get("path", ""),
                "reason": f"Importance {item['importance']}; linked to {item['projects']} projects and {item['objectives']} objectives.",
                "route": "/decisions",
            }
            for item in state.decisions
        ],
        "follow_ups": [
            {
                "id": _stable_related_id("follow_up", f"{item.path}:{normalise_name(item.summary)}"),
                "title": item.title,
                "path": item.path,
                "reason": item.summary,
                "route": "/follow-ups",
            }
            for item in (state.followups.all_items if state.followups is not None else ())
        ],
        "open_loops": [
            {
                "id": _stable_related_id("open_loop", f"{item.path}:{normalise_name(item.summary)}"),
                "title": item.title,
                "path": item.path,
                "reason": item.summary,
                "route": "/open-loops",
            }
            for item in (state.open_loops.all_items if state.open_loops is not None else ())
        ],
        "related_people": [
            {
                "id": _stable_related_id("person", person.path),
                "title": person.title,
                "path": person.path,
                "reason": f"Linked to {person.projects} projects, {person.objectives} objectives, and {person.decisions} decisions.",
                "route": "/people",
            }
            for person in state.people
        ],
        "relevant_meetings": [
            {
                "id": _stable_related_id("meeting", meeting.subject),
                "title": meeting.subject,
                "path": meeting.matched_entities[0].path if meeting.matched_entities else "",
                "reason": meeting.recommended_discussion[0] if meeting.recommended_discussion else "Relevant meeting context exists.",
                "route": "/meetings",
            }
            for meeting in state.meetings
        ],
        "related_companies": [
            {
                "id": _stable_related_id("company", company.path),
                "title": company.title,
                "path": company.path,
                "reason": f"Linked to {company.projects} projects and {company.objectives} objectives.",
                "route": "/companies",
            }
            for company in state.companies
        ],
    }


def _project_entity_id_by_path(state: ExecutiveState, path: str, entity_type: str) -> str | None:
    for entity in state.canonical_entities:
        if entity.entity_type == entity_type and entity.primary_path == path:
            return entity.entity_id
    return None


def _related_contract_items(names: tuple[str, ...] | list[str], items: tuple[Any, ...], *, route_prefix: str, id_kind: str, route_lookup: dict[str, str] | None = None) -> list[dict[str, str]]:
    lookup = {item.title: item for item in items}
    related_items: list[dict[str, str]] = []
    for name in names:
        item = lookup.get(name)
        path = getattr(item, "path", "") if item is not None else ""
        route = route_lookup.get(name, route_prefix) if route_lookup else route_prefix
        related_items.append(
            {
                "id": _stable_related_id(id_kind, path or name),
                "title": name,
                "path": path,
                "reason": "Connected in canonical executive state.",
                "route": route,
            }
        )
    return related_items


def _related_project_work_items(state: ExecutiveState, contract: CanonicalExecutiveEntityContract) -> list[Any]:
    return [
        item
        for item in state.work_items
        if contract.canonical_name in item.related_projects
        or contract.canonical_name in item.related_entities
    ]


def _related_project_decisions(contract: CanonicalExecutiveEntityContract, state: ExecutiveState) -> list[dict[str, str]]:
    entity_lookup = {entity.id: entity for entity in state.entities}
    decision_lookup = {item["title"]: item for item in state.decisions}
    items: list[dict[str, str]] = []
    for entity_id in state.neighbours.get(contract.primary_path, ()):
        entity = entity_lookup.get(entity_id)
        if entity is None or getattr(entity, "type", None) != "decision":
            continue
        decision = decision_lookup.get(entity.title)
        if decision is None:
            continue
        items.append(
            {
                "title": decision["title"],
                "path": decision.get("path", ""),
                "reason": f"Importance {decision['importance']}; linked to {decision['projects']} projects and {decision['objectives']} objectives.",
                "route": "/decisions",
            }
        )
    return items


def _related_project_meetings(state: ExecutiveState, contract: CanonicalExecutiveEntityContract) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for meeting in state.meetings:
        if contract.canonical_name not in [item.title for item in meeting.related_projects]:
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


def _related_project_companies(state: ExecutiveState, contract: CanonicalExecutiveEntityContract) -> list[dict[str, str]]:
    entity_lookup = {entity.id: entity for entity in state.entities}
    company_lookup = {item.title: item for item in state.companies}
    items: list[dict[str, str]] = []
    for entity_id in state.neighbours.get(contract.primary_path, ()):
        entity = entity_lookup.get(entity_id)
        if entity is None or getattr(entity, "type", None) != "company":
            continue
        company = company_lookup.get(entity.title)
        reason = "Connected to the project through the executive knowledge graph."
        if company is not None:
            reason = f"Linked to {company.projects} projects and {company.objectives} objectives."
        items.append(
            {
                "id": _stable_related_id("company", entity.path),
                "title": entity.title,
                "path": entity.path,
                "reason": reason,
                "route": "/companies",
            }
        )
    return items


def _related_decision_companies(state: ExecutiveState, contract: CanonicalExecutiveEntityContract) -> list[dict[str, str]]:
    entity_lookup = {entity.id: entity for entity in state.entities}
    company_lookup = {item.title: item for item in state.companies}
    items: list[dict[str, str]] = []
    for entity_id in state.neighbours.get(contract.primary_path, ()):
        entity = entity_lookup.get(entity_id)
        if entity is None or getattr(entity, "type", None) != "company":
            continue
        company = company_lookup.get(entity.title)
        reason = "Connected to the decision through the executive knowledge graph."
        if company is not None:
            reason = f"Linked to {company.projects} projects and {company.objectives} objectives."
        items.append(
            {
                "id": _stable_related_id("company", entity.path),
                "title": entity.title,
                "path": entity.path,
                "reason": reason,
                "route": "/companies",
            }
        )
    return items


def _related_decision_work_items(state: ExecutiveState, contract: CanonicalExecutiveEntityContract) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for item in state.work_items:
        related_names = set(item.related_entities)
        legacy_title = item.extensions.get("legacy_title")
        if isinstance(legacy_title, str) and legacy_title:
            related_names.add(legacy_title)
        if contract.canonical_name not in related_names:
            continue
        items.append(
            {
                "work_item_id": item.work_item_id,
                "title": item.title,
                "path": item.evidence_paths[0] if item.evidence_paths else "",
                "reason": _work_item_reason(item),
                "route": "/follow-ups" if item.work_item_type == "follow_up" else "/open-loops",
                "type": item.work_item_type,
            }
        )
    return items


def _related_decision_meetings(state: ExecutiveState, contract: CanonicalExecutiveEntityContract) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for meeting in state.meetings:
        if contract.canonical_name not in [item.title for item in meeting.related_decisions]:
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


def _decision_rationale(contract: CanonicalExecutiveEntityContract, raw_entities: dict[str, Any]) -> str:
    snippet = _objective_definition(contract, raw_entities)
    return snippet if snippet != "No evidence found." else "No rationale found in the source evidence."


def _build_decision_recent_changes(contract: CanonicalExecutiveEntityContract, related_work_items: list[dict[str, str]]) -> list[str]:
    changes: list[str] = []
    if contract.last_activity:
        changes.append(f"Last meaningful activity recorded on {contract.last_activity}.")
    if related_work_items:
        changes.append(f"{len(related_work_items)} related work item(s) currently reference this decision.")
    return changes or ["No evidence found."]


def _decision_missing_information(contract: CanonicalExecutiveEntityContract, *, rationale: str) -> list[str]:
    items: list[str] = []
    if not contract.owner:
        items.append("Accountable owner is not defined.")
    if not contract.status:
        items.append("Decision status is not defined.")
    if not contract.created and not contract.last_activity and not contract.review_date:
        items.append("Decision date is not defined.")
    if rationale == "No rationale found in the source evidence.":
        items.append("Decision rationale is not explicit in the source evidence.")
    return items or ["No material missing information identified."]


def _project_blockers(contract: CanonicalExecutiveEntityContract, related_work_items: list[Any]) -> list[dict[str, str]]:
    items = []
    for item in related_work_items:
        if item.work_item_type not in {"open_loop", "decision_review", "follow_up"}:
            continue
        items.append(
            {
                "title": item.title,
                "path": item.evidence_paths[0] if item.evidence_paths else "",
                "reason": _work_item_reason(item),
                "type": item.work_item_type,
                "route": "/follow-ups" if item.work_item_type == "follow_up" else "/open-loops",
            }
        )
    for dependency in contract.dependencies:
        items.append(
            {
                "title": dependency,
                "path": "",
                "reason": "Dependency linked to the project in canonical executive state.",
                "type": "dependency",
                "route": "/open-loops",
            }
        )
    deduped = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        key = (item["title"], item["type"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped[:12]


def _build_project_progress_assessment(
    contract: CanonicalExecutiveEntityContract,
    linked_objectives: list[dict[str, str]],
    linked_decisions: list[dict[str, str]],
    related_work_items: list[Any],
    project,
) -> str:
    signals = []
    if contract.status:
        signals.append(contract.status)
    elif getattr(project, "status", None):
        signals.append(project.status)
    signals.append(f"{getattr(project, 'linked_entities', 0)} linked entities")
    if linked_objectives:
        signals.append(f"{len(linked_objectives)} linked objective(s)")
    if linked_decisions:
        signals.append(f"{len(linked_decisions)} linked decision(s)")
    if related_work_items:
        signals.append(f"{len(related_work_items)} open work item(s)")
    return ", ".join(signals) if signals else "No evidence found."


def _build_project_recent_changes(
    contract: CanonicalExecutiveEntityContract,
    linked_decisions: list[dict[str, str]],
    related_work_items: list[Any],
) -> list[str]:
    changes = []
    if contract.last_activity:
        changes.append(f"Last meaningful activity recorded on {contract.last_activity}.")
    if linked_decisions:
        changes.append(f"{len(linked_decisions)} linked decision(s) remain active.")
    if related_work_items:
        changes.append(f"{len(related_work_items)} open work item(s) remain linked to this project.")
    return changes or ["No evidence found."]


def _project_missing_information(
    contract: CanonicalExecutiveEntityContract,
    *,
    linked_objectives: list[dict[str, str]],
    related_people: list[dict[str, str]],
    executive_definition: str,
) -> list[str]:
    items: list[str] = []
    if not contract.owner:
        items.append("Accountable owner is not defined.")
    if not contract.due_date:
        items.append("Target date is not defined.")
    if not contract.review_date:
        items.append("Review cadence is not defined.")
    if not linked_objectives:
        items.append("No linked objectives are defined.")
    if not related_people:
        items.append("No related people are linked.")
    if executive_definition == "No evidence found.":
        items.append("Executive definition is not explicit in the current evidence.")
    return items or ["No material missing information identified."]


def _recalculate_project_missing_information(detail: dict[str, Any]) -> list[str]:
    items: list[str] = []
    if detail.get("owner", "Not defined") == "Not defined":
        items.append("Accountable owner is not defined.")
    if detail.get("target_date", "Not defined") == "Not defined":
        items.append("Target date is not defined.")
    if detail.get("last_review_date", "Not defined") == "Not defined" and detail.get("next_review_date", "Not defined") == "Not defined":
        items.append("Review cadence is not defined.")
    if not detail.get("linked_objectives"):
        items.append("No linked objectives are defined.")
    if not detail.get("related_people"):
        items.append("No related people are linked.")
    return list(dict.fromkeys(items)) or ["No material missing information identified."]


def _stable_objective_id(entity_id: str) -> str:
    return hashlib.sha1(entity_id.encode("utf-8")).hexdigest()[:12]


def _stable_project_id(entity_id: str) -> str:
    return hashlib.sha1(entity_id.encode("utf-8")).hexdigest()[:12]


def _stable_decision_id(entity_id: str) -> str:
    return hashlib.sha1(entity_id.encode("utf-8")).hexdigest()[:12]


def _stable_related_id(kind: str, value: str) -> str:
    return hashlib.sha1(f"{kind}:{value}".encode("utf-8")).hexdigest()[:12]


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
    project_contracts = {
        entity.primary_path: entity
        for entity in state.canonical_entities
        if entity.entity_type == "project"
    }
    management_store = load_project_management_store()
    details: dict[str, Any] = {}
    items = []
    for project in state.projects:
        contract = project_contracts.get(project.path)
        if contract is None:
            continue
        project_id = _stable_project_id(contract.entity_id)
        detail = _build_project_detail(state, contract=contract, project=project, project_id=project_id)
        detail["relationship_options"] = _build_project_relationship_options(state)
        detail = merge_project_detail(detail, management_store.get("projects", {}).get(project_id))
        detail["missing_information"] = _recalculate_project_missing_information(detail)
        details[project_id] = detail
        items.append(
            {
                "project_id": project_id,
                "title": detail["title"],
                "source_path": detail["source_path"],
                "source_entity_id": detail["source_entity_id"],
                "route": detail["route"],
                "status": detail["current_status"],
                "health": detail["health"],
                "owner": detail["owner"],
                "progress_indicator": detail["progress_assessment"],
                "last_meaningful_activity": detail["last_meaningful_activity"],
                "next_checkpoint_or_deadline": detail["next_checkpoint_or_deadline"],
                "objective_linkage": [item["title"] for item in detail["linked_objectives"]],
                "linked_decision_count": len(detail["linked_decisions"]),
                "open_action_count": len(detail["open_actions"]),
                "evidence_confidence": detail["evidence_confidence"],
                "risk": detail["key_risk_or_blocker"],
                "recommendation": detail["recommended_next_action"],
                "missing_fields": detail["missing_information"],
            }
        )
    return {
        "health": state.project_health,
        "items": items,
        "details": details,
        "summary": [
            f"Projects tracked: {len(state.projects)}.",
            f"Projects at risk: {state.project_health.get('at_risk', 0)}.",
        ],
    }


def _build_decisions_page(state: ExecutiveState, *, read_model=None) -> dict[str, Any]:
    effective_read_model = read_model or build_unified_executive_read_model(state)
    decision_contracts = {
        entity.primary_path: entity
        for entity in state.canonical_entities
        if _is_dashboard_decision_entity(entity)
    }
    decision_index = {item.get("path"): item for item in state.decisions if item.get("path")}
    decision_index_by_title = {item.get("title"): item for item in state.decisions if item.get("title")}
    details: dict[str, Any] = {}
    items: list[dict[str, Any]] = []
    contracts_used = len(decision_contracts)

    for contract in sorted(decision_contracts.values(), key=lambda entity: (entity.canonical_name.lower(), entity.primary_path)):
        decision = decision_index.get(contract.primary_path) or decision_index_by_title.get(contract.canonical_name) or {
            "title": contract.canonical_name,
            "importance": 0,
            "path": contract.primary_path,
        }
        decision_id = _stable_decision_id(contract.entity_id)
        detail = _build_decision_detail(state, effective_read_model, contract=contract, decision=decision, decision_id=decision_id)
        details[decision_id] = detail
        items.append(
            {
                "decision_id": decision_id,
                "title": detail["title"],
                "source_path": detail["source_path"],
                "source_entity_id": detail["source_entity_id"],
                "route": detail["route"],
                "status": detail["current_status"],
                "owner": detail["owner"],
                "decision_date": detail["decision_date"],
                "related_project_count": len(detail["related_projects"]),
                "related_objective_count": len(detail["related_objectives"]),
                "related_people_count": len(detail["related_people"]),
                "evidence_confidence": detail["evidence_confidence"],
                "rationale": detail["rationale"],
                "missing_fields": detail["missing_information"],
                "importance": detail["importance"],
            }
        )

    status_counts = {"total": len(items), "defined_status": 0, "owner_defined": 0}
    for detail in details.values():
        if detail["current_status"] != "Not defined":
            status_counts["defined_status"] += 1
        if detail["owner"] != "Not defined":
            status_counts["owner_defined"] += 1

    return {
        "counts": {
            **status_counts,
            "source_notes": contracts_used,
        },
        "items": items,
        "details": details,
        "summary": [
            f"Decision records tracked: {len(items)}.",
            f"Owners defined: {status_counts['owner_defined']}.",
            f"Statuses defined: {status_counts['defined_status']}.",
        ],
    }


def _is_dashboard_decision_entity(entity: CanonicalExecutiveEntityContract) -> bool:
    if entity.entity_type != "decision":
        return False
    path = entity.primary_path.replace("\\", "/")
    lowered_title = entity.canonical_name.lower()
    if not path.startswith("04 Decisions/"):
        return False
    if "template" in lowered_title:
        return False
    return True


def _build_project_detail(
    state: ExecutiveState,
    *,
    contract: CanonicalExecutiveEntityContract,
    project,
    project_id: str,
) -> dict[str, Any]:
    related_work_items = _related_project_work_items(state, contract)
    objective_routes = {
        entity.canonical_name: f"/objectives/{_stable_objective_id(entity.entity_id)}"
        for entity in state.canonical_entities
        if entity.entity_type == "objective"
    }
    linked_objectives = _related_contract_items(
        contract.related_objectives,
        state.objectives,
        route_prefix="/objectives",
        id_kind="objective",
        route_lookup=objective_routes,
    )
    linked_decisions = _related_project_decisions(contract, state)
    related_people = _related_people_items(contract, state)
    related_companies = _related_project_companies(state, contract)
    relevant_meetings = _related_project_meetings(state, contract)
    blockers = _project_blockers(contract, related_work_items)
    evidence_sources = _objective_evidence_sources(contract, {entity.id: entity for entity in state.entities})
    current_status = contract.status or project.status or "Not defined"
    rag_rating = _status_to_rag(current_status)
    progress_assessment = _build_project_progress_assessment(contract, linked_objectives, linked_decisions, related_work_items, project)
    executive_definition = _objective_definition(contract, {entity.id: entity for entity in state.entities})
    last_review_date, next_review_date = _review_window(contract.review_date)
    recent_changes = _build_project_recent_changes(contract, linked_decisions, related_work_items)
    open_actions = _build_open_action_items(related_work_items)
    followups = [item for item in open_actions if item["type"] == "follow_up"]
    open_loops = [item for item in open_actions if item["type"] != "follow_up"]
    next_checkpoint = contract.due_date or _future_review_date(contract.review_date) or "Not defined"
    missing_information = _project_missing_information(contract, linked_objectives=linked_objectives, related_people=related_people, executive_definition=executive_definition)
    recommended_next_action = project.recommendation

    return {
        "project_id": project_id,
        "route": f"/projects/{project_id}",
        "title": contract.canonical_name,
        "source_entity_id": contract.entity_id,
        "source_path": contract.primary_path,
        "executive_definition": executive_definition,
        "owner": contract.owner or "Not defined",
        "delegates": list(contract.delegates),
        "contributors": [],
        "current_status": current_status,
        "health": rag_rating,
        "rag_rating": rag_rating,
        "progress_assessment": progress_assessment,
        "progress_percentage": None,
        "priority": contract.priority or "Not defined",
        "evidence_confidence": contract.confidence,
        "start_date": contract.created or "Not defined",
        "target_date": contract.due_date or "Not defined",
        "last_review_date": last_review_date,
        "next_review_date": next_review_date,
        "last_meaningful_activity": contract.last_activity or "No evidence found",
        "next_checkpoint_or_deadline": next_checkpoint,
        "linked_objectives": linked_objectives,
        "linked_decisions": linked_decisions,
        "risks_and_blockers": blockers,
        "open_actions": open_actions,
        "follow_ups": followups,
        "open_loops": open_loops,
        "dependencies": list(contract.dependencies),
        "relevant_meetings": relevant_meetings,
        "related_people": related_people,
        "related_companies": related_companies,
        "evidence_sources": evidence_sources,
        "recent_changes": recent_changes,
        "recommended_next_action": recommended_next_action,
        "key_risk_or_blocker": blockers[0]["title"] if blockers else "No evidence found",
        "missing_information": missing_information,
        "success_measures": [],
        "milestones": [],
        "resources": [],
        "management_notes": [],
        "audit_history": [],
        "stale_evidence": contract.last_activity is None,
        "provenance": {
            "project": list(contract.evidence_paths),
            "linked_objectives": [item["path"] for item in linked_objectives if item["path"]],
            "linked_decisions": [item["path"] for item in linked_decisions if item["path"]],
            "open_actions": [item["path"] for item in open_actions if item["path"]],
            "related_people": [item["path"] for item in related_people if item["path"]],
            "related_companies": [item["path"] for item in related_companies if item["path"]],
        },
    }


def _build_decision_detail(
    state: ExecutiveState,
    read_model,
    *,
    contract: CanonicalExecutiveEntityContract,
    decision: dict[str, Any],
    decision_id: str,
) -> dict[str, Any]:
    del read_model
    rationale = _decision_rationale(contract, {entity.id: entity for entity in state.entities})
    related_projects = _related_contract_items(
        contract.related_projects,
        state.projects,
        route_prefix="/projects",
        id_kind="project",
        route_lookup={
            entity.canonical_name: f"/projects/{_stable_project_id(entity.entity_id)}"
            for entity in state.canonical_entities
            if entity.entity_type == "project"
        },
    )
    related_objectives = _related_contract_items(
        contract.related_objectives,
        state.objectives,
        route_prefix="/objectives",
        id_kind="objective",
        route_lookup={
            entity.canonical_name: f"/objectives/{_stable_objective_id(entity.entity_id)}"
            for entity in state.canonical_entities
            if entity.entity_type == "objective"
        },
    )
    related_people = _related_people_items(contract, state)
    related_companies = _related_decision_companies(state, contract)
    related_work_items = _related_decision_work_items(state, contract)
    relevant_meetings = _related_decision_meetings(state, contract)
    evidence_sources = _objective_evidence_sources(contract, {entity.id: entity for entity in state.entities})
    decision_date = contract.created or contract.last_activity or contract.review_date or "Not defined"
    current_status = contract.status or "Not defined"
    recent_changes = _build_decision_recent_changes(contract, related_work_items)
    missing_information = _decision_missing_information(contract, rationale=rationale)

    return {
        "decision_id": decision_id,
        "route": f"/decisions/{decision_id}",
        "title": contract.canonical_name,
        "source_entity_id": contract.entity_id,
        "source_path": contract.primary_path,
        "decision_date": decision_date,
        "current_status": current_status,
        "owner": contract.owner or "Not defined",
        "importance": decision["importance"],
        "evidence_confidence": contract.confidence,
        "rationale": rationale,
        "related_projects": related_projects,
        "related_objectives": related_objectives,
        "related_people": related_people,
        "related_companies": related_companies,
        "related_work_items": related_work_items,
        "relevant_meetings": relevant_meetings,
        "evidence_sources": evidence_sources,
        "recent_changes": recent_changes,
        "missing_information": missing_information,
        "stale_evidence": not bool(contract.last_activity),
        "source_entities": [contract.entity_id],
        "source_work_items": [item["work_item_id"] for item in related_work_items if item.get("work_item_id")],
        "provenance": {
            "decision": list(contract.evidence_paths),
            "owner": list(contract.provenance.get("owner", ())),
            "status": list(contract.provenance.get("status", ())),
            "related_projects": [item["path"] for item in related_projects if item["path"]],
            "related_objectives": [item["path"] for item in related_objectives if item["path"]],
            "related_people": [item["path"] for item in related_people if item["path"]],
            "related_companies": [item["path"] for item in related_companies if item["path"]],
            "related_work_items": [item["path"] for item in related_work_items if item["path"]],
        },
    }


def _build_followups_page(state: ExecutiveState) -> dict[str, Any]:
    work_item_lookup = {
        (item.evidence_paths[0] if item.evidence_paths else "", normalise_name(item.title)): item
        for item in state.work_items
        if item.work_item_type == "follow_up"
    }
    items = [
        _serialize_followup_item(item, work_item_lookup.get((item.path, normalise_name(item.summary))))
        for item in sorted(
            state.followups.all_items,
            key=_followup_item_sort_key,
        )
    ]
    return {
        "counts": {
            "total": len(items),
            "overdue": len(state.followups.overdue),
            "due_today": len(state.followups.due_today),
            "due_this_week": len(state.followups.due_this_week),
            "waiting_on_others": len(state.followups.waiting_on_others),
            "high_priority": len(state.followups.high_priority),
        },
        "items": items,
        "summary": list(state.followups.executive_summary),
        "recommendations": list(state.followups.recommendations),
    }


def _build_open_loops_page(state: ExecutiveState) -> dict[str, Any]:
    work_item_lookup = {
        (item.evidence_paths[0] if item.evidence_paths else "", normalise_name(str(item.extensions.get("summary", item.title)))): item
        for item in state.work_items
        if item.work_item_type in {"open_loop", "decision_review"}
    }
    items = [
        _serialize_open_loop_item(item, work_item_lookup.get((item.path, normalise_name(item.summary))))
        for item in sorted(
            state.open_loops.all_items,
            key=_open_loop_item_sort_key,
        )
    ]
    return {
        "counts": {
            "total": len(items),
            "critical": len(state.open_loops.critical_open_loops),
            "waiting_for": len(state.open_loops.waiting_for),
            "stalled_projects": len(state.open_loops.stalled_projects),
            "missing_decisions": len(state.open_loops.missing_decisions),
            "missing_owners": len(state.open_loops.missing_owners),
        },
        "items": items,
        "summary": list(state.open_loops.executive_summary),
        "recommended_actions": list(state.open_loops.recommended_actions),
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
    meeting_purpose = list(getattr(meeting, "meeting_purpose", []))
    relationship_history = list(getattr(meeting, "relationship_history", []))
    commercial_issues = list(getattr(meeting, "commercial_issues", []))
    recent_changes = list(getattr(meeting, "recent_changes", []))
    dependencies = list(getattr(meeting, "dependencies", []))
    recommended_questions = list(getattr(meeting, "recommended_questions", []))
    recommended_decisions = list(getattr(meeting, "recommended_decisions", []))
    evidence_references = list(getattr(meeting, "evidence_references", []))
    return {
        "subject": meeting.subject,
        "meeting_purpose": list(meeting_item.extensions.get("meeting_purpose", meeting_purpose)) if meeting_item else meeting_purpose,
        "executive_summary": list(meeting_item.extensions.get("executive_summary", meeting.executive_summary)) if meeting_item else meeting.executive_summary,
        "relationship_history": list(meeting_item.extensions.get("relationship_history", relationship_history)) if meeting_item else relationship_history,
        "related_people": list(meeting_item.extensions.get("related_people", [item.title for item in meeting.related_people])) if meeting_item else [item.title for item in meeting.related_people],
        "related_projects": list(meeting_item.extensions.get("related_projects", [item.title for item in meeting.related_projects])) if meeting_item else [item.title for item in meeting.related_projects],
        "related_companies": list(meeting_item.extensions.get("related_companies", [item.title for item in meeting.related_companies])) if meeting_item else [item.title for item in meeting.related_companies],
        "related_objectives": list(meeting_item.extensions.get("related_objectives", [item.title for item in meeting.related_objectives])) if meeting_item else [item.title for item in meeting.related_objectives],
        "related_decisions": list(meeting_item.extensions.get("related_decisions", [item.title for item in meeting.related_decisions])) if meeting_item else [item.title for item in meeting.related_decisions],
        "risks": list(meeting_item.extensions.get("risks", meeting.risks)) if meeting_item else meeting.risks,
        "commercial_issues": list(meeting_item.extensions.get("commercial_issues", commercial_issues)) if meeting_item else commercial_issues,
        "recent_changes": list(meeting_item.extensions.get("recent_changes", recent_changes)) if meeting_item else recent_changes,
        "open_loops": list(meeting_item.extensions.get("open_loops", [item.title for item in meeting.open_loops])) if meeting_item else [item.title for item in meeting.open_loops],
        "follow_ups": list(meeting_item.extensions.get("follow_ups", [item.title for item in meeting.follow_ups])) if meeting_item else [item.title for item in meeting.follow_ups],
        "dependencies": list(meeting_item.extensions.get("dependencies", dependencies)) if meeting_item else dependencies,
        "recommended_discussion": list(meeting_item.extensions.get("recommended_discussion", meeting.recommended_discussion)) if meeting_item else meeting.recommended_discussion,
        "recommended_questions": list(meeting_item.extensions.get("recommended_questions", recommended_questions)) if meeting_item else recommended_questions,
        "recommended_decisions": list(meeting_item.extensions.get("recommended_decisions", recommended_decisions)) if meeting_item else recommended_decisions,
        "evidence_references": list(meeting_item.extensions.get("evidence_references", evidence_references)) if meeting_item else evidence_references,
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


def _serialize_followup_item(item: Any, work_item: Any | None) -> dict[str, Any]:
    source_date = _source_date_from_path(item.path)
    buckets = tuple(work_item.extensions.get("buckets", ())) if work_item is not None else ()
    return {
        "work_item_id": work_item.work_item_id if work_item is not None else f"follow_up::{item.path}::{normalise_name(item.summary)}",
        "title": item.summary,
        "source_path": item.path,
        "status": (work_item.status if work_item is not None else None) or "Not defined",
        "priority": item.priority or "Not defined",
        "owner": (work_item.owner if work_item is not None else None) or "Not defined",
        "due_date": item.due_date or "Not defined",
        "source_date": source_date or "No evidence found",
        "recency": source_date or "No evidence found",
        "buckets": [_format_bucket(bucket) for bucket in buckets],
        "classification": _followup_item_classification(item, work_item),
        "confidence": work_item.confidence if work_item is not None else ("MEDIUM" if item.due_date or item.priority == "HIGH" else "LOW"),
        "summary": item.summary,
        "evidence_paths": [item.path],
        "provenance": {key: list(value) for key, value in (work_item.provenance.items() if work_item is not None else {"evidence_paths": (item.path,)}.items())},
    }


def _serialize_open_loop_item(item: Any, work_item: Any | None) -> dict[str, Any]:
    source_date = _source_date_from_path(item.path)
    buckets = tuple(work_item.extensions.get("buckets", ())) if work_item is not None else ()
    return {
        "work_item_id": work_item.work_item_id if work_item is not None else f"open_loop::{item.path}::{normalise_name(item.summary)}",
        "title": item.summary,
        "source_path": item.path,
        "status": item.status or "Not defined",
        "priority": item.priority or "Not defined",
        "owner": item.owner or "Not defined",
        "due_date": "Not defined",
        "source_date": source_date or "No evidence found",
        "recency": source_date or "No evidence found",
        "buckets": [_format_bucket(bucket) for bucket in buckets],
        "classification": _open_loop_item_classification(item, work_item),
        "confidence": work_item.confidence if work_item is not None else ("HIGH" if item.priority in {"CRITICAL", "HIGH"} else "MEDIUM"),
        "summary": item.summary,
        "related_entities": list(work_item.related_entities) if work_item is not None else ([item.title] if item.title else []),
        "evidence_paths": [item.path],
        "provenance": {key: list(value) for key, value in (work_item.provenance.items() if work_item is not None else {"evidence_paths": (item.path,)}.items())},
    }


def _followup_item_sort_key(item: Any) -> tuple[int, str, str]:
    lowered = item.summary.lower()
    if item.due_date and item.due_date < date.today().isoformat():
        rank = 0
    elif item.due_date == date.today().isoformat():
        rank = 1
    elif item.priority == "HIGH":
        rank = 2
    elif item.due_date:
        rank = 3
    elif item.waiting_on_others:
        rank = 4
    else:
        rank = 5
    recency = _source_date_from_path(item.path) or ""
    return (rank, _descending_date_key(recency), item.summary.lower())


def _open_loop_item_sort_key(item: Any) -> tuple[int, str, str]:
    lowered = item.summary.lower()
    if item.priority in {"CRITICAL", "HIGH"}:
        rank = 0
    elif any(marker in lowered for marker in ("awaiting", "waiting", "blocked", "pending")):
        rank = 1
    elif item.owner in {"Unknown", "Not mentioned", "None"}:
        rank = 2
    else:
        rank = 3
    recency = _source_date_from_path(item.path) or ""
    return (rank, _descending_date_key(recency), item.summary.lower())


def _followup_sort_key(item: Any) -> tuple[int, str, str]:
    buckets = set(item.extensions.get("buckets", ()))
    if "overdue" in buckets:
        rank = 0
    elif "due_today" in buckets:
        rank = 1
    elif "high_priority" in buckets:
        rank = 2
    elif "due_this_week" in buckets:
        rank = 3
    elif "waiting_on_others" in buckets:
        rank = 4
    else:
        rank = 5
    recency = _work_item_source_date(item) or ""
    return (rank, _descending_date_key(recency), item.title.lower())


def _open_loop_sort_key(item: Any) -> tuple[int, str, str]:
    buckets = set(item.extensions.get("buckets", ()))
    if "critical_open_loops" in buckets:
        rank = 0
    elif "waiting_for" in buckets:
        rank = 1
    elif "missing_owners" in buckets:
        rank = 2
    elif "stalled_projects" in buckets:
        rank = 3
    else:
        rank = 4
    recency = _work_item_source_date(item) or ""
    return (rank, _descending_date_key(recency), item.title.lower())


def _work_item_source_date(item: Any) -> str | None:
    if item.last_activity:
        return item.last_activity
    if item.created:
        return item.created
    for path in item.evidence_paths:
        matched = re.search(r"(20\d{2}-\d{2}-\d{2})", path)
        if matched:
            return matched.group(1)
    return None


def _source_date_from_path(path: str) -> str | None:
    matched = re.search(r"(20\d{2}-\d{2}-\d{2})", path)
    if matched:
        return matched.group(1)
    return None


def _descending_date_key(value: str) -> str:
    return "".join(chr(255 - ord(char)) for char in value) if value else chr(255) * 10


def _format_bucket(bucket: str) -> str:
    return bucket.replace("_", " ").title()


def _followup_classification(item: Any) -> str:
    buckets = set(item.extensions.get("buckets", ()))
    if "overdue" in buckets:
        return "Overdue"
    if "due_today" in buckets:
        return "Due Today"
    if "high_priority" in buckets:
        return "High Priority"
    if "due_this_week" in buckets:
        return "Due This Week"
    if "waiting_on_others" in buckets:
        return "Waiting On Others"
    return "Current"


def _open_loop_classification(item: Any) -> str:
    buckets = set(item.extensions.get("buckets", ()))
    if "critical_open_loops" in buckets:
        return "Critical"
    if "waiting_for" in buckets:
        return "Waiting For"
    if "missing_owners" in buckets:
        return "Missing Owner"
    if "stalled_projects" in buckets:
        return "Stalled Project"
    return "Current"


def _followup_item_classification(item: Any, work_item: Any | None) -> str:
    if work_item is not None:
        return _followup_classification(work_item)
    if item.due_date and item.due_date < date.today().isoformat():
        return "Overdue"
    if item.due_date == date.today().isoformat():
        return "Due Today"
    if item.priority == "HIGH":
        return "High Priority"
    if item.waiting_on_others:
        return "Waiting On Others"
    return "Current"


def _open_loop_item_classification(item: Any, work_item: Any | None) -> str:
    if work_item is not None:
        return _open_loop_classification(work_item)
    lowered = item.summary.lower()
    if item.priority in {"CRITICAL", "HIGH"}:
        return "Critical"
    if any(marker in lowered for marker in ("awaiting", "waiting", "blocked", "pending")):
        return "Waiting For"
    if item.owner in {"Unknown", "Not mentioned", "None"}:
        return "Missing Owner"
    return "Current"


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
