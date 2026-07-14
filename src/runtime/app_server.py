"""Alfred application server with static UI hosting and management APIs."""

from __future__ import annotations

from functools import partial
import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import re
import threading
import time
from typing import Any
from urllib.parse import urlparse

from src.management.objectives import (
    accept_smart_proposal,
    add_linked_item,
    add_management_note,
    add_milestone,
    create_smart_proposal,
    reject_smart_proposal,
    remove_linked_item,
    set_objective_status,
    update_objective_fields,
)
from src.management.matters import (
    add_management_note as add_matter_management_note,
    update_matter_fields,
)
from src.runtime.published_snapshot import SnapshotStore
from src.management.projects import (
    add_linked_item as add_project_linked_item,
    add_management_note as add_project_management_note,
    add_milestone as add_project_milestone,
    complete_milestone as complete_project_milestone,
    remove_linked_item as remove_project_linked_item,
    set_project_status,
    update_project_fields,
)

ROOT = Path(__file__).resolve().parents[2]
OBJECTIVE_ACTION_PATH = re.compile(r"^/api/objectives/([^/]+)/actions$")
PROJECT_ACTION_PATH = re.compile(r"^/api/projects/([^/]+)/actions$")
MATTER_ACTION_PATH = re.compile(r"^/api/matters/([^/]+)/actions$")
OBJECTIVE_DETAIL_PATH = re.compile(r"^/api/objectives/([^/]+)\.json$")
PROJECT_DETAIL_PATH = re.compile(r"^/api/projects/([^/]+)\.json$")
MATTER_DETAIL_PATH = re.compile(r"^/api/matters/([^/]+)\.json$")
DOMAIN_API_PATH = re.compile(r"^/api/(objectives|projects|decisions|followups|open-loops|risks|companies|people|governance|operations|meetings|daily-brief|matters)\.json$")


