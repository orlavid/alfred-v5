"""Persistent landing-matter management state for Alfred."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

ROOT = Path(__file__).resolve().parents[2]

MATTER_SCALAR_FIELDS = {
    "owner",
    "status",
    "priority",
    "hold_reason",
    "dismiss_reason",
    "resolution_note",
}

MATTER_LIST_FIELDS = {
    "related_objectives",
    "related_projects",
    "related_people",
    "related_companies",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _default_store() -> dict[str, Any]:
    return {"version": 1, "matters": {}}


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
    explicit = os.environ.get("ALFRED_MATTER_MANAGEMENT_STORE")
    if explicit:
        return Path(explicit).expanduser().resolve()
    return management_data_dir() / "matter_management_state.json"


def load_matter_management_store() -> dict[str, Any]:
    path = management_store_path()
    if not path.exists():
        return _default_store()
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        return _default_store()
    payload.setdefault("version", 1)
    payload.setdefault("matters", {})
    return payload


def save_matter_management_store(store: dict[str, Any]) -> Path:
    path = management_store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(store, indent=2, sort_keys=True))
    return path


def get_matter_record(store: dict[str, Any], matter_id: str) -> dict[str, Any]:
    matters = store.setdefault("matters", {})
    return matters.setdefault(
        matter_id,
        {
            "values": {},
            "management_notes": [],
            "audit_history": [],
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


def update_matter_fields(matter_id: str, changes: dict[str, Any], *, actor: str = "user", reason: str = "") -> dict[str, Any]:
    store = load_matter_management_store()
    record = get_matter_record(store, matter_id)
    values = record.setdefault("values", {})

    for field, new_value in changes.items():
        previous = deepcopy(values.get(field, "__missing__"))
        if field in MATTER_LIST_FIELDS:
            new_value = _normalise_list(new_value)
        if previous == new_value:
            continue
        values[field] = new_value
        _record_audit(record, action="update_field", field=field, previous=previous, new=new_value, actor=actor, reason=reason)

    save_matter_management_store(store)
    return record


def add_management_note(matter_id: str, text: str, *, actor: str = "user", reason: str = "") -> dict[str, Any]:
    store = load_matter_management_store()
    record = get_matter_record(store, matter_id)
    note = {
        "note_id": str(uuid4()),
        "text": text.strip(),
        "timestamp": utc_now(),
        "source": actor,
        "reason": reason or "Management note added.",
    }
    record.setdefault("management_notes", []).append(note)
    _record_audit(record, action="add_management_note", field="management_notes", previous="__append__", new=note, actor=actor, reason=reason)
    save_matter_management_store(store)
    return record


def merge_matter_record(detail: dict[str, Any], record: dict[str, Any] | None) -> dict[str, Any]:
    merged = deepcopy(detail)
    if not record:
        merged.setdefault("management_notes", [])
        merged.setdefault("audit_history", [])
        return merged

    values = record.get("values", {})
    for key in MATTER_SCALAR_FIELDS | MATTER_LIST_FIELDS:
        if key in values:
            merged[key] = deepcopy(values[key])

    merged["management_notes"] = deepcopy(record.get("management_notes", []))
    merged["audit_history"] = list(reversed(deepcopy(record.get("audit_history", []))))
    return merged

