"""Persistent objective management state for Alfred."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

ROOT = Path(__file__).resolve().parents[2]

OBJECTIVE_SCALAR_FIELDS = {
    "owner",
    "current_status",
    "rag_rating",
    "progress_assessment",
    "progress_percentage",
    "priority",
    "start_date",
    "target_date",
    "last_review_date",
    "next_review_date",
}

OBJECTIVE_LIST_FIELDS = {
    "delegates",
    "contributors",
    "success_measures",
    "resources",
    "dependencies",
    "supporting_projects",
        "linked_decisions",
        "open_actions",
        "follow_ups",
        "open_loops",
        "relevant_meetings",
        "related_people",
        "evidence_sources",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _default_store() -> dict[str, Any]:
    return {"version": 1, "objectives": {}}


def management_data_dir() -> Path:
    explicit = os.environ.get("ALFRED_DATA_DIR")
    if explicit:
        return Path(explicit).expanduser().resolve()

    install_root = os.environ.get("ALFRED_INSTALL_ROOT")
    if install_root:
        config_path = Path(install_root).expanduser().resolve() / "config" / "config.yaml"
        if config_path.exists():
            try:
                config = yaml.safe_load(config_path.read_text()) or {}
                configured = config.get("paths", {}).get("data")
                if configured:
                    return Path(configured).expanduser().resolve()
            except Exception:
                pass
        return Path(install_root).expanduser().resolve() / "data"

    return ROOT / "data"


def management_store_path() -> Path:
    explicit = os.environ.get("ALFRED_OBJECTIVE_MANAGEMENT_STORE")
    if explicit:
        return Path(explicit).expanduser().resolve()
    return management_data_dir() / "objective_management_state.json"


def load_objective_management_store() -> dict[str, Any]:
    path = management_store_path()
    if not path.exists():
        return _default_store()
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        return _default_store()
    payload.setdefault("version", 1)
    payload.setdefault("objectives", {})
    return payload


def save_objective_management_store(store: dict[str, Any]) -> Path:
    path = management_store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(store, indent=2, sort_keys=True))
    return path


def get_objective_record(store: dict[str, Any], objective_id: str) -> dict[str, Any]:
    objectives = store.setdefault("objectives", {})
    return objectives.setdefault(
        objective_id,
        {
            "values": {},
            "management_notes": [],
            "milestones": [],
            "audit_history": [],
            "proposals": {},
        },
    )


def _record_audit(record: dict[str, Any], *, action: str, field: str, previous: Any, new: Any, actor: str, reason: str) -> None:
    record.setdefault("audit_history", []).append(
        {
            "audit_id": str(uuid4()),
            "timestamp": utc_now(),
            "action": action,
            "field": field,
            "previous_value": previous,
            "new_value": new,
            "source": actor,
            "reason": reason or "No reason provided.",
        }
    )


def _normalise_list(value: Any) -> list[Any]:
    if value in (None, "", []):
        return []
    if isinstance(value, list):
        return [item for item in value if item not in (None, "")]
    return [value]


def update_objective_fields(
    objective_id: str,
    changes: dict[str, Any],
    *,
    actor: str = "user",
    reason: str = "",
) -> dict[str, Any]:
    store = load_objective_management_store()
    record = get_objective_record(store, objective_id)
    values = record.setdefault("values", {})

    for field, new_value in changes.items():
        previous = deepcopy(values.get(field, "__missing__"))
        if field in OBJECTIVE_LIST_FIELDS:
            new_value = _normalise_list(new_value)
        if previous == new_value:
            continue
        values[field] = new_value
        _record_audit(record, action="update_field", field=field, previous=previous, new=new_value, actor=actor, reason=reason)

    save_objective_management_store(store)
    return record


def add_management_note(objective_id: str, text: str, *, actor: str = "user", reason: str = "") -> dict[str, Any]:
    store = load_objective_management_store()
    record = get_objective_record(store, objective_id)
    note = {
        "note_id": str(uuid4()),
        "text": text.strip(),
        "timestamp": utc_now(),
        "source": actor,
        "reason": reason or "Management note added.",
    }
    record.setdefault("management_notes", []).append(note)
    _record_audit(record, action="add_management_note", field="management_notes", previous="__append__", new=note, actor=actor, reason=reason)
    save_objective_management_store(store)
    return record


def add_milestone(
    objective_id: str,
    *,
    title: str,
    due_date: str | None = None,
    actor: str = "user",
    reason: str = "",
) -> dict[str, Any]:
    store = load_objective_management_store()
    record = get_objective_record(store, objective_id)
    milestone = {
        "milestone_id": str(uuid4()),
        "title": title.strip(),
        "due_date": due_date or "Not defined",
        "status": "OPEN",
        "completed_at": None,
    }
    record.setdefault("milestones", []).append(milestone)
    _record_audit(record, action="add_milestone", field="milestones", previous="__append__", new=milestone, actor=actor, reason=reason)
    save_objective_management_store(store)
    return record


def complete_milestone(objective_id: str, milestone_id: str, *, actor: str = "user", reason: str = "") -> dict[str, Any]:
    store = load_objective_management_store()
    record = get_objective_record(store, objective_id)
    for milestone in record.setdefault("milestones", []):
        if milestone["milestone_id"] != milestone_id:
            continue
        previous = deepcopy(milestone)
        milestone["status"] = "COMPLETED"
        milestone["completed_at"] = utc_now()
        _record_audit(record, action="complete_milestone", field="milestones", previous=previous, new=milestone, actor=actor, reason=reason)
        break
    save_objective_management_store(store)
    return record


def remove_linked_item(
    objective_id: str,
    field: str,
    item_key: str,
    *,
    current_items: list[dict[str, Any]] | None = None,
    actor: str = "user",
    reason: str = "",
) -> dict[str, Any]:
    store = load_objective_management_store()
    record = get_objective_record(store, objective_id)
    values = record.setdefault("values", {})
    previous = deepcopy(values.get(field, []))
    current = _normalise_list(current_items if current_items is not None else values.get(field, []))
    values[field] = [
        item
        for item in current
        if str(item.get("id") if isinstance(item, dict) else item) != item_key
        and str(item.get("work_item_id") if isinstance(item, dict) else item) != item_key
    ]
    if previous != values[field]:
        _record_audit(record, action="unlink_item", field=field, previous=previous, new=values[field], actor=actor, reason=reason)
    save_objective_management_store(store)
    return record


def add_linked_item(
    objective_id: str,
    field: str,
    item: dict[str, Any],
    *,
    current_items: list[dict[str, Any]] | None = None,
    actor: str = "user",
    reason: str = "",
) -> dict[str, Any]:
    store = load_objective_management_store()
    record = get_objective_record(store, objective_id)
    values = record.setdefault("values", {})
    current = _normalise_list(current_items if current_items is not None else values.get(field, []))
    item_key = str(item.get("id") or item.get("work_item_id") or item.get("path") or item.get("title"))
    for existing in current:
        existing_key = str(existing.get("id") or existing.get("work_item_id") or existing.get("path") or existing.get("title"))
        if existing_key == item_key:
            save_objective_management_store(store)
            return record
    previous = deepcopy(current)
    current.append(item)
    values[field] = current
    _record_audit(record, action="link_item", field=field, previous=previous, new=current, actor=actor, reason=reason)
    save_objective_management_store(store)
    return record


def set_objective_status(objective_id: str, status: str, rag_rating: str, *, actor: str = "user", reason: str = "") -> dict[str, Any]:
    return update_objective_fields(
        objective_id,
        {"current_status": status, "rag_rating": rag_rating},
        actor=actor,
        reason=reason or f"Objective moved to {status}.",
    )


def _proposal_fields_from_detail(detail: dict[str, Any]) -> dict[str, Any]:
    proposal_fields: dict[str, Any] = {}
    if detail.get("owner") == "Not defined":
        proposal_fields["owner"] = None
    if detail.get("next_review_date") == "Not defined" and detail.get("last_meaningful_activity") not in {"No evidence found", "Not defined"}:
        try:
            proposal_fields["next_review_date"] = (
                datetime.fromisoformat(detail["last_meaningful_activity"]).date() + timedelta(days=30)
            ).isoformat()
        except Exception:
            proposal_fields["next_review_date"] = (datetime.now(timezone.utc).date() + timedelta(days=30)).isoformat()
    elif detail.get("next_review_date") == "Not defined":
        proposal_fields["next_review_date"] = (datetime.now(timezone.utc).date() + timedelta(days=30)).isoformat()
    if detail.get("current_status") == "Not defined" and detail.get("supporting_projects"):
        proposal_fields["current_status"] = "SUPPORTED"
        proposal_fields["rag_rating"] = "GREEN"
    if not detail.get("success_measures"):
        proposal_fields["success_measures"] = []
    return proposal_fields


def create_smart_proposal(
    objective_id: str,
    detail: dict[str, Any],
    *,
    actor: str = "user",
    reason: str = "",
) -> dict[str, Any]:
    store = load_objective_management_store()
    record = get_objective_record(store, objective_id)
    proposal_id = str(uuid4())
    proposal = {
        "proposal_id": proposal_id,
        "created_at": utc_now(),
        "status": "PENDING",
        "source": actor,
        "reason": reason or "SMART enrichment requested.",
        "summary_lines": list(detail.get("proposed_smart_refinement", [])),
        "field_proposals": _proposal_fields_from_detail(detail),
        "evidence_paths": list(detail.get("provenance", {}).get("objective", [])),
    }
    record.setdefault("proposals", {})["smart_refinement"] = proposal
    _record_audit(record, action="create_smart_proposal", field="proposals.smart_refinement", previous=None, new=proposal, actor=actor, reason=reason)
    save_objective_management_store(store)
    return record


def accept_smart_proposal(
    objective_id: str,
    *,
    selected_fields: list[str] | None = None,
    actor: str = "user",
    reason: str = "",
) -> dict[str, Any]:
    store = load_objective_management_store()
    record = get_objective_record(store, objective_id)
    proposal = record.get("proposals", {}).get("smart_refinement")
    if not proposal:
        return record
    field_proposals = proposal.get("field_proposals", {})
    accepted_fields = set(selected_fields or field_proposals.keys())
    values = record.setdefault("values", {})
    for field, value in field_proposals.items():
        if field not in accepted_fields:
            continue
        previous = deepcopy(values.get(field, "__missing__"))
        values[field] = value
        _record_audit(record, action="accept_smart_proposal_field", field=field, previous=previous, new=value, actor=actor, reason=reason)
    proposal["status"] = "ACCEPTED"
    proposal["accepted_fields"] = sorted(accepted_fields)
    _record_audit(record, action="accept_smart_proposal", field="proposals.smart_refinement", previous="PENDING", new="ACCEPTED", actor=actor, reason=reason)
    save_objective_management_store(store)
    return record


def reject_smart_proposal(objective_id: str, *, actor: str = "user", reason: str = "") -> dict[str, Any]:
    store = load_objective_management_store()
    record = get_objective_record(store, objective_id)
    proposal = record.get("proposals", {}).get("smart_refinement")
    if not proposal:
        return record
    proposal["status"] = "REJECTED"
    _record_audit(record, action="reject_smart_proposal", field="proposals.smart_refinement", previous="PENDING", new="REJECTED", actor=actor, reason=reason)
    save_objective_management_store(store)
    return record


def merge_objective_detail(detail: dict[str, Any], record: dict[str, Any] | None) -> dict[str, Any]:
    merged = deepcopy(detail)
    if not record:
        merged["contributors"] = []
        merged["priority"] = "Not defined"
        merged["progress_percentage"] = None
        merged["success_measures"] = []
        merged["milestones"] = []
        merged["resources"] = []
        merged["management_notes"] = []
        merged["audit_history"] = []
        merged["smart_enrichment_proposal"] = None
        return merged

    values = record.get("values", {})
    scalar_map = {
        "owner": "owner",
        "current_status": "current_status",
        "rag_rating": "rag_rating",
        "progress_assessment": "progress_assessment",
        "start_date": "start_date",
        "target_date": "target_date",
        "last_review_date": "last_review_date",
        "next_review_date": "next_review_date",
        "priority": "priority",
    }
    for detail_key, record_key in scalar_map.items():
        if record_key in values:
            merged[detail_key] = values[record_key] if values[record_key] not in (None, "") else "Not defined"

    if "progress_percentage" in values:
        merged["progress_percentage"] = values["progress_percentage"]
    else:
        merged["progress_percentage"] = None

    list_map = {
        "delegates": "delegates",
        "contributors": "contributors",
        "supporting_projects": "supporting_projects",
        "linked_decisions": "linked_decisions",
        "open_actions": "open_actions",
        "follow_ups": "follow_ups",
        "open_loops": "open_loops",
        "relevant_meetings": "relevant_meetings",
        "related_people": "related_people",
        "evidence_sources": "evidence_sources",
        "success_measures": "success_measures",
        "resources": "resources",
        "dependencies": "dependencies",
    }
    for detail_key, record_key in list_map.items():
        if record_key in values:
            merged[detail_key] = deepcopy(values[record_key])

    merged["milestones"] = deepcopy(record.get("milestones", []))
    merged["management_notes"] = deepcopy(record.get("management_notes", []))
    merged["audit_history"] = list(reversed(deepcopy(record.get("audit_history", []))))
    merged["smart_enrichment_proposal"] = deepcopy(record.get("proposals", {}).get("smart_refinement"))
    if "current_status" in values:
        merged["health"] = merged["rag_rating"]
    merged["next_checkpoint_or_deadline"] = merged.get("target_date") if merged.get("target_date") not in {None, "", "Not defined"} else merged.get("next_review_date", "Not defined")
    return merged
