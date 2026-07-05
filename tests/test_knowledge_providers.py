from datetime import date
from pathlib import Path

from src.executive.executive_state import build_executive_state
from src.knowledge.executive_knowledge_builder import build_executive_knowledge
from src.knowledge.providers import extract_provider_entities
from src.knowledge.providers.obsidian_provider import load_obsidian_notes


def test_providers_extract_from_obsidian_style_folders(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")

    notes = load_obsidian_notes(vault)
    entities = extract_provider_entities(vault)

    assert any(note.kind == "objective" for note in notes)
    assert any(note.kind == "project" for note in notes)
    assert any(note.kind == "daily_log" for note in notes)
    assert any(entity.type == "objective" and entity.title == "Objective Alpha" for entity in entities)
    assert any(entity.type == "project" and entity.title == "Project Phoenix" for entity in entities)
    assert any(entity.type == "daily_log" and entity.title == "2026-07-04 Daily" for entity in entities)


def test_engineering_artefacts_are_ignored_for_live_knowledge(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    (vault / "output").mkdir()
    (vault / "output" / "Objective Fake.md").write_text("# Objective Fake\nShould be ignored.\n")
    (vault / "docs" / "migration").mkdir(parents=True)
    (vault / "docs" / "migration" / "Project Fake.md").write_text("# Project Fake\nShould be ignored.\n")
    (vault / "analysis").mkdir()
    (vault / "analysis" / "Risk Fake.md").write_text("# Risk Fake\nShould be ignored.\n")

    report = build_executive_knowledge(vault_root=vault, today=date(2026, 7, 4))
    titles = {entity.title for entity in report.entities}

    assert "Objective Alpha" in titles
    assert "Project Phoenix" in titles
    assert "Objective Fake" not in titles
    assert "Project Fake" not in titles
    assert "Risk Fake" not in titles


def test_fallback_inventory_mode_does_not_contaminate_executive_state(tmp_path: Path):
    evidence_root = tmp_path / "evidence"
    evidence_root.mkdir()
    (evidence_root / "Objectives.md").write_text("# Objectives\nStrategic objective with [[Project Alpha]].\n")
    (evidence_root / "Project Alpha.md").write_text("# Project Alpha\nProgramme initiative.\n")

    state = build_executive_state(evidence_root, vault_root=tmp_path / "missing-vault")

    assert state.knowledge_model is not None
    assert state.knowledge_model.source_mode == "evidence_inventory"
    assert state.knowledge_model.entity_inventory["objective"] >= 1
    assert state.knowledge_model.entity_inventory["project"] >= 1
    assert state.objectives == ()
    assert state.projects == ()


def test_domain_providers_extract_independently(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")

    objectives = extract_provider_entities(vault, domains=("objectives",))
    projects = extract_provider_entities(vault, domains=("projects",))
    followups = extract_provider_entities(vault, domains=("followups",))
    open_loops = extract_provider_entities(vault, domains=("open_loops",))

    assert len(objectives) == 1
    assert all(entity.type == "objective" for entity in objectives)
    assert len(projects) == 1
    assert all(entity.type == "project" for entity in projects)
    assert len(followups) == 1
    assert all(entity.type == "follow_up" for entity in followups)
    assert len(open_loops) == 1
    assert all(entity.type == "open_loop" for entity in open_loops)


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
    (vault / "03 Projects" / "Project Phoenix.md").write_text("# Project Phoenix\n[[Objective Alpha]] [[Jane Smith]].\n")
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\nOwner.\n")
    (vault / "04 Companies" / "Barclays.md").write_text("# Barclays\nSupplier.\n")
    (vault / "04 Decisions" / "Decision 1.md").write_text("# Decision 1\nApprove.\n")
    (vault / "05 Meetings" / "Barclays Meeting.md").write_text("# Barclays Meeting\nAgenda.\n")
    (vault / "06 Risks" / "Risk Register.md").write_text("# Risk Register\nEscalation.\n")
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text("## LOOP-1\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\nIssue: Await approval.\n")
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text("## Follow-Up Actions\n- Follow up with Barclays today.\n")
    (vault / "01 Daily Logs" / "2026-07-04 Daily.md").write_text("# 2026-07-04 Daily\nReviewed [[Project Phoenix]].\n")
    (vault / "10 Briefings" / "Weekly Executive Briefing.md").write_text("# Weekly Executive Briefing\nExecutive briefing.\n")
    return vault
