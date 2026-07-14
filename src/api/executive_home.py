"""Canonical executive home payload for Alfred."""

from __future__ import annotations

from copy import deepcopy
from datetime import date
import hashlib
import re
from typing import Any

from src.executive.executive_state import ExecutiveState
from src.executive.read_model import UnifiedExecutiveReadModel
from src.management.matters import load_matter_management_store, merge_matter_record

TECHNICAL_LANGUAGE_PATTERNS = (
    "graph linkage",
    "canonical",
    "extraction pipeline",
    "semantic equivalence",
    "markdown filename",
    "internal confidence",
)
RAW_FILENAME_PATTERNS = (
    ".md",
    "open loop register",
    "watchlist",
    "strategic memory synthesis",
    "entity graph",
)
RECENT_WINDOW_DAYS = 7


def build_executive_home_payload(
    state: ExecutiveState,
    *,
    read_model: UnifiedExecutiveReadModel,
    objectives_page: dict[str, Any],
    projects_page: dict[str, Any],
    decisions_page: dict[str, Any],
    followups_page: dict[str, Any],
    open_loops_page: dict[str, Any],
    meetings_page: dict[str, Any],
    admin_configuration_page: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    matter_store = load_matter_management_store()
    technical_alerts: list[dict[str, Any]] = []
    matter_details: dict[str, dict[str, Any]] = {}
    candidate_sections: dict[str, list[dict[str, Any]]] = {
        "decisions_required": [],
        "meetings_to_prepare": [],
        "objectives_projects_at_risk": [],
        "waiting_blocked": [],
        "recently_changed": [],
    }

    for item in decisions_page.get("items", []):
        detail = decisions_page.get("details", {}).get(item["decision_id"])
        if not detail:
            continue
        matter = _build_decision_matter(item, detail, state)
        if _is_executive_noise(matter):
            technical_alerts.append(_technical_alert(matter, "Decision rejected because it reads as system language rather than business action."))
            continue
        matter = merge_matter_record(matter, matter_store.get("matters", {}).get(matter["matter_id"]))
        if not _is_active_matter(matter):
            continue
        matter_details[matter["matter_id"]] = matter
        candidate_sections["decisions_required"].append(matter)
        if _is_recent(matter):
            candidate_sections["recently_changed"].append(matter)

    for item in objectives_page.get("items", []):
        detail = objectives_page.get("details", {}).get(item["objective_id"])
        if not detail:
            continue
        matter = _build_objective_matter(item, detail)
        if not _is_at_risk_matter(matter):
            continue
        if _is_executive_noise(matter):
            technical_alerts.append(_technical_alert(matter, "Objective rejected because the title or explanation is technical noise."))
            continue
        matter_details[matter["matter_id"]] = matter
        candidate_sections["objectives_projects_at_risk"].append(matter)
        if _is_recent(matter):
            candidate_sections["recently_changed"].append(matter)

    for item in projects_page.get("items", []):
        detail = projects_page.get("details", {}).get(item["project_id"])
        if not detail:
            continue
        matter = _build_project_matter(item, detail)
        if _is_non_executive_project(matter):
            technical_alerts.append(_technical_alert(matter, "Project rejected because the source reads as personal or scratch-note material rather than an executive programme matter."))
            continue
        if _is_closed_or_superseded(matter):
            continue
        if not _is_at_risk_matter(matter):
            continue
        if _is_executive_noise(matter):
            technical_alerts.append(_technical_alert(matter, "Project rejected because it reads as technical or archival noise."))
            continue
        matter_details[matter["matter_id"]] = matter
        candidate_sections["objectives_projects_at_risk"].append(matter)
        if _is_recent(matter):
            candidate_sections["recently_changed"].append(matter)

    for item in followups_page.get("items", []):
        matter = _build_followup_matter(item, read_model)
        matter = merge_matter_record(matter, matter_store.get("matters", {}).get(matter["matter_id"]))
        if not _is_active_matter(matter):
            continue
        matter_details[matter["matter_id"]] = matter
        if item["classification"] in {"Overdue", "Due Today", "High Priority", "Waiting On Others"}:
            candidate_sections["waiting_blocked"].append(matter)
        if _is_recent(matter):
            candidate_sections["recently_changed"].append(matter)

    for item in open_loops_page.get("items", []):
        matter = _build_open_loop_matter(item, read_model)
        if _is_executive_noise(matter):
            technical_alerts.append(_technical_alert(matter, "Open loop rejected because it is an internal/system signal rather than an executive matter."))
            continue
        matter = merge_matter_record(matter, matter_store.get("matters", {}).get(matter["matter_id"]))
        if not _is_active_matter(matter):
            continue
        matter_details[matter["matter_id"]] = matter
        candidate_sections["waiting_blocked"].append(matter)
        if _is_recent(matter):
            candidate_sections["recently_changed"].append(matter)

    meeting_matter = _build_meeting_matter(meetings_page, read_model)
    if meeting_matter is not None:
        meeting_matter = merge_matter_record(meeting_matter, matter_store.get("matters", {}).get(meeting_matter["matter_id"]))
        if _is_active_matter(meeting_matter):
            matter_details[meeting_matter["matter_id"]] = meeting_matter
            candidate_sections["meetings_to_prepare"].append(meeting_matter)
            if _is_recent(meeting_matter):
                candidate_sections["recently_changed"].append(meeting_matter)

    for section_id, matters in candidate_sections.items():
        candidate_sections[section_id] = _sort_matters(_dedupe_matters(matters))

    requires_attention = _sort_matters(
        _dedupe_matters(
            candidate_sections["decisions_required"][:2]
            + candidate_sections["meetings_to_prepare"][:1]
            + candidate_sections["objectives_projects_at_risk"][:2]
            + candidate_sections["waiting_blocked"][:3]
        )
    )[:6]

    used: set[str] = set()
    ordered_sections = []
    for section_id, title, summary, matters in (
        ("requires_attention", "Requires Your Attention", "The matters that currently deserve direct executive time.", requires_attention),
        ("decisions_required", "Decisions Required", "Decisions or unresolved decision gaps that need an owner, call, or explicit outcome.", candidate_sections["decisions_required"]),
        ("meetings_to_prepare", "Meetings to Prepare", "Meetings where Alfred can already explain the purpose, context, and the next conversation to have.", candidate_sections["meetings_to_prepare"]),
        ("objectives_projects_at_risk", "Objectives / Projects At Risk", "Current delivery or governance items whose health, ownership, or checkpoint is weak enough to need intervention.", candidate_sections["objectives_projects_at_risk"]),
        ("waiting_blocked", "Waiting / Blocked", "Follow-ups and open matters that are stalled on ownership, response, or an overdue next step.", candidate_sections["waiting_blocked"]),
        ("recently_changed", "Recently Changed", "Fresh evidence from the last week that may change the executive picture.", candidate_sections["recently_changed"]),
    ):
        section_matters = _exclude_used(matters, used)
        used.update(matter["matter_id"] for matter in section_matters)
        ordered_sections.append(_build_section(section_id, title, section_matters, summary))
    sections = [section for section in ordered_sections if section["matters"]]

    executive_home = {
        "headline": "Executive engagement surface",
        "summary_lines": [
            f"{len(requires_attention)} matters currently need attention.",
            "Every matter shown below is evidence-backed, de-duplicated, and linked to a direct workflow.",
        ],
        "kpis": [
            {
                "card_id": "attention",
                "label": "Requires Your Attention",
                "summary": _kpi_summary(requires_attention, "No current executive matter has crossed the attention threshold."),
                "count": len(requires_attention),
                "route": "/",
            },
            {
                "card_id": "decisions",
                "label": "Decisions Required",
                "summary": _kpi_summary(candidate_sections["decisions_required"], "No decision requires executive intervention."),
                "count": len(candidate_sections["decisions_required"]),
                "route": "/decisions",
            },
            {
                "card_id": "meetings",
                "label": "Meetings to Prepare",
                "summary": _kpi_summary(candidate_sections["meetings_to_prepare"], "No current meeting requires preparation."),
                "count": len(candidate_sections["meetings_to_prepare"]),
                "route": "/meetings",
            },
            {
                "card_id": "delivery",
                "label": "Objectives / Projects At Risk",
                "summary": _kpi_summary(candidate_sections["objectives_projects_at_risk"], "No objective or project is currently classed at risk."),
                "count": len(candidate_sections["objectives_projects_at_risk"]),
                "route": "/projects",
            },
            {
                "card_id": "waiting",
                "label": "Waiting / Blocked",
                "summary": _kpi_summary(candidate_sections["waiting_blocked"], "No current blocker needs executive attention."),
                "count": len(candidate_sections["waiting_blocked"]),
                "route": "/open-loops",
            },
            {
                "card_id": "changed",
                "label": "Recently Changed",
                "summary": _kpi_summary(candidate_sections["recently_changed"], "No recent change has materially altered the executive picture."),
                "count": len(candidate_sections["recently_changed"]),
                "route": "/daily-brief",
            },
        ],
        "sections": sections,
        "system_health_route": "/system-health",
    }

    matters_page = {
        "counts": {
            "total": len(matter_details),
            "requires_attention": len(requires_attention),
            "decisions_required": len(candidate_sections["decisions_required"]),
            "meetings_to_prepare": len(candidate_sections["meetings_to_prepare"]),
            "objectives_projects_at_risk": len(candidate_sections["objectives_projects_at_risk"]),
            "waiting_blocked": len(candidate_sections["waiting_blocked"]),
            "recently_changed": len(candidate_sections["recently_changed"]),
        },
        "sections": sections,
        "summary": executive_home["summary_lines"],
    }
    system_health_page = {
        "summary": admin_configuration_page["overview"]["summary_lines"],
        "data_quality_alerts": technical_alerts,
        "refresh_status": {
            "overall_health": admin_configuration_page["overview"]["overall_health"],
            "environment_score": admin_configuration_page["overview"]["environment_score"],
        },
    }
    return executive_home, matters_page, matter_details | {"__system_health__": system_health_page}


def build_system_health_from_matter_details(matter_details: dict[str, Any]) -> dict[str, Any]:
    return matter_details.get("__system_health__", {"summary": [], "data_quality_alerts": [], "refresh_status": {}})


def _build_section(section_id: str, title: str, matters: list[dict[str, Any]], summary: str) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "title": title,
        "summary": summary,
        "matters": matters,
    }