class AlfredAppHandler(SimpleHTTPRequestHandler):
    server_version = "AlfredAppServer/1.0"

    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/dashboard-home.json":
            self._send_json(self.server.snapshot_store.read_bootstrap())
            return
        if parsed.path == "/api/refresh-status.json":
            self._send_json(self.server.snapshot_store.read_refresh_status())
            return
        if match := OBJECTIVE_DETAIL_PATH.match(parsed.path):
            self._send_json(self.server.snapshot_store.read_domain_detail("objectives", match.group(1)))
            return
        if match := PROJECT_DETAIL_PATH.match(parsed.path):
            self._send_json(self.server.snapshot_store.read_domain_detail("projects", match.group(1)))
            return
        if match := MATTER_DETAIL_PATH.match(parsed.path):
            self._send_json(self.server.snapshot_store.read_domain_detail("matters", match.group(1)))
            return
        if match := DOMAIN_API_PATH.match(parsed.path):
            domain = match.group(1).replace("-", "_")
            self._send_json(self.server.snapshot_store.read_domain(domain))
            return
        if parsed.path.startswith("/api/"):
            self.send_error(HTTPStatus.NOT_FOUND, "API route not found")
            return
        return super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if match := OBJECTIVE_ACTION_PATH.match(parsed.path):
            payload = self._read_json_body()
            response = self._handle_objective_action(match.group(1), payload)
            self._send_json(response)
            return
        if match := PROJECT_ACTION_PATH.match(parsed.path):
            payload = self._read_json_body()
            response = self._handle_project_action(match.group(1), payload)
            self._send_json(response)
            return
        if match := MATTER_ACTION_PATH.match(parsed.path):
            payload = self._read_json_body()
            response = self._handle_matter_action(match.group(1), payload)
            self._send_json(response)
            return
        if parsed.path == "/api/refresh-now":
            status = self.server.snapshot_store.refresh_async(trigger="manual")
            self._send_json({"status": "accepted", "refresh": status.as_dict()}, status=202)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "API route not found")

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        super().log_message(format, *args)

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b"{}"
        return json.loads(body.decode("utf-8") or "{}")

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _handle_objective_action(self, objective_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        action = payload.get("action", "update_fields")
        actor = payload.get("actor", "user")
        reason = payload.get("reason", "")

        if action == "update_fields":
            update_objective_fields(objective_id, payload.get("changes", {}), actor=actor, reason=reason)
        elif action == "add_management_note":
            add_management_note(objective_id, payload.get("text", ""), actor=actor, reason=reason)
        elif action == "add_milestone":
            add_milestone(
                objective_id,
                title=payload.get("title", ""),
                due_date=payload.get("due_date"),
                actor=actor,
                reason=reason,
            )
        elif action == "complete_milestone":
            from src.management.objectives import complete_milestone

            complete_milestone(objective_id, payload.get("milestone_id", ""), actor=actor, reason=reason)
        elif action == "link_item":
            add_linked_item(
                objective_id,
                payload.get("field", ""),
                payload.get("item", {}),
                current_items=payload.get("current_items"),
                actor=actor,
                reason=reason,
            )
        elif action == "unlink_item":
            remove_linked_item(
                objective_id,
                payload.get("field", ""),
                payload.get("item_key", ""),
                current_items=payload.get("current_items"),
                actor=actor,
                reason=reason,
            )
        elif action == "set_status":
            set_objective_status(
                objective_id,
                payload.get("status", "Not defined"),
                payload.get("rag_rating", "Not defined"),
                actor=actor,
                reason=reason,
            )
        elif action == "run_smart_enrichment":
            detail = self.server.snapshot_store.read_domain_detail("objectives", objective_id)
            create_smart_proposal(objective_id, detail, actor=actor, reason=reason)
        elif action == "accept_smart_proposal":
            accept_smart_proposal(objective_id, selected_fields=payload.get("fields"), actor=actor, reason=reason)
        elif action == "reject_smart_proposal":
            reject_smart_proposal(objective_id, actor=actor, reason=reason)
        elif action == "hold_objective":
            set_objective_status(objective_id, "HOLD", "AMBER", actor=actor, reason=reason or "Objective placed on hold.")
        elif action == "close_objective":
            set_objective_status(objective_id, "CLOSED", "GREEN", actor=actor, reason=reason or "Objective closed.")
        elif action == "reopen_objective":
            set_objective_status(objective_id, "SUPPORTED", "GREEN", actor=actor, reason=reason or "Objective reopened.")
        else:
            return {"status": "error", "message": f"Unsupported action: {action}"}
        self.server.snapshot_store.refresh_async(trigger="objective_action")
        return {"status": "ok", "action": action, "objective_id": objective_id}

    def _handle_project_action(self, project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        action = payload.get("action", "update_fields")
        actor = payload.get("actor", "user")
        reason = payload.get("reason", "")

        if action == "update_fields":
            update_project_fields(project_id, payload.get("changes", {}), actor=actor, reason=reason)
        elif action == "add_management_note":
            add_project_management_note(project_id, payload.get("text", ""), actor=actor, reason=reason)
        elif action == "add_milestone":
            add_project_milestone(
                project_id,
                title=payload.get("title", ""),
                due_date=payload.get("due_date"),
                actor=actor,
                reason=reason,
            )
        elif action == "complete_milestone":
            complete_project_milestone(project_id, payload.get("milestone_id", ""), actor=actor, reason=reason)
        elif action == "link_item":
            add_project_linked_item(
                project_id,
                payload.get("field", ""),
                payload.get("item", {}),
                current_items=payload.get("current_items"),
                actor=actor,
                reason=reason,
            )
        elif action == "unlink_item":
            remove_project_linked_item(
                project_id,
                payload.get("field", ""),
                payload.get("item_key", ""),
                current_items=payload.get("current_items"),
                actor=actor,
                reason=reason,
            )
        elif action == "hold_project":
            set_project_status(project_id, "HOLD", "AMBER", actor=actor, reason=reason or "Project placed on hold.")
        elif action == "close_project":
            set_project_status(project_id, "CLOSED", "GREEN", actor=actor, reason=reason or "Project closed.")
        elif action == "reopen_project":
            set_project_status(project_id, "SUPPORTED", "GREEN", actor=actor, reason=reason or "Project reopened.")
        else:
            return {"status": "error", "message": f"Unsupported action: {action}"}
        self.server.snapshot_store.refresh_async(trigger="project_action")
        return {"status": "ok", "action": action, "project_id": project_id}

    def _handle_matter_action(self, matter_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        action = payload.get("action", "update_fields")
        actor = payload.get("actor", "user")
        reason = payload.get("reason", "")

        if action == "update_fields":
            update_matter_fields(matter_id, payload.get("changes", {}), actor=actor, reason=reason)
        elif action == "add_management_note":
            add_matter_management_note(matter_id, payload.get("text", ""), actor=actor, reason=reason)
        elif action == "set_owner":
            update_matter_fields(matter_id, {"owner": payload.get("owner", "Not defined")}, actor=actor, reason=reason)
        elif action == "set_priority":
            update_matter_fields(matter_id, {"priority": payload.get("priority", "Not defined")}, actor=actor, reason=reason)
        elif action == "hold_matter":
            update_matter_fields(
                matter_id,
                {"status": "HOLD", "hold_reason": reason or "Matter placed on hold."},
                actor=actor,
                reason=reason or "Matter placed on hold.",
            )
        elif action == "resolve_matter":
            update_matter_fields(
                matter_id,
                {"status": "RESOLVED", "resolution_note": reason or "Matter resolved."},
                actor=actor,
                reason=reason or "Matter resolved.",
            )
        elif action == "dismiss_matter":
            update_matter_fields(
                matter_id,
                {"status": "DISMISSED", "dismiss_reason": reason or "Matter dismissed."},
                actor=actor,
                reason=reason or "Matter dismissed.",
            )
        elif action == "reopen_matter":
            update_matter_fields(
                matter_id,
                {"status": "OPEN", "hold_reason": "", "dismiss_reason": "", "resolution_note": ""},
                actor=actor,
                reason=reason or "Matter reopened.",
            )
        else:
            return {"status": "error", "message": f"Unsupported action: {action}"}
        self.server.snapshot_store.refresh_async(trigger="matter_action")
        return {"status": "ok", "action": action, "matter_id": matter_id}


def main() -> None:
    install_root = Path(os.environ.get("ALFRED_INSTALL_ROOT", ROOT)).resolve()
    config_path = install_root / "config" / "config.yaml"
    host = "127.0.0.1"
    port = 4173
    if config_path.exists():
        import yaml

        config = yaml.safe_load(config_path.read_text()) or {}
        runtime = config.get("runtime", {})
        host = runtime.get("host", host)
        port = int(runtime.get("ui_port", port))

    static_root = install_root / "app" / "dist"
    if not static_root.exists():
        static_root = ROOT / "dist"
    evidence_root = ROOT / "evidence" / "alfred-inventory"
    if (install_root / "app" / "evidence" / "alfred-inventory").exists():
        evidence_root = install_root / "app" / "evidence" / "alfred-inventory"
    snapshot_store = SnapshotStore(
        install_root=install_root,
        evidence_root=evidence_root,
        vault_root=Path(os.environ.get("ALFRED_OBSIDIAN_VAULT", "/docker/obsidian-vault")),
    )
    snapshot_store.ensure_snapshot()
    _start_daily_refresh(snapshot_store)

    handler = partial(AlfredAppHandler, directory=str(static_root))
    server = ThreadingHTTPServer((host, port), handler)
    server.snapshot_store = snapshot_store  # type: ignore[attr-defined]
    try:
        server.serve_forever()
    finally:
        server.server_close()


def _start_daily_refresh(snapshot_store: SnapshotStore) -> None:
    def _runner() -> None:
        while True:
            time.sleep(24 * 60 * 60)
            snapshot_store.refresh_async(trigger="scheduled")

    thread = threading.Thread(target=_runner, daemon=True, name="alfred-snapshot-refresh")
    thread.start()


if __name__ == "__main__":
    main()
