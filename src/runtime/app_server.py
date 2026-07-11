"""Alfred application server with static UI hosting and management APIs."""

from __future__ import annotations

from functools import partial
import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

from src.api.dashboard_api import get_dashboard_home
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

ROOT = Path(__file__).resolve().parents[2]
OBJECTIVE_ACTION_PATH = re.compile(r"^/api/objectives/([^/]+)/actions$")


class AlfredAppHandler(SimpleHTTPRequestHandler):
    server_version = "AlfredAppServer/1.0"

    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/api/dashboard-home.json":
            self._send_json(get_dashboard_home())
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
            dashboard = get_dashboard_home()
            detail = dashboard["objectives"]["details"][objective_id]
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

        return {"status": "ok", "action": action, "objective_id": objective_id}


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
    handler = partial(AlfredAppHandler, directory=str(static_root))
    server = ThreadingHTTPServer((host, port), handler)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
