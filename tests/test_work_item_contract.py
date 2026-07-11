from pathlib import Path

from src.executive.executive_state import build_executive_state
from src.executive.work_item_contract import (
    build_executive_work_items,
    project_followups_from_work_items,
    project_open_loops_from_work_items,
)
from src.knowledge.providers.legacy_adapter import build_legacy_knowledge_adapter


def test_work_items_include_followups_open_loops_and_meetings(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")

    types = {item.work_item_type for item in state.work_items}

    assert "follow_up" in types
    assert "open_loop" in types
    assert "meeting" in types


def test_work_item_missing_metadata_is_explicit(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault)

    followup = next(item for item in state.work_items if item.work_item_type == "follow_up")
    meeting = next(item for item in state.work_items if item.work_item_type == "meeting")

    assert "owner" in followup.missing_fields
    assert "status" in followup.missing_fields
    assert "due_date" not in followup.missing_fields
    assert "owner" in meeting.missing_fields
    assert "priority" in meeting.missing_fields


def test_work_item_evidence_paths_survive_transformation(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    adapter = build_legacy_knowledge_adapter(Path("evidence/alfred-inventory"), vault_root=vault)

    items = build_executive_work_items(
        followups=adapter.get_followups(),
        open_loops=adapter.get_open_loops(),
        meetings=(),
    )

    followup = next(item for item in items if item.work_item_type == "follow_up")
    open_loop = next(item for item in items if item.work_item_type == "open_loop")

    assert followup.evidence_paths == ("08 Follow Ups/Follow Up Actions.md",)
    assert open_loop.evidence_paths == ("07 Open Loops/Open Loop Register.md",)
    assert followup.provenance["due_date"] == ("08 Follow Ups/Follow Up Actions.md",)
    assert open_loop.provenance["owner"] == ("07 Open Loops/Open Loop Register.md",)


def test_compatibility_projections_preserve_existing_followup_and_open_loop_surfaces(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    adapter = build_legacy_knowledge_adapter(Path("evidence/alfred-inventory"), vault_root=vault)

    items = build_executive_work_items(
        followups=adapter.get_followups(),
        open_loops=adapter.get_open_loops(),
        meetings=(),
    )
    followups = project_followups_from_work_items(items, adapter.get_followups())
    open_loops = project_open_loops_from_work_items(items, adapter.get_open_loops())

    assert len(followups.overdue) == len(adapter.get_followups().overdue)
    assert len(followups.high_priority) == len(adapter.get_followups().high_priority)
    assert len(open_loops.critical_open_loops) == len(adapter.get_open_loops().critical_open_loops)
    assert len(open_loops.missing_decisions) == len(adapter.get_open_loops().missing_decisions)
    assert len(followups.all_items) == adapter.get_followups().followup_count
    assert len(open_loops.all_items) == adapter.get_open_loops().open_loop_count


def test_work_items_support_existing_action_consumers(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")

    assert any(item.work_item_type == "follow_up" and item.due_date is not None for item in state.work_items)
    assert any(item.work_item_type == "open_loop" and item.status is not None for item in state.work_items)
    assert any(item.work_item_type == "meeting" and item.evidence_count >= 1 for item in state.work_items)


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
