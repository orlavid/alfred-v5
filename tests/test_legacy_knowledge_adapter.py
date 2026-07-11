from pathlib import Path

from src.api.dashboard_api import get_dashboard_home
from src.alfred.ask import ask_alfred
from src.executive.executive_state import build_executive_state
from src.knowledge.providers.legacy_adapter import build_legacy_knowledge_adapter


def test_legacy_adapter_wraps_existing_retrieval_behaviour(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    adapter = build_legacy_knowledge_adapter(Path("evidence/alfred-inventory"), vault_root=vault)

    assert len(adapter.get_objectives()) == 1
    assert adapter.get_objectives()[0].title == "Objective Alpha"
    assert len(adapter.get_projects()) == 1
    assert adapter.get_projects()[0].title == "Project Phoenix"
    assert len(adapter.get_people()) == 1
    assert adapter.get_people()[0].title == "Jane Smith"
    assert len(adapter.get_decisions()) == 1
    assert adapter.get_decisions()[0]["title"] == "Decision 1"
    assert isinstance(adapter.get_risks(), tuple)
    assert adapter.get_open_loops().open_loop_count >= 1


def test_legacy_adapter_supports_entity_lookup_and_note_search(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    adapter = build_legacy_knowledge_adapter(Path("evidence/alfred-inventory"), vault_root=vault)

    assert adapter.get_project("Project Phoenix").title == "Project Phoenix"
    assert adapter.get_person("Jane Smith").title == "Jane Smith"
    assert adapter.get_company("Acme Capital").title == "Acme Capital"

    search_results = adapter.search("Project Phoenix")
    semantic_results = adapter.semantic_search("Objective Alpha")

    assert search_results
    assert search_results[0]["source_note"].endswith(".md")
    assert "Project Phoenix" in search_results[0]["title"]
    assert semantic_results
    assert any(item["semantic_match"] for item in semantic_results)


def test_executive_state_uses_legacy_adapter_factory(tmp_path: Path, monkeypatch):
    vault = _build_obsidian_vault(tmp_path / "vault")
    calls = {"count": 0}

    from src.knowledge.providers import legacy_adapter as legacy_module
    from src.executive import executive_state as executive_state_module

    real_builder = legacy_module.build_legacy_knowledge_adapter

    def tracking_builder(evidence_root: Path, *, vault_root: Path | None = None):
        calls["count"] += 1
        return real_builder(evidence_root, vault_root=vault_root)

    monkeypatch.setattr(executive_state_module, "build_legacy_knowledge_adapter", tracking_builder)

    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault)

    assert calls["count"] == 1
    assert state.adapter is not None
    assert state.objectives[0].title == "Objective Alpha"
    assert state.projects[0].title == "Project Phoenix"


def test_executive_state_matches_legacy_adapter_output(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    evidence_root = Path("evidence/alfred-inventory")

    adapter = build_legacy_knowledge_adapter(evidence_root, vault_root=vault)
    state = build_executive_state(evidence_root, vault_root=vault)

    assert tuple(item.title for item in state.objectives) == tuple(item.title for item in adapter.get_objectives())
    assert tuple(item.title for item in state.projects) == tuple(item.title for item in adapter.get_projects())
    assert tuple(item.title for item in state.people) == tuple(item.title for item in adapter.get_people())
    assert tuple(item.title for item in state.companies) == tuple(item.title for item in adapter.get_companies())
    assert tuple(item["title"] for item in state.decisions) == tuple(item["title"] for item in adapter.get_decisions())
    assert len(state.followups.overdue) == len(adapter.get_followups().overdue)
    assert len(state.followups.high_priority) == len(adapter.get_followups().high_priority)
    assert len(state.open_loops.critical_open_loops) == len(adapter.get_open_loops().critical_open_loops)


def test_executive_state_defaults_to_legacy_adapter_provider(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault)

    assert state.adapter is not None
    assert state.adapter.__class__.__name__ == "LegacyKnowledgeAdapter"


def test_executive_state_only_consumes_configured_provider(tmp_path: Path, monkeypatch):
    vault = _build_obsidian_vault(tmp_path / "vault")

    from src.executive import executive_state as executive_state_module

    class FakeRegistry:
        default_knowledge_provider = "unsupported_provider"

    monkeypatch.setattr(executive_state_module, "build_configuration_registry", lambda **_: FakeRegistry())

    try:
        build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault)
    except ValueError as exc:
        assert "Unsupported knowledge provider" in str(exc)
    else:
        raise AssertionError("build_executive_state should reject unsupported configured providers")


def test_executive_state_uses_configured_vault_when_no_explicit_vault_root(tmp_path: Path, monkeypatch):
    vault = _build_obsidian_vault(tmp_path / "vault")
    install_root = tmp_path / "opt" / "alfred"
    app_root = install_root / "app"
    config_dir = install_root / "config"

    app_root.mkdir(parents=True)
    config_dir.mkdir(parents=True)
    config_dir.joinpath("config.yaml").write_text(
        f"""deployment:
  profile: VPS
paths:
  install_root: {install_root}
  app: {app_root}
  vault: {vault}
python:
  executable: /opt/alfred/.venv/bin/python
"""
    )

    monkeypatch.delenv("ALFRED_LIVE_VAULT_PATH", raising=False)
    monkeypatch.delenv("ALFRED_OBSIDIAN_VAULT", raising=False)
    monkeypatch.delenv("ALFRED_CONFIG_FILE", raising=False)
    monkeypatch.setenv("ALFRED_INSTALL_ROOT", str(install_root))

    state = build_executive_state(Path("evidence/alfred-inventory"))

    assert state.knowledge_model.source_mode == "live_vault"
    assert len(state.objectives) == 1
    assert len(state.projects) == 1


def test_ask_alfred_uses_configured_vault_when_no_explicit_vault_root(tmp_path: Path, monkeypatch):
    vault = _build_obsidian_vault(tmp_path / "vault")
    install_root = tmp_path / "opt" / "alfred"
    app_root = install_root / "app"
    config_dir = install_root / "config"

    app_root.mkdir(parents=True)
    config_dir.mkdir(parents=True)
    config_dir.joinpath("config.yaml").write_text(
        f"""deployment:
  profile: VPS
paths:
  install_root: {install_root}
  app: {app_root}
  vault: {vault}
python:
  executable: /opt/alfred/.venv/bin/python
"""
    )

    monkeypatch.delenv("ALFRED_LIVE_VAULT_PATH", raising=False)
    monkeypatch.delenv("ALFRED_OBSIDIAN_VAULT", raising=False)
    monkeypatch.delenv("ALFRED_CONFIG_FILE", raising=False)
    monkeypatch.setenv("ALFRED_INSTALL_ROOT", str(install_root))

    response = ask_alfred("What should I do today?", Path("evidence/alfred-inventory"))

    assert response.executive_answer
    assert response.executive_answer[0] != "No evidence found."
    assert response.recommended_next_actions
    assert response.recommended_next_actions[0] != "No evidence found."


def test_legacy_objective_path_excludes_monitoring_and_ai_artefacts(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    (vault / "09 Governance" / "Watchlists").mkdir(parents=True)
    (vault / "07 AI Memory" / "Strategic Synthesis").mkdir(parents=True)
    (vault / "09 Governance" / "Objectives").mkdir(parents=True)
    (vault / "09 Governance" / "Objectives" / "2026 Executive Objectives.md").write_text(
        "# 2026 Executive Objectives\n\n"
        "## Objectives\n\n"
        "1. Operational Governance\n"
        "2. Data and AI Strategies\n"
        "3. Risk Management\n"
        "4. Employee Development\n"
        "5. Cost Management\n"
        "6. Performance and Value Realisation\n"
    )

    (vault / "09 Governance" / "Watchlists" / "2026-05-29 Watchlist - strategic_drift.md").write_text(
        "# 2026-05-29 Watchlist - strategic_drift\nObjective: monitor strategic drift.\n"
    )
    (vault / "09 Governance" / "Objectives" / "2026-05-28 Open Loop - platform_resilience.md").write_text(
        "# 2026-05-28 Open Loop - platform_resilience\nObjective: unblock platform resilience work.\n"
    )
    (vault / "07 AI Memory" / "Strategic Synthesis" / "Strategic Memory Synthesis.md").write_text(
        "# Strategic Memory Synthesis\nObjective: summarise the historical record.\n"
    )
    adapter = build_legacy_knowledge_adapter(Path("evidence/alfred-inventory"), vault_root=vault)
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault)
    dashboard = get_dashboard_home(Path("evidence/alfred-inventory"), vault_root=vault)
    objective_titles = [item.title for item in adapter.get_objectives()]
    state_titles = [item.title for item in state.objectives]
    dashboard_titles = [item["title"] for item in dashboard["objectives"]["items"]]
    assert objective_titles == [
        "Cost Management",
        "Data and AI Strategies",
        "Employee Development",
        "Objective Alpha",
        "Operational Governance",
        "Performance and Value Realisation",
        "Risk Management",
    ]
    assert state_titles == objective_titles
    assert dashboard_titles == objective_titles


def _build_obsidian_vault(vault: Path) -> Path:
    (vault / "01 Daily Logs").mkdir(parents=True)
    (vault / "02 People").mkdir(parents=True)
    (vault / "03 Projects").mkdir(parents=True)
    (vault / "04 Companies").mkdir(parents=True)
    (vault / "04 Decisions").mkdir(parents=True)
    (vault / "05 Meetings").mkdir(parents=True)
    (vault / "06 Risks").mkdir(parents=True)
    (vault / "07 Open Loops").mkdir(parents=True)
    (vault / "08 Follow Ups").mkdir(parents=True)
    (vault / "09 Objectives").mkdir(parents=True)
    (vault / "10 Briefings").mkdir(parents=True)
    (vault / "09 Objectives" / "Objective Alpha.md").write_text("# Objective Alpha\n[[Project Phoenix]].\n")
    (vault / "03 Projects" / "Project Phoenix.md").write_text("# Project Phoenix\n[[Objective Alpha]] [[Jane Smith]] [[Acme Capital]].\n")
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\nOwner.\n")
    (vault / "04 Companies" / "Acme Capital.md").write_text("# Acme Capital\nSupplier.\n")
    (vault / "04 Decisions" / "Decision 1.md").write_text("# Decision 1\n[[Project Phoenix]]\nApprove.\n")
    (vault / "05 Meetings" / "Project Phoenix Review.md").write_text("# Project Phoenix Review\nAgenda for [[Project Phoenix]].\n")
    (vault / "06 Risks" / "Risk Register.md").write_text("# Risk Register\nIssue with [[Project Phoenix]].\n")
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text("## LOOP-1\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\nIssue: Await approval.\n")
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text("## Follow-Up Actions\n- Follow up with Acme Capital today.\n")
    (vault / "01 Daily Logs" / "2026-07-04 Daily.md").write_text("# 2026-07-04 Daily\nReviewed [[Project Phoenix]].\n")
    (vault / "10 Briefings" / "Weekly Executive Briefing.md").write_text("# Weekly Executive Briefing\nExecutive briefing.\n")
    return vault
