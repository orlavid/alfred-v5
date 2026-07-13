"""Published snapshot store for Alfred UI payloads."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import threading
from typing import Any

from src.api.dashboard_api import get_dashboard_home
from src.daily.daily_brief import build_daily_brief_from_state, render_daily_brief
from src.executive.executive_reasoning import build_executive_reasoning_from_state, render_executive_reasoning
from src.executive.executive_state import render_executive_state_summary
from src.executive.executive_state import build_executive_state
from src.operations.doctor import build_operational_readiness
from src.operations.config_registry import build_configuration_registry


@dataclass(frozen=True)
class SnapshotStatus:
    version: str | None
    build_timestamp: str | None
    source_vault_timestamp: str | None
    deployed_commit: str | None
    certification_status: str
    last_successful_refresh: str | None
    last_failed_refresh: str | None
    last_failed_reason: str | None
    refresh_in_progress: bool
    refresh_started_at: str | None
    current_snapshot_version: str | None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SnapshotPublicationResult:
    version: str
    snapshot_dir: Path
    bootstrap_size_bytes: int
    domain_sizes: dict[str, int]
    detail_domain_sizes: dict[str, dict[str, int]]
    build_timestamp: str
    source_vault_timestamp: str | None
    deployed_commit: str
    certification_status: str
    validation_status: str
    readiness_status: str
    refresh_duration_seconds: float


@dataclass
class SnapshotStore:
    install_root: Path
    evidence_root: Path
    vault_root: Path
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _refresh_thread: threading.Thread | None = None

    @property
    def runtime_dir(self) -> Path:
        return self.install_root / "runtime"

    @property
    def snapshot_root(self) -> Path:
        return self.runtime_dir / "published_snapshots"

    @property
    def versions_dir(self) -> Path:
        return self.snapshot_root / "versions"

    @property
    def current_link(self) -> Path:
        return self.snapshot_root / "current"

    @property
    def status_path(self) -> Path:
        return self.snapshot_root / "status.json"

    def ensure_snapshot(self) -> None:
        self._ensure_dirs()
        if self.current_link.exists():
            return
        self.publish_snapshot(trigger="startup")

    def load_status(self) -> SnapshotStatus:
        self._ensure_dirs()
        if not self.status_path.exists():
            return SnapshotStatus(
                version=None,
                build_timestamp=None,
                source_vault_timestamp=None,
                deployed_commit=None,
                certification_status="UNKNOWN",
                last_successful_refresh=None,
                last_failed_refresh=None,
                last_failed_reason=None,
                refresh_in_progress=False,
                refresh_started_at=None,
                current_snapshot_version=None,
            )
        data = json.loads(self.status_path.read_text())
        return SnapshotStatus(**data)

    def refresh_async(self, *, trigger: str) -> SnapshotStatus:
        with self._lock:
            status = self.load_status()
            if self._refresh_thread and self._refresh_thread.is_alive():
                return status
            started_at = _now_iso()
            self._write_status(
                SnapshotStatus(
                    version=status.version,
                    build_timestamp=status.build_timestamp,
                    source_vault_timestamp=status.source_vault_timestamp,
                    deployed_commit=status.deployed_commit,
                    certification_status=status.certification_status,
                    last_successful_refresh=status.last_successful_refresh,
                    last_failed_refresh=status.last_failed_refresh,
                    last_failed_reason=status.last_failed_reason,
                    refresh_in_progress=True,
                    refresh_started_at=started_at,
                    current_snapshot_version=status.current_snapshot_version,
                )
            )
            self._refresh_thread = threading.Thread(
                target=self._refresh_runner,
                kwargs={"trigger": trigger},
                daemon=True,
            )
            self._refresh_thread.start()
            return self.load_status()

    def publish_snapshot(self, *, trigger: str) -> SnapshotPublicationResult:
        self._ensure_dirs()
        started = datetime.now(UTC)
        version = _snapshot_version(started)
        staging_dir = Path(tempfile.mkdtemp(prefix=f"snapshot-{version}-", dir=self.snapshot_root))
        try:
            app_root = _app_root(self.install_root)
            staged_output_dir = staging_dir / "output"
            staged_output_dir.mkdir(parents=True, exist_ok=True)
            current_output_dir = app_root / "output"
            if current_output_dir.exists():
                shutil.copytree(current_output_dir, staged_output_dir, dirs_exist_ok=True)

            payload = get_dashboard_home(self.evidence_root, vault_root=self.vault_root)
            state = build_executive_state(self.evidence_root, vault_root=self.vault_root)
            build_timestamp = _now_iso()
            source_vault_timestamp = _latest_mtime_iso(self.vault_root)
            deployed_commit = _deployed_commit(app_root, self.install_root)
            snapshot = _build_snapshot_payloads(
                payload,
                state,
                version=version,
                build_timestamp=build_timestamp,
                source_vault_timestamp=source_vault_timestamp,
                deployed_commit=deployed_commit,
            )

            files_dir = staging_dir / "api"
            files_dir.mkdir(parents=True, exist_ok=True)
            domain_sizes: dict[str, int] = {}
            detail_domain_sizes: dict[str, dict[str, int]] = {}
            for name, data in snapshot["domains"].items():
                size = _write_json(files_dir / f"{name}.json", data)
                domain_sizes[name] = size
            for domain_name, items in snapshot["detail_domains"].items():
                detail_domain_sizes[domain_name] = {}
                for record_id, data in items.items():
                    size = _write_json(files_dir / domain_name / f"{record_id}.json", data)
                    detail_domain_sizes[domain_name][record_id] = size
            bootstrap_size = _write_json(files_dir / "dashboard-home.json", snapshot["bootstrap"])

            _write_json(staged_output_dir / "Dashboard_Home.json", snapshot["bootstrap"])
            _write_json(staging_dir / "manifest.json", snapshot["manifest"])
            (staged_output_dir / "ExecutiveState_Summary.md").write_text(render_executive_state_summary(state))
            reasoning = build_executive_reasoning_from_state(state)
            (staged_output_dir / "Executive_Reasoning.md").write_text(render_executive_reasoning(reasoning))
            brief = build_daily_brief_from_state(state, reasoning=reasoning)
            (staged_output_dir / "Daily_Brief.md").write_text(render_daily_brief(brief))

            readiness = build_operational_readiness(output_dir=staged_output_dir)
            validation_findings = _validate_snapshot_payloads(
                [staged_output_dir / "Dashboard_Home.json", *files_dir.rglob("*.json")]
            )
            validation_status = "PASS" if not validation_findings else "FAIL"

            readiness_has_failure = any(check.status == "FAIL" for check in readiness.checks)
            certification_status = readiness.overall_health if validation_status == "PASS" else "FAIL"
            if validation_status != "PASS" or readiness_has_failure:
                raise RuntimeError(
                    f"snapshot validation failed: operational_readiness={readiness.overall_health}; snapshot_validation={validation_status}"
                )

            published_bootstrap = {
                **snapshot["bootstrap"],
                "snapshot": {
                    **snapshot["bootstrap"]["snapshot"],
                    "build_timestamp": build_timestamp,
                    "source_vault_timestamp": source_vault_timestamp,
                    "deployed_commit": deployed_commit,
                    "certification_status": certification_status,
                    "last_successful_refresh": build_timestamp,
                    "last_failed_refresh": None,
                    "last_failed_reason": None,
                    "refresh_in_progress": False,
                    "refresh_started_at": None,
                    "current_snapshot_version": version,
                },
            }
            bootstrap_size = _write_json(files_dir / "dashboard-home.json", published_bootstrap)
            _write_json(staged_output_dir / "Dashboard_Home.json", published_bootstrap)

            target_version_dir = self.versions_dir / version
            if target_version_dir.exists():
                shutil.rmtree(target_version_dir)
            staging_dir.rename(target_version_dir)
            _replace_symlink(self.current_link, target_version_dir)

            status = SnapshotStatus(
                version=version,
                build_timestamp=build_timestamp,
                source_vault_timestamp=source_vault_timestamp,
                deployed_commit=deployed_commit,
                certification_status=certification_status,
                last_successful_refresh=build_timestamp,
                last_failed_refresh=self.load_status().last_failed_refresh,
                last_failed_reason=None,
                refresh_in_progress=False,
                refresh_started_at=None,
                current_snapshot_version=version,
            )
            self._write_status(status)
            refresh_status = {
                **published_bootstrap["snapshot"],
                "trigger": trigger,
                "bootstrap_payload_size_bytes": bootstrap_size,
                "domain_payload_sizes": domain_sizes,
                "detail_domain_payload_sizes": {
                    domain_name: {
                        "count": len(items),
                        "total_bytes": sum(items.values()),
                        "max_bytes": max(items.values()) if items else 0,
                    }
                    for domain_name, items in detail_domain_sizes.items()
                },
            }
            _write_json(target_version_dir / "refresh-status.json", refresh_status)
            duration = (datetime.now(UTC) - started).total_seconds()
            return SnapshotPublicationResult(
                version=version,
                snapshot_dir=target_version_dir,
                bootstrap_size_bytes=bootstrap_size,
                domain_sizes=domain_sizes,
                detail_domain_sizes=detail_domain_sizes,
                build_timestamp=build_timestamp,
                source_vault_timestamp=status.source_vault_timestamp,
                deployed_commit=status.deployed_commit or "unknown",
                certification_status=certification_status,
                validation_status=validation_status,
                readiness_status=readiness.overall_health,
                refresh_duration_seconds=round(duration, 3),
            )
        except Exception as exc:
            shutil.rmtree(staging_dir, ignore_errors=True)
            previous = self.load_status()
            failed_at = _now_iso()
            self._write_status(
                SnapshotStatus(
                    version=previous.version,
                    build_timestamp=previous.build_timestamp,
                    source_vault_timestamp=previous.source_vault_timestamp,
                    deployed_commit=previous.deployed_commit,
                    certification_status=previous.certification_status,
                    last_successful_refresh=previous.last_successful_refresh,
                    last_failed_refresh=failed_at,
                    last_failed_reason=str(exc),
                    refresh_in_progress=False,
                    refresh_started_at=None,
                    current_snapshot_version=previous.current_snapshot_version,
                )
            )
            raise

    def current_snapshot_dir(self) -> Path:
        self.ensure_snapshot()
        if self.current_link.is_symlink():
            return self.current_link.resolve()
        return self.current_link

    def read_bootstrap(self) -> dict[str, Any]:
        return self._read_current_json("api/dashboard-home.json")

    def read_domain(self, name: str) -> dict[str, Any]:
        return self._read_current_json(f"api/{name}.json")

    def read_domain_detail(self, domain: str, record_id: str) -> dict[str, Any]:
        return self._read_current_json(f"api/{domain}/{record_id}.json")

    def read_refresh_status(self) -> dict[str, Any]:
        current = self.current_snapshot_dir() / "refresh-status.json"
        if current.exists():
            current_data = json.loads(current.read_text())
        else:
            current_data = self.load_status().as_dict()
        live_status = self.load_status().as_dict()
        current_data.update(
            {
                "refresh_in_progress": live_status["refresh_in_progress"],
                "refresh_started_at": live_status["refresh_started_at"],
                "last_failed_refresh": live_status["last_failed_refresh"],
                "last_failed_reason": live_status["last_failed_reason"],
                "last_successful_refresh": live_status["last_successful_refresh"],
                "current_snapshot_version": live_status["current_snapshot_version"],
            }
        )
        return current_data

    def _read_current_json(self, relative_path: str) -> dict[str, Any]:
        path = self.current_snapshot_dir() / relative_path
        return json.loads(path.read_text())

    def _ensure_dirs(self) -> None:
        self.snapshot_root.mkdir(parents=True, exist_ok=True)
        self.versions_dir.mkdir(parents=True, exist_ok=True)

    def _write_status(self, status: SnapshotStatus) -> None:
        self.snapshot_root.mkdir(parents=True, exist_ok=True)
        self.status_path.write_text(json.dumps(status.as_dict(), indent=2, sort_keys=True))

    def _refresh_runner(self, *, trigger: str) -> None:
        try:
            self.publish_snapshot(trigger=trigger)
        finally:
            pass


def _build_snapshot_payloads(
    payload: dict[str, Any],
    state,
    *,
    version: str,
    build_timestamp: str,
    source_vault_timestamp: str | None,
    deployed_commit: str,
) -> dict[str, Any]:
    manifest = {
        "snapshot_version": version,
        "build_timestamp": build_timestamp,
        "source_vault_timestamp": source_vault_timestamp,
        "deployed_commit": deployed_commit,
        "certification_status": "PENDING",
    }
    bootstrap = {
        "snapshot": {
            **manifest,
            "last_successful_refresh": None,
            "last_failed_refresh": None,
            "last_failed_reason": None,
            "refresh_in_progress": False,
        },
        "burning_fires": payload["burning_fires"],
        "plan_today": payload["plan_today"],
        "next_best_action": payload["next_best_action"],
        "operating_picture": payload["operating_picture"],
        "navigation_priorities": payload["navigation_priorities"],
        "interruption_policy": payload["interruption_policy"],
        "objectives": {
            "health": payload["objectives"]["health"],
            "summary": payload["objectives"]["summary"],
            "count": len(payload["objectives"]["items"]),
        },
        "projects": {
            "health": payload["projects"]["health"],
            "summary": payload["projects"]["summary"],
            "count": len(payload["projects"]["items"]),
        },
        "decisions": {
            "counts": payload["decisions"]["counts"],
            "summary": payload["decisions"]["summary"],
        },
        "followups": {
            "counts": payload["followups"]["counts"],
            "summary": payload["followups"]["summary"],
            "recommendations": payload["followups"]["recommendations"],
        },
        "open_loops": {
            "counts": payload["open_loops"]["counts"],
            "summary": payload["open_loops"]["summary"],
            "recommended_actions": payload["open_loops"]["recommended_actions"],
        },
        "meetings": payload["meetings"],
        "board": payload["board"],
        "ask_alfred": payload["ask_alfred"],
        "daily_brief": payload["daily_brief"],
        "knowledge": {
            "summary": payload["knowledge"]["summary"],
            "entity_counts": payload["knowledge"]["entity_counts"],
            "graph": {
                "node_count": payload["knowledge"]["graph"]["node_count"],
                "edge_count": payload["knowledge"]["graph"]["edge_count"],
                "top_nodes": payload["knowledge"]["graph"]["top_nodes"][:10],
            },
        },
        "admin_configuration": payload["admin_configuration"],
        "generated_from": payload["generated_from"],
    }
    domains = {
        "objectives": {
            "health": payload["objectives"]["health"],
            "items": payload["objectives"]["items"],
            "summary": payload["objectives"]["summary"],
        },
        "projects": {
            "health": payload["projects"]["health"],
            "items": payload["projects"]["items"],
            "summary": payload["projects"]["summary"],
        },
        "decisions": payload["decisions"],
        "followups": payload["followups"],
        "open_loops": payload["open_loops"],
        "risks": {
            "items": payload["daily_brief"]["risks_escalating"],
            "summary": payload["operating_picture"]["summary"],
        },
        "companies": {
            "items": [
                {
                    "title": item.title,
                    "path": item.path,
                    "status": item.status,
                    "projects": item.projects,
                    "objectives": item.objectives,
                    "score": item.score,
                }
                for item in getattr(state, "companies", ())
            ],
        },
        "people": {
            "items": [
                {
                    "title": item.title,
                    "path": item.path,
                    "projects": item.projects,
                    "companies": item.companies,
                    "objectives": item.objectives,
                    "decisions": item.decisions,
                    "risk": item.risk,
                }
                for item in getattr(state, "people", ())
            ],
        },
        "governance": payload["board"],
        "operations": payload["admin_configuration"],
        "meetings": payload["meetings"],
        "daily_brief": payload["daily_brief"],
    }
    detail_domains = {
        "objectives": payload["objectives"].get("details", {}),
        "projects": payload["projects"].get("details", {}),
    }
    refresh_status = {
        **bootstrap["snapshot"],
        "bootstrap_payload_size_bytes": 0,
        "domain_payload_sizes": {},
        "detail_domain_payload_sizes": {},
    }
    return {
        "bootstrap": bootstrap,
        "domains": domains,
        "detail_domains": detail_domains,
        "manifest": manifest,
        "refresh_status": refresh_status,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(payload, indent=2, sort_keys=True)
    path.write_text(body)
    return len(body.encode("utf-8"))


def _replace_symlink(link_path: Path, target: Path) -> None:
    temp_link = link_path.with_suffix(".tmp")
    if temp_link.exists() or temp_link.is_symlink():
        temp_link.unlink()
    os.symlink(target, temp_link)
    os.replace(temp_link, link_path)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _latest_mtime_iso(root: Path) -> str | None:
    if not root.exists():
        return None
    latest = 0.0
    for path in root.rglob("*.md"):
        latest = max(latest, path.stat().st_mtime)
    return datetime.fromtimestamp(latest, UTC).isoformat() if latest else None


def _snapshot_version(now: datetime) -> str:
    seed = now.isoformat()
    return f"{now.strftime('%Y%m%dT%H%M%SZ')}-{hashlib.sha1(seed.encode('utf-8')).hexdigest()[:8]}"


def _git_commit(root: Path) -> str:
    head = root / ".git" / "HEAD"
    if not head.exists():
        return "unknown"
    ref = head.read_text().strip()
    if ref.startswith("ref: "):
        ref_path = root / ".git" / ref.removeprefix("ref: ").strip()
        if ref_path.exists():
            return ref_path.read_text().strip()
    return ref


def _app_root(install_root: Path) -> Path:
    app_root = install_root / "app"
    return app_root if app_root.exists() else install_root


def _deployed_commit(app_root: Path, install_root: Path) -> str:
    commit = _git_commit(app_root)
    if commit != "unknown":
        return commit
    build_info_path = install_root / "runtime" / "BUILD_INFO"
    if build_info_path.exists():
        for line in build_info_path.read_text().splitlines():
            if line.startswith("build_version="):
                value = line.partition("=")[2].strip()
                if value:
                    return value
    return "unknown"


def _validate_snapshot_payloads(files: list[Path]) -> tuple[str, ...]:
    registry = build_configuration_registry()
    forbidden = tuple(
        value
        for value in registry.forbidden_output_strings
        if value == "Reconnect Alfred" or value.startswith("DEFAULT_")
    )
    findings: list[str] = []
    for path in files:
        text = path.read_text(errors="ignore")
        for value in forbidden:
            if value in text:
                findings.append(f"{path.name}: forbidden string `{value}`")
    return tuple(findings)
