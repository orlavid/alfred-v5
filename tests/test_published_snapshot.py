from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
import time

import src.runtime.published_snapshot as snapshot_module
from src.runtime.published_snapshot import SnapshotStore


def _payload(label: str) -> dict[str, object]:
    return {
        "burning_fires": [{"type": "risk", "summary": f"{label} fire"}],
        "plan_today": [{"type": "plan", "summary": f"{label} plan", "confidence": "HIGH", "origin": "test", "provider": "test", "source_notes": []}],
        "next_best_action": {"priority": "HIGH", "action": f"{label} action", "why_it_matters": "Test", "confidence": "HIGH"},
        "operating_picture": {
            "overall_health": "GREEN",
            "confidence": "HIGH",
            "meeting_focus": "None",
            "followup_pressure": {"overdue": 0, "due_today": 0, "high_priority": 0},
            "open_loop_pressure": {"critical": 0, "waiting_for": 0, "missing_owners": 0},
            "summary": [f"{label} summary"],
        },
        "navigation_priorities": [{"label": "Priorities", "reason": f"{label} reason"}],
        "interruption_policy": {"level": "filter", "rule": "Only interrupt for priority issues."},
        "objectives": {"health": {"total": 1}, "summary": [], "items": [], "details": {}},
        "projects": {"health": {"total": 1}, "summary": [], "items": [], "details": {}},
        "decisions": {"counts": {"total": 1, "defined_status": 1, "owner_defined": 1, "source_notes": 1}, "summary": [], "items": [], "details": {}},
        "followups": {"counts": {"total": 12, "overdue": 3, "due_today": 2, "due_this_week": 7, "waiting_on_others": 4, "high_priority": 5}, "summary": [], "recommendations": [], "items": []},
        "open_loops": {"counts": {"total": 15, "critical": 4, "waiting_for": 5, "stalled_projects": 2, "missing_decisions": 1, "missing_owners": 1}, "summary": [], "recommended_actions": [], "items": []},
        "meetings": {"subject": "No active meeting identified.", "executive_summary": [], "related_people": [], "related_projects": [], "related_companies": [], "related_objectives": [], "related_decisions": [], "risks": [], "open_loops": [], "follow_ups": [], "recommended_discussion": [], "confidence": "LOW"},
        "board": {"summary": [], "members": [], "weekly_meeting": [], "monthly_meeting": [], "standing_agenda": []},
        "ask_alfred": {"questions": ["What should I do today?"], "responses": [{"question": "What should I do today?", "executive_answer": ["Proceed"], "supporting_evidence": [], "confidence": "HIGH", "recommended_next_actions": ["Proceed"]}]},
        "daily_brief": {
            "executive_health": [],
            "overnight_changes": [],
            "top_three_priorities": [],
            "meetings_requiring_preparation": [],
            "followups_due_today": ["Brief subset"],
            "open_loops_blocking_progress": ["Loop subset"],
            "risks_escalating": [],
            "decisions_awaiting_you": [],
            "recommended_agenda": [],
            "one_page_executive_summary": [],
            "confidence": "HIGH",
        },
        "knowledge": {"summary": [], "entity_counts": {}, "graph": {"node_count": 1, "edge_count": 1, "top_nodes": []}},
        "admin_configuration": {
            "overview": {"environment_score": 100, "overall_health": "GREEN", "architecture_rule": "", "summary_lines": []},
            "sections": {
                "core_configuration": [],
                "vault": [],
                "ai_providers": [],
                "knowledge_sources": [],
                "runtime": [],
                "services": [],
                "security": [],
                "diagnostics": [],
                "deployment": [],
                "required_actions": [],
            },
            "auto_configured": {},
            "doctor_summary": {"environment_score": 100, "healthy": [], "warnings": [], "disabled": [], "recommended_actions": [], "summary_lines": []},
            "actions": [],
        },
        "generated_from": {"meeting_subject": None, "runtime_model": "ExecutiveState", "production_mode": True, "sources": ["ExecutiveState"], "confidence": "HIGH"},
    }


@dataclass(frozen=True)
class _FakeCheck:
    status: str


def _seed_snapshot_environment(monkeypatch, tmp_path: Path, label: str = "current") -> SnapshotStore:
    vault = tmp_path / "vault"
    vault.mkdir(parents=True)
    (vault / "note.md").write_text(f"# {label}\n")
    app_root = tmp_path / "app"
    (app_root / "output").mkdir(parents=True, exist_ok=True)
    for name in (
        "Executive_Knowledge.json",
        "Knowledge_Graph.json",
        "Executive_Pipeline_Report.md",
        "Live_Vault_Status.md",
        "LIVE_KNOWLEDGE_CERTIFICATION.md",
        "Knowledge_Certification.md",
        "Knowledge_Certification.json",
        "Semantic_Equivalence_Validation.md",
        "Semantic_Equivalence_Validation.json",
        "Environment_Inventory.json",
        "Environment_Inventory.md",
    ):
        (app_root / "output" / name).write_text("{}")

    monkeypatch.setattr(snapshot_module, "get_dashboard_home", lambda *_args, **_kwargs: _payload(label))
    monkeypatch.setattr(snapshot_module, "build_executive_state", lambda *_args, **_kwargs: SimpleNamespace(adapter=SimpleNamespace(vault_root=vault), companies=(), people=()))
    monkeypatch.setattr(snapshot_module, "render_executive_state_summary", lambda _state: "# ExecutiveState\n")
    monkeypatch.setattr(snapshot_module, "build_executive_reasoning_from_state", lambda _state: SimpleNamespace())
    monkeypatch.setattr(snapshot_module, "render_executive_reasoning", lambda _reasoning: "# Reasoning\n")
    monkeypatch.setattr(snapshot_module, "build_daily_brief_from_state", lambda _state, reasoning=None: SimpleNamespace())
    monkeypatch.setattr(snapshot_module, "render_daily_brief", lambda _brief: "# Brief\n")
    monkeypatch.setattr(
        snapshot_module,
        "build_operational_readiness",
        lambda output_dir=None: SimpleNamespace(overall_health="GREEN", checks=(_FakeCheck("PASS"),)),
    )
    return SnapshotStore(
        install_root=tmp_path,
        evidence_root=tmp_path / "evidence",
        vault_root=vault,
    )


def test_snapshot_publish_creates_bootstrap_and_domain_files(monkeypatch, tmp_path):
    store = _seed_snapshot_environment(monkeypatch, tmp_path, label="published")

    result = store.publish_snapshot(trigger="test")

    bootstrap = store.read_bootstrap()
    objectives = store.read_domain("objectives")
    refresh_status = store.read_refresh_status()

    assert result.bootstrap_size_bytes > 0
    assert bootstrap["next_best_action"]["action"] == "published action"
    assert "projects" in bootstrap
    assert objectives["health"]["total"] == 1
    assert refresh_status["current_snapshot_version"] == result.version
    assert refresh_status["bootstrap_payload_size_bytes"] == result.bootstrap_size_bytes


def test_snapshot_failed_refresh_preserves_previous_snapshot(monkeypatch, tmp_path):
    store = _seed_snapshot_environment(monkeypatch, tmp_path, label="before")
    initial = store.publish_snapshot(trigger="initial")
    previous_bootstrap = store.read_bootstrap()

    monkeypatch.setattr(
        snapshot_module,
        "_validate_snapshot_payloads",
        lambda files: ("Dashboard_Home.json: forbidden string `Reconnect Alfred`",),
    )

    try:
        store.publish_snapshot(trigger="broken")
        raise AssertionError("expected publish_snapshot to fail")
    except RuntimeError:
        pass

    assert store.load_status().current_snapshot_version == initial.version
    assert store.read_bootstrap() == previous_bootstrap


def test_snapshot_serves_previous_content_while_refresh_runs(monkeypatch, tmp_path):
    store = _seed_snapshot_environment(monkeypatch, tmp_path, label="before")
    store.publish_snapshot(trigger="initial")
    previous_bootstrap = store.read_bootstrap()

    def slow_dashboard(*_args, **_kwargs):
        time.sleep(0.3)
        return _payload("after")

    monkeypatch.setattr(snapshot_module, "get_dashboard_home", slow_dashboard)

    store.refresh_async(trigger="manual")
    time.sleep(0.05)

    status = store.load_status()
    assert status.refresh_in_progress is True
    assert store.read_bootstrap() == previous_bootstrap

    while store.load_status().refresh_in_progress:
        time.sleep(0.05)

    assert store.read_bootstrap()["next_best_action"]["action"] == "after action"


def test_snapshot_validation_blocks_runtime_placeholders(monkeypatch, tmp_path):
    store = _seed_snapshot_environment(monkeypatch, tmp_path, label="placeholder")

    def placeholder_payload(*_args, **_kwargs):
        payload = _payload("placeholder")
        payload["next_best_action"]["action"] = "Reconnect Alfred"
        return payload

    monkeypatch.setattr(snapshot_module, "get_dashboard_home", placeholder_payload)

    try:
        store.publish_snapshot(trigger="placeholder")
        raise AssertionError("expected publish_snapshot to fail on runtime placeholder")
    except RuntimeError as exc:
        assert "snapshot_validation=FAIL" in str(exc)
