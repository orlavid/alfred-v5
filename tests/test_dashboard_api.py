from pathlib import Path
import inspect
import json
import subprocess
import sys
from types import SimpleNamespace

from src.api.dashboard_api import get_dashboard_home
from src.followups.followup_intelligence import FollowupIntelligence, FollowupItem
from src.openloops.open_loop_intelligence import OpenLoopIntelligence, OpenLoopItem


def test_get_dashboard_home_returns_expected_shape():
    payload = get_dashboard_home(Path("evidence/alfred-inventory"))

    assert "burning_fires" in payload
    assert "plan_today" in payload
    assert "next_best_action" in payload
    assert "operating_picture" in payload
    assert "navigation_priorities" in payload
    assert "interruption_policy" in payload
    assert "generated_from" in payload
    assert "objectives" in payload
    assert "projects" in payload
    assert "followups" in payload
    assert "open_loops" in payload
    assert "meetings" in payload
    assert "board" in payload
    assert "ask_alfred" in payload
    assert "daily_brief" in payload
    assert "knowledge" in payload
    assert "admin_configuration" in payload
    assert isinstance(payload["burning_fires"], list)
    assert isinstance(payload["plan_today"], list)
    assert isinstance(payload["next_best_action"], dict)
    assert isinstance(payload["operating_picture"], dict)
    assert isinstance(payload["navigation_priorities"], list)
    assert isinstance(payload["interruption_policy"], dict)
    assert isinstance(payload["followups"]["items"], list)
    assert isinstance(payload["open_loops"]["items"], list)
    assert payload["generated_from"]["runtime_model"] == "ExecutiveState"
    assert "Executive Reasoning" in payload["generated_from"]["sources"]
    assert payload["board"]["members"]
    assert payload["ask_alfred"]["responses"]
    assert payload["admin_configuration"]["actions"]
    assert payload["admin_configuration"]["overview"]["environment_score"] >= 0
    assert payload["generated_from"]["production_mode"] is True
    if payload["burning_fires"]:
        assert {"origin", "confidence", "source_notes", "provider"} <= payload["burning_fires"][0].keys()
    if payload["plan_today"]:
        assert {"origin", "confidence", "source_notes", "provider"} <= payload["plan_today"][0].keys()
    assert {"origin", "confidence", "source_notes", "provider"} <= payload["next_best_action"].keys()


def test_dashboard_empty_vault_returns_explicit_no_evidence(tmp_path):
    payload = get_dashboard_home(tmp_path / "missing-evidence", vault_root=tmp_path / "missing-vault")

    assert payload["next_best_action"]["action"] == "No evidence found"
    assert payload["meetings"]["subject"] == "No active meeting identified."


def test_build_dashboard_api_generates_json_output():
    output = Path("output/Dashboard_Home.json")
    public_output = Path("web/public/api/dashboard-home.json")
    objectives_output = Path("web/public/api/objectives.json")
    projects_output = Path("web/public/api/projects.json")
    if output.exists():
        output.unlink()
    if public_output.exists():
        public_output.unlink()
    if objectives_output.exists():
        objectives_output.unlink()
    if projects_output.exists():
        projects_output.unlink()

    result = subprocess.run(
        [sys.executable, "build_dashboard_api.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output.exists()
    assert public_output.exists()
    assert objectives_output.exists()
    assert projects_output.exists()

    payload = json.loads(output.read_text())
    objectives_payload = json.loads(objectives_output.read_text())
    projects_payload = json.loads(projects_output.read_text())
    assert "burning_fires" in payload
    assert "plan_today" in payload
    assert "next_best_action" in payload
    assert "operating_picture" in payload
    assert "navigation_priorities" in payload
    assert "interruption_policy" in payload
    assert "generated_from" in payload
    assert "followups" in payload
    assert "open_loops" in payload
    assert "board" in payload
    assert "admin_configuration" in payload
    assert objectives_output.stat().st_size > 0
    assert projects_output.stat().st_size > 0
    assert "details" not in objectives_payload
    assert "details" not in projects_payload
    assert public_output.stat().st_size < 100_000


def test_dashboard_consumes_executive_state_only():
    import src.api.dashboard_api as dashboard_api_module

    source = inspect.getsource(dashboard_api_module)

    assert "build_executive_state(" in source
    assert "build_executive_knowledge(" not in source
    assert "load_vault(" not in source


def test_dashboard_does_not_depend_on_direct_followup_or_open_loop_builders():
    import src.api.dashboard_api as dashboard_api_module

    source = inspect.getsource(dashboard_api_module)

    assert "build_followup_intelligence(" not in source
    assert "build_open_loop_intelligence(" not in source


def test_objective_management_payload_includes_summary_and_detail_fields(tmp_path):
    vault = tmp_path / "vault"
    (vault / "09 Governance" / "Objectives").mkdir(parents=True)
    (vault / "03 Projects").mkdir(parents=True)
    (vault / "09 Governance" / "Decisions").mkdir(parents=True)
    (vault / "08 Follow Ups").mkdir(parents=True)
    (vault / "07 Open Loops").mkdir(parents=True)

    (vault / "09 Governance" / "Objectives" / "2026 Executive Objectives.md").write_text(
        "# 2026 Executive Objectives\n\n"
        "## Objectives\n\n"
        "- Operational Governance\n"
    )
    (vault / "09 Governance" / "Objectives" / "Operational Governance.md").write_text(
        "# Operational Governance\n"
        "Type: Objective\n"
        "Status: Supported\n"
        "Last Activity: 2026-07-01\n"
    )
    (vault / "03 Projects" / "Governance Programme.md").write_text(
        "# Governance Programme\n"
        "Status: Active\n"
        "Owner: Jane Smith\n"
        "[[Operational Governance]]\n"
    )
    (vault / "09 Governance" / "Decisions" / "Governance Approval.md").write_text(
        "# Governance Approval\n"
        "[[Operational Governance]]\n"
    )
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text(
        "# Follow Up Actions\n\n"
        "## Follow-Up Actions\n\n"
        "- Confirm governance checkpoint this week\n"
    )
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text(
        "# Open Loop Register\n\n"
        "## LOOP-001\n"
        "Issue: Governance decision pending\n"
        "Status: OPEN\n"
        "Priority: HIGH\n"
        "Owner: Jane Smith\n"
    )

    payload = get_dashboard_home(tmp_path / "evidence", vault_root=vault)

    assert payload["objectives"]["items"]
    item = next(item for item in payload["objectives"]["items"] if item["title"] == "Operational Governance")
    detail = payload["objectives"]["details"][item["objective_id"]]

    assert item["title"] == "Operational Governance"
    assert item["route"].startswith("/objectives/")
    assert item["supporting_project_count"] >= 1
    assert "current_status" in detail
    assert "smart_assessment" in detail
    assert detail["evidence_sources"]
    assert detail["provenance"]["objective"]


def test_dashboard_payload_exposes_full_followup_and_open_loop_collections(tmp_path, monkeypatch):
    from src.openloops import open_loop_intelligence as open_loop_module

    vault = tmp_path / "vault"
    (vault / "09 Governance" / "Objectives").mkdir(parents=True)
    (vault / "08 Follow Ups").mkdir(parents=True)
    (vault / "01 Daily Logs").mkdir(parents=True)

    (vault / "09 Governance" / "Objectives" / "2026 Executive Objectives.md").write_text(
        "# 2026 Executive Objectives\n\n"
        "## Objectives\n\n"
        "- Operational Governance\n"
    )
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text(
        "# Follow Up Actions\n\n"
        "## Follow-Up Actions\n\n"
        "- Complete procurement KPI update by 2026-07-13\n"
        "- Await Finance confirmation on invoice routing\n"
    )
    (vault / "01 Daily Logs" / "2026-07-10.md").write_text(
        "# 2026-07-10\n\n"
        "Follow-up: Complete procurement KPI update by 2026-07-13.\n"
        "Open loop: Await Finance confirmation on invoice routing.\n"
    )
    index = tmp_path / "daily_governance_index.json"
    index.write_text(
        """{
  "records": [
    {
      "id": "DG-20260710-OPEN_LOOP-1",
      "date": "2026-07-10",
      "type": "open_loop",
      "text": "Await Finance confirmation on invoice routing.",
      "status": "open",
      "source": "/docker/obsidian-vault/01 Daily Logs/2026-07-10.md"
    }
  ]
}"""
    )
    monkeypatch.setattr(open_loop_module, "DAILY_GOVERNANCE_INDEX", index)

    payload = get_dashboard_home(tmp_path / "evidence", vault_root=vault)

    assert payload["followups"]["counts"]["total"] >= 1
    assert len(payload["followups"]["items"]) >= 1
    assert payload["followups"]["items"][0]["title"]
    assert payload["followups"]["items"][0]["source_path"]
    assert payload["followups"]["items"][0]["evidence_paths"]
    assert payload["open_loops"]["counts"]["total"] == len(payload["open_loops"]["items"])
    if payload["open_loops"]["items"]:
        assert payload["open_loops"]["items"][0]["title"]
        assert payload["open_loops"]["items"][0]["source_path"]
        assert payload["open_loops"]["items"][0]["evidence_paths"]
    assert len(payload["followups"]["items"]) >= len(payload["daily_brief"]["followups_due_today"])


def test_dashboard_payload_preserves_full_canonical_work_item_collections(monkeypatch):
    import src.api.dashboard_api as dashboard_api_module

    followup_items = [
        FollowupItem(
            title=f"Follow-up {index}",
            path=f"01 Daily Logs/2026-07-{index:02d}.md",
            source_kind="daily_governance_index",
            due_date=None,
            priority="HIGH" if index <= 4 else "NORMAL",
            waiting_on_others=index in {2, 5, 9},
            summary=f"Follow-up item {index}.",
        )
        for index in range(1, 13)
    ]
    open_loop_items = [
        OpenLoopItem(
            title=f"Open Loop {index}",
            path=f"01 Daily Logs/2026-07-{index:02d}.md",
            source_kind="daily_governance_index",
            status="OPEN",
            priority="HIGH" if index <= 5 else "MEDIUM",
            owner="Unknown" if index % 3 == 0 else "Jane Smith",
            summary=f"Open loop item {index}.",
        )
        for index in range(1, 12)
    ]

    followups = FollowupIntelligence(
        generated_at="2026-07-11T00:00:00Z",
        followup_count=len(followup_items),
        overdue=followup_items[:1],
        due_today=followup_items[1:2],
        due_this_week=followup_items[2:5],
        waiting_on_others=[followup_items[1], followup_items[4], followup_items[8]],
        high_priority=followup_items[:4],
        recommendations=[],
        executive_summary=[],
        all_items=followup_items,
    )
    open_loops = OpenLoopIntelligence(
        generated_at="2026-07-11T00:00:00Z",
        open_loop_count=len(open_loop_items),
        critical_open_loops=open_loop_items[:5],
        waiting_for=open_loop_items[:4],
        stalled_projects=open_loop_items[4:6],
        missing_decisions=open_loop_items[6:8],
        missing_owners=[item for item in open_loop_items if item.owner == "Unknown"],
        recommended_actions=[],
        executive_summary=[],
        all_items=open_loop_items,
    )

    state = SimpleNamespace(
        followups=followups,
        open_loops=open_loops,
        work_items=(),
        confidence="HIGH",
        canonical_entities=(),
        objectives=(),
        projects=(),
        companies=(),
        people=(),
        meetings=(),
        decisions=(),
        policies=(),
        risks=(),
        board=SimpleNamespace(
            registry_summary=(),
            board_members=(),
            weekly_board_meeting=(),
            monthly_board_meeting=(),
            standing_agenda=(),
        ),
        engine_result={"health": {"status": "GREEN", "score": 95}},
        objective_health={"total": 0, "supported": 0, "at_risk": 0, "watch": 0},
        project_health={"total": 0, "supported": 0, "at_risk": 0, "watch": 0},
        recommendations=(),
        relationship_graph=SimpleNamespace(statistics={"node_count": 0, "edge_count": 0}),
        summary=(),
        priorities=(),
        suppliers=(),
        vault={},
        entities=(),
        neighbours={},
        knowledge_model=SimpleNamespace(confidence="HIGH"),
    )
    read_model = SimpleNamespace(
        open_loops=open_loops,
        followups=followups,
        meetings=(),
        work_items=(),
        entities=(),
        evidence_summaries={},
    )
    reasoning = SimpleNamespace(
        overall_health="GREEN",
        confidence="HIGH",
        top_actions=[],
        intents=[],
        key_themes=[],
        risks_requiring_immediate_attention=[],
        decisions_required=[],
    )
    presentation = SimpleNamespace(
        confidence="HIGH",
        sections={
            "risks": SimpleNamespace(items=()),
            "recommended_actions": SimpleNamespace(items=()),
            "priorities": SimpleNamespace(items=()),
            "meetings": SimpleNamespace(items=()),
            "followups": SimpleNamespace(items=()),
        },
    )
    brief = SimpleNamespace(
        executive_health=[],
        overnight_changes=[],
        top_three_priorities=[],
        meetings_requiring_preparation=[],
        followups_due_today=[item.summary for item in followup_items[:3]],
        open_loops_blocking_progress=[item.summary for item in open_loop_items[:3]],
        risks_escalating=[],
        decisions_awaiting_you=[],
        recommended_agenda=[],
        one_page_executive_summary=[],
        confidence="HIGH",
    )

    monkeypatch.setattr(dashboard_api_module, "build_executive_state", lambda *args, **kwargs: state)
    monkeypatch.setattr(dashboard_api_module, "build_unified_executive_read_model", lambda *_args, **_kwargs: read_model)
    monkeypatch.setattr(dashboard_api_module, "build_executive_reasoning_from_state", lambda *_args, **_kwargs: reasoning)
    monkeypatch.setattr(dashboard_api_module, "build_daily_brief_from_state", lambda *_args, **_kwargs: brief)
    monkeypatch.setattr(dashboard_api_module, "build_executive_presentation_from_state", lambda *_args, **_kwargs: presentation)
    monkeypatch.setattr(dashboard_api_module, "_build_objectives_page", lambda *_args, **_kwargs: {"health": {}, "items": [], "summary": []})
    monkeypatch.setattr(dashboard_api_module, "_build_projects_page", lambda *_args, **_kwargs: {"health": {}, "items": [], "summary": []})
    monkeypatch.setattr(dashboard_api_module, "_build_meetings_page", lambda *_args, **_kwargs: {"subject": "No active meeting identified.", "executive_summary": [], "related_people": [], "related_projects": [], "related_companies": [], "related_objectives": [], "related_decisions": [], "risks": [], "open_loops": [], "follow_ups": [], "recommended_discussion": [], "confidence": "LOW"})
    monkeypatch.setattr(dashboard_api_module, "_build_board_page", lambda *_args, **_kwargs: {"summary": [], "members": [], "weekly_meeting": [], "monthly_meeting": [], "standing_agenda": []})
    monkeypatch.setattr(dashboard_api_module, "_build_ask_alfred_page", lambda *_args, **_kwargs: {"questions": [], "responses": []})
    monkeypatch.setattr(dashboard_api_module, "_build_knowledge_page", lambda *_args, **_kwargs: {"summary": [], "entity_counts": {}, "graph": {"node_count": 0, "edge_count": 0, "top_nodes": []}})
    monkeypatch.setattr(dashboard_api_module, "_build_admin_configuration_page", lambda *_args, **_kwargs: {"overview": {"environment_score": 100, "overall_health": "GREEN", "architecture_rule": "", "summary_lines": []}, "sections": {"core_configuration": [], "vault": [], "ai_providers": [], "knowledge_sources": [], "runtime": [], "services": [], "security": [], "diagnostics": [], "deployment": [], "required_actions": []}, "auto_configured": {}, "doctor_summary": {"environment_score": 100, "healthy": [], "warnings": [], "disabled": [], "recommended_actions": [], "summary_lines": []}, "actions": []})

    payload = get_dashboard_home(Path("evidence/alfred-inventory"))

    assert payload["followups"]["counts"]["total"] == 12
    assert len(payload["followups"]["items"]) == 12
    assert payload["followups"]["items"][-1]["work_item_id"].startswith("follow_up::")
    assert len(payload["daily_brief"]["followups_due_today"]) == 3
    assert payload["open_loops"]["counts"]["total"] == 11
    assert len(payload["open_loops"]["items"]) == 11
    assert payload["open_loops"]["items"][-1]["work_item_id"].startswith("open_loop::")
    assert len(payload["daily_brief"]["open_loops_blocking_progress"]) == 3