def _exclude_used(matters: list[dict[str, Any]], used: set[str]) -> list[dict[str, Any]]:
    return [matter for matter in matters if matter["matter_id"] not in used][:8]


def _kpi_summary(matters: list[dict[str, Any]], fallback: str) -> str:
    if not matters:
        return fallback
    matter = matters[0]
    return f"{matter['business_title']}: {matter['why_now']}"


def _build_objective_matter(item: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    matter_id = _stable_matter_id(f"objective::{item['objective_id']}")
    return {
        "matter_id": matter_id,
        "matter_category": "objective",
        "business_title": detail["title"],
        "human_summary": detail["executive_definition"],
        "why_it_matters": detail["key_risk_or_blocker"] if detail["key_risk_or_blocker"] != "No evidence found" else detail["recommended_next_action"],
        "why_now": _why_now_from_dates(detail["next_checkpoint_or_deadline"], detail["last_meaningful_activity"], detail["current_status"]),
        "status": detail["current_status"],
        "priority": detail["priority"],
        "urgency": detail["rag_rating"],
        "owner": detail["owner"],
        "related": _related_map(
            objective=detail["title"],
            projects=[item["title"] for item in detail.get("supporting_projects", [])],
            people=[item["title"] for item in detail.get("related_people", [])],
            companies=[],
        ),
        "evidence_summary": _objective_evidence_summary(detail),
        "confidence": detail["evidence_confidence"],
        "recommended_next_step": detail["recommended_next_action"],
        "available_actions": [
            {"action": "open_detail", "label": "Open detail"},
            {"action": "assign_owner", "label": "Assign owner"},
            {"action": "change_priority", "label": "Change priority"},
            {"action": "hold", "label": "Hold"},
            {"action": "resolve", "label": "Resolve"},
        ],
        "route": f"/matters/{matter_id}",
        "authoritative_route": detail["route"],
        "source_path": detail["source_path"],
        "evidence_paths": [source["path"] for source in detail.get("evidence_sources", []) if source.get("path")],
        "provenance": detail.get("provenance", {}),
        "source_kind": "objective",
        "source_record_id": item["objective_id"],
        "action_target": {"kind": "objective", "id": item["objective_id"]},
        "detail_backlink_label": "Open objective workspace",
        "recent_activity": detail["last_meaningful_activity"],
        "audit_history": detail.get("audit_history", []),
        "management_notes": detail.get("management_notes", []),
        "missing_information": detail.get("missing_information", []),
    }


def _build_project_matter(item: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    matter_id = _stable_matter_id(f"project::{item['project_id']}")
    return {
        "matter_id": matter_id,
        "matter_category": "project",
        "business_title": detail["title"],
        "human_summary": detail["executive_definition"],
        "why_it_matters": detail["key_risk_or_blocker"] if detail.get("key_risk_or_blocker") and detail["key_risk_or_blocker"] != "No evidence found" else detail["recommended_next_action"],
        "why_now": _why_now_from_dates(detail["next_checkpoint_or_deadline"], detail["last_meaningful_activity"], detail["current_status"]),
        "status": detail["current_status"],
        "priority": detail["priority"],
        "urgency": detail["rag_rating"],
        "owner": detail["owner"],
        "related": _related_map(
            objective="",
            projects=[detail["title"]],
            people=[item["title"] for item in detail.get("related_people", [])],
            companies=[item["title"] for item in detail.get("related_companies", [])],
        ),
        "evidence_summary": _project_evidence_summary(detail),
        "confidence": detail["evidence_confidence"],
        "recommended_next_step": detail["recommended_next_action"],
        "available_actions": [
            {"action": "open_detail", "label": "Open detail"},
            {"action": "assign_owner", "label": "Assign owner"},
            {"action": "change_priority", "label": "Change priority"},
            {"action": "hold", "label": "Hold"},
            {"action": "resolve", "label": "Resolve"},
        ],
        "route": f"/matters/{matter_id}",
        "authoritative_route": detail["route"],
        "source_path": detail["source_path"],
        "evidence_paths": [source["path"] for source in detail.get("evidence_sources", []) if source.get("path")],
        "provenance": detail.get("provenance", {}),
        "source_kind": "project",
        "source_record_id": item["project_id"],
        "action_target": {"kind": "project", "id": item["project_id"]},
        "detail_backlink_label": "Open project workspace",
        "recent_activity": detail["last_meaningful_activity"],
        "audit_history": detail.get("audit_history", []),
        "management_notes": detail.get("management_notes", []),
        "missing_information": detail.get("missing_information", []),
    }


def _build_decision_matter(item: dict[str, Any], detail: dict[str, Any], state: ExecutiveState) -> dict[str, Any]:
    matter_id = _stable_matter_id(f"decision::{item['decision_id']}")
    related_companies = [entry["title"] for entry in detail.get("related_companies", [])]
    if not related_companies and state.suppliers:
        related_companies = [supplier.title for supplier in state.suppliers[:1]]
    business_title = _decision_business_title(detail)
    return {
        "matter_id": matter_id,
        "matter_category": "decision",
        "business_title": business_title,
        "human_summary": detail["rationale"],
        "why_it_matters": _decision_impact_summary(detail),
        "why_now": _why_now_from_dates(detail["decision_date"], detail["decision_date"], detail["current_status"]),
        "status": detail["current_status"],
        "priority": _decision_priority(detail["importance"]),
        "urgency": _decision_priority(detail["importance"]),
        "owner": detail["owner"],
        "related": _related_map(
            objective="",
            projects=[entry["title"] for entry in detail.get("related_projects", [])],
            people=[entry["title"] for entry in detail.get("related_people", [])],
            companies=related_companies,
        ),
        "evidence_summary": f"Recorded in the decision note '{detail['title']}'. The source rationale says: {detail['rationale']}",
        "confidence": detail["evidence_confidence"],
        "recommended_next_step": _decision_next_step(detail),
        "available_actions": [
            {"action": "open_detail", "label": "Open detail"},
            {"action": "assign_owner", "label": "Assign owner"},
            {"action": "change_priority", "label": "Change priority"},
            {"action": "hold", "label": "Hold"},
            {"action": "resolve", "label": "Resolve"},
            {"action": "dismiss", "label": "Dismiss"},
        ],
        "route": f"/matters/{matter_id}",
        "authoritative_route": detail["route"],
        "source_path": detail["source_path"],
        "evidence_paths": [source["path"] for source in detail.get("evidence_sources", []) if source.get("path")],
        "provenance": detail.get("provenance", {}),
        "source_kind": "decision",
        "source_record_id": item["decision_id"],
        "action_target": {"kind": "matter", "id": matter_id},
        "detail_backlink_label": "Open decision register",
        "recent_activity": detail["decision_date"],
        "audit_history": [],
        "management_notes": [],
        "missing_information": detail.get("missing_information", []),
    }


def _build_followup_matter(item: dict[str, Any], read_model: UnifiedExecutiveReadModel) -> dict[str, Any]:
    matter_id = _stable_matter_id(f"followup::{item['work_item_id']}")
    related = _related_from_work_item(read_model, item["work_item_id"])
    return {
        "matter_id": matter_id,
        "matter_category": "follow_up",
        "business_title": item["title"],
        "human_summary": item["summary"],
        "why_it_matters": _followup_importance(item),
        "why_now": _followup_why_now(item),
        "status": item["status"],
        "priority": item["priority"],
        "urgency": item["classification"],
        "owner": item["owner"],
        "related": related,
        "evidence_summary": _followup_evidence_summary(item),
        "confidence": item["confidence"],
        "recommended_next_step": _followup_next_step(item),
        "available_actions": [
            {"action": "open_detail", "label": "Open detail"},
            {"action": "assign_owner", "label": "Assign owner"},
            {"action": "change_priority", "label": "Change priority"},
            {"action": "hold", "label": "Hold"},
            {"action": "resolve", "label": "Resolve"},
            {"action": "dismiss", "label": "Dismiss"},
        ],
        "route": f"/matters/{matter_id}",
        "authoritative_route": "/follow-ups",
        "source_path": item["source_path"],
        "evidence_paths": item["evidence_paths"],
        "provenance": item["provenance"],
        "source_kind": "follow_up",
        "source_record_id": item["work_item_id"],
        "action_target": {"kind": "matter", "id": matter_id},
        "detail_backlink_label": "Open follow-up register",
        "recent_activity": item["source_date"],
        "audit_history": [],
        "management_notes": [],
        "missing_information": [],
    }


def _build_open_loop_matter(item: dict[str, Any], read_model: UnifiedExecutiveReadModel) -> dict[str, Any]:
    matter_id = _stable_matter_id(f"open_loop::{item['work_item_id']}")
    related = _related_from_work_item(read_model, item["work_item_id"])
    return {
        "matter_id": matter_id,
        "matter_category": "open_loop",
        "business_title": item["title"],
        "human_summary": item["summary"],
        "why_it_matters": _open_loop_importance(item),
        "why_now": _open_loop_why_now(item),
        "status": item["status"],
        "priority": item["priority"],
        "urgency": item["classification"],
        "owner": item["owner"],
        "related": related,
        "evidence_summary": _open_loop_evidence_summary(item),
        "confidence": item["confidence"],
        "recommended_next_step": _open_loop_next_step(item),
        "available_actions": [
            {"action": "open_detail", "label": "Open detail"},
            {"action": "assign_owner", "label": "Assign owner"},
            {"action": "change_priority", "label": "Change priority"},
            {"action": "hold", "label": "Hold"},
            {"action": "resolve", "label": "Resolve"},
            {"action": "dismiss", "label": "Dismiss"},
        ],
        "route": f"/matters/{matter_id}",
        "authoritative_route": "/open-loops",
        "source_path": item["source_path"],
        "evidence_paths": item["evidence_paths"],
        "provenance": item["provenance"],
        "source_kind": "open_loop",
        "source_record_id": item["work_item_id"],
        "action_target": {"kind": "matter", "id": matter_id},
        "detail_backlink_label": "Open open-loop register",
        "recent_activity": item["source_date"],
        "audit_history": [],
        "management_notes": [],
        "missing_information": [],
    }


def _build_meeting_matter(meetings_page: dict[str, Any], read_model: UnifiedExecutiveReadModel) -> dict[str, Any] | None:
    subject = meetings_page.get("subject", "")
    if subject in {"", "No active meeting identified."}:
        return None
    if not meetings_page.get("recommended_discussion") and not meetings_page.get("recommended_questions") and not meetings_page.get("recommended_decisions"):
        return None
    matter_id = _stable_matter_id(f"meeting::{subject}")
    return {
        "matter_id": matter_id,
        "matter_category": "meeting",
        "business_title": subject,
        "human_summary": meetings_page["executive_summary"][0] if meetings_page.get("executive_summary") else "Meeting context available from linked evidence.",
        "why_it_matters": meetings_page["recommended_discussion"][0] if meetings_page.get("recommended_discussion") else "This meeting has linked evidence, dependencies, or open actions that merit preparation.",
        "why_now": meetings_page["recent_changes"][0] if meetings_page.get("recent_changes") else "The meeting is active in the current executive picture and should be prepared before the next interaction.",
        "status": "PREPARE",
        "priority": "HIGH" if meetings_page.get("risks") or meetings_page.get("recommended_decisions") else "MEDIUM",
        "urgency": "MEETING",
        "owner": "Unassigned",
        "related": _related_map(
            objective="",
            projects=meetings_page.get("related_projects", []),
            people=meetings_page.get("related_people", []),
            companies=meetings_page.get("related_companies", []),
        ),
        "evidence_summary": _meeting_evidence_summary(meetings_page),
        "confidence": meetings_page.get("confidence", "LOW"),
        "recommended_next_step": meetings_page["recommended_questions"][0] if meetings_page.get("recommended_questions") else meetings_page["recommended_discussion"][0],
        "available_actions": [
            {"action": "open_detail", "label": "Open detail"},
            {"action": "hold", "label": "Hold"},
            {"action": "dismiss", "label": "Dismiss"},
        ],
        "route": f"/matters/{matter_id}",
        "authoritative_route": "/meetings",
        "source_path": meetings_page.get("evidence_references", [""])[0] if meetings_page.get("evidence_references") else "",
        "evidence_paths": list(_meeting_evidence_paths(read_model, subject)),
        "provenance": {"meeting": list(_meeting_evidence_paths(read_model, subject))},
        "source_kind": "meeting",
        "source_record_id": subject,
        "action_target": {"kind": "matter", "id": matter_id},
        "detail_backlink_label": "Open meetings page",
        "recent_activity": meetings_page.get("recent_changes", [""])[0] if meetings_page.get("recent_changes") else "",
        "audit_history": [],
        "management_notes": [],
        "missing_information": [],
    }


def _meeting_evidence_paths(read_model: UnifiedExecutiveReadModel, subject: str) -> tuple[str, ...]:
    for meeting in read_model.meetings:
        if meeting.subject == subject:
            return tuple(match.path for match in meeting.matched_entities[:8])
    return ()


def _related_from_work_item(read_model: UnifiedExecutiveReadModel, work_item_id: str) -> dict[str, list[str]]:
    for item in read_model.work_items:
        if item.work_item_id != work_item_id:
            continue
        companies = sorted(
            {
                entity.canonical_name
                for entity in read_model.entities
                if entity.entity_type == "company" and set(entity.evidence_paths) & set(item.evidence_paths)
            }
        )
        return _related_map(
            objective=item.related_objectives[0] if item.related_objectives else "",
            projects=list(item.related_projects),
            people=list(item.related_people),
            companies=companies,
        )
    return _related_map(objective="", projects=[], people=[], companies=[])


def _related_map(*, objective: str, projects: list[str], people: list[str], companies: list[str]) -> dict[str, list[str] | str]:
    return {
        "objective": objective or "",
        "projects": _dedupe_nonempty(projects),
        "people": _dedupe_nonempty(people),
        "companies": _dedupe_nonempty(companies),
    }


def _objective_evidence_summary(detail: dict[str, Any]) -> str:
    if detail.get("executive_definition") and detail["executive_definition"] != "No evidence found.":
        return f"The objective definition says: {detail['executive_definition']}"
    return "The objective is being tracked from the executive objective register, but its practical definition is still weak."


def _project_evidence_summary(detail: dict[str, Any]) -> str:
    return f"The project note for '{detail['title']}' is currently classified as {detail['current_status']} with recommendation: {detail['recommended_next_action']}"


def _decision_impact_summary(detail: dict[str, Any]) -> str:
    if detail.get("related_projects"):
        return f"This decision affects {len(detail['related_projects'])} linked project(s)."
    if detail.get("related_objectives"):
        return f"This decision affects {len(detail['related_objectives'])} linked objective(s)."
    return "This decision remains part of the active executive record and still needs explicit treatment."


def _decision_business_title(detail: dict[str, Any]) -> str:
    title = str(detail.get("title", "")).strip()
    rationale = str(detail.get("rationale", "")).strip()
    lowered = title.lower()
    if lowered.startswith(("capture -", "decision -")) and rationale and not rationale.startswith("["):
        sentence = rationale.split(".")[0].strip().rstrip(".")
        if sentence:
            return sentence[0].upper() + sentence[1:]
    return title


def _decision_next_step(detail: dict[str, Any]) -> str:
    if detail["owner"] == "Not defined":
        return "Assign an accountable owner and confirm the required decision outcome."
    if detail["current_status"] in {"Not defined", "OPEN"}:
        return "Confirm whether the decision has been made and record the current status."
    return "Review the linked work and confirm the decision still matches current execution."


def _followup_importance(item: dict[str, Any]) -> str:
    if item["classification"] == "Overdue":
        return "This follow-up is overdue and has not been closed in the live evidence."
    if item["classification"] == "Due Today":
        return "This follow-up is due today and still active."
    if item["classification"] == "Waiting On Others":
        return "This follow-up is waiting on an external response and may need escalation."
    return "This follow-up is still current and evidence-backed."


def _followup_why_now(item: dict[str, Any]) -> str:
    if item["due_date"] != "Not defined":
        return f"It is dated for {item['due_date']}."
    if item["source_date"] != "No evidence found":
        return f"It was surfaced from current evidence dated {item['source_date']}."
    return "It remains in the current follow-up register."


def _followup_evidence_summary(item: dict[str, Any]) -> str:
    if item["source_date"] != "No evidence found":
        return f"This follow-up was identified from evidence dated {item['source_date']}. The source records: {item['summary']}"
    return f"The follow-up register still records: {item['summary']}"


def _followup_next_step(item: dict[str, Any]) -> str:
    if item["owner"] == "Not defined":
        return "Assign an owner and confirm the next dated step."
    if item["classification"] == "Waiting On Others":
        return "Confirm whether escalation or a dated chase is now required."
    return "Update the next action and close it if the work is complete."


def _open_loop_importance(item: dict[str, Any]) -> str:
    if item["classification"] == "Critical":
        return "This unresolved matter is currently classed as critical."
    if item["classification"] == "Missing Owner":
        return "This unresolved matter still has no accountable owner."
    if item["classification"] == "Waiting For":
        return "This unresolved matter is blocked on an external dependency."
    return "This matter is still unresolved in the live open-loop evidence."


def _open_loop_why_now(item: dict[str, Any]) -> str:
    if item["source_date"] != "No evidence found":
        return f"Latest source evidence is dated {item['source_date']}."
    return "It remains open in the current register."


def _open_loop_evidence_summary(item: dict[str, Any]) -> str:
    return f"The live open-loop evidence still records: {item['summary']}"


def _open_loop_next_step(item: dict[str, Any]) -> str:
    if item["owner"] == "Not defined":
        return "Assign an owner and define the next accountable step."
    if item["classification"] == "Waiting For":
        return "Confirm who is being waited on and whether escalation is now required."
    return "Review the blocker, update its current state, and close it if resolved."


def _meeting_evidence_summary(meetings_page: dict[str, Any]) -> str:
    if meetings_page.get("meeting_purpose"):
        return f"Meeting purpose: {meetings_page['meeting_purpose'][0]}"
    if meetings_page.get("executive_summary"):
        return meetings_page["executive_summary"][0]
    return "This meeting has linked executive context and should be prepared from the current evidence."


def _decision_priority(importance: int) -> str:
    if importance >= 120:
        return "HIGH"
    if importance >= 60:
        return "MEDIUM"
    return "LOW"


def _why_now_from_dates(next_checkpoint: str, recent_activity: str, status: str) -> str:
    if next_checkpoint not in {None, "", "Not defined"}:
        return f"The next checkpoint is {next_checkpoint}."
    if recent_activity not in {None, "", "No evidence found"}:
        return f"Latest meaningful activity is dated {recent_activity}."
    return f"It is still classified as {status}."


def _is_recent(matter: dict[str, Any]) -> bool:
    token = _extract_date(matter.get("recent_activity") or matter.get("source_path") or "")
    if not token:
        return False
    return (date.today() - date.fromisoformat(token)).days <= RECENT_WINDOW_DAYS


def _is_at_risk_matter(matter: dict[str, Any]) -> bool:
    return any(
        token in str(matter.get("status", "")).upper() or token in str(matter.get("urgency", "")).upper()
        for token in ("AT RISK", "WATCH", "RED", "AMBER")
    )


def _is_closed_or_superseded(matter: dict[str, Any]) -> bool:
    text = " ".join(
        str(matter.get(key, ""))
        for key in ("business_title", "status", "human_summary", "why_it_matters", "recommended_next_step")
    ).lower()
    return any(token in text for token in ("closed", "complete", "completed", "superseded", "archived"))


def _is_non_executive_project(matter: dict[str, Any]) -> bool:
    if matter.get("matter_category") != "project":
        return False
    text = " ".join(
        str(matter.get(key, ""))
        for key in ("business_title", "human_summary", "source_path", "evidence_summary")
    ).lower()
    return any(token in text for token in ("personal-notes", "personal notes", "scratch note", "scratch-note"))


def _is_active_matter(matter: dict[str, Any]) -> bool:
    status = str(matter.get("status", "")).upper()
    return status not in {"DISMISSED", "RESOLVED", "CLOSED", "HOLD"}


def _is_executive_noise(matter: dict[str, Any]) -> bool:
    text = " ".join(
        str(matter.get(key, ""))
        for key in ("business_title", "human_summary", "why_it_matters", "why_now", "evidence_summary")
    ).lower()
    if any(pattern in text for pattern in TECHNICAL_LANGUAGE_PATTERNS):
        return True
    if any(pattern in matter.get("business_title", "").lower() for pattern in RAW_FILENAME_PATTERNS):
        return True
    if re.fullmatch(r"[0-9a-f-]{8,}", matter.get("business_title", "").lower()):
        return True
    return False


def _technical_alert(matter: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "title": matter["business_title"],
        "summary": reason,
        "source_path": matter.get("source_path", ""),
        "route": matter.get("authoritative_route") or matter.get("route") or "/admin",
    }


def _sort_matters(matters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        matters,
        key=lambda matter: (
            _matter_rank(matter),
            _descending_date_key(_extract_date(matter.get("recent_activity") or matter.get("source_path") or "") or ""),
            matter["business_title"].lower(),
        ),
    )


def _matter_rank(matter: dict[str, Any]) -> int:
    priority = str(matter.get("priority", "")).upper()
    urgency = str(matter.get("urgency", "")).upper()
    status = str(matter.get("status", "")).upper()
    if priority == "HIGH" or urgency in {"CRITICAL", "OVERDUE", "DUE TODAY", "RED"}:
        return 0
    if "AT RISK" in status or urgency in {"AMBER", "WAITING FOR", "MISSING OWNER"}:
        return 1
    if priority == "MEDIUM":
        return 2
    return 3


def _dedupe_matters(matters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for matter in matters:
        if matter["matter_id"] in seen:
            continue
        seen.add(matter["matter_id"])
        deduped.append(matter)
    return deduped


def _stable_matter_id(seed: str) -> str:
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]


def _extract_date(value: str) -> str | None:
    matched = re.search(r"(20\d{2}-\d{2}-\d{2})", value)
    return matched.group(1) if matched else None


def _descending_date_key(value: str) -> str:
    return "".join(chr(255 - ord(char)) for char in value) if value else chr(255) * 10


def _dedupe_nonempty(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped
