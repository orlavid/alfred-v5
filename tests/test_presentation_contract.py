from pathlib import Path

from src.alfred.ask import ask_alfred_from_state
from src.api.dashboard_api import get_dashboard_home
from src.daily.daily_brief import build_daily_brief_from_state
from src.executive.executive_reasoning import build_executive_reasoning_from_state
from src.executive.executive_state import build_executive_state
from src.executive.presentation_contract import SECTION_ORDER, build_executive_presentation_from_state
from src.executive.read_model import build_unified_executive_read_model


def test_dashboard_and_daily_brief_share_presentation_model(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")
    reasoning = build_executive_reasoning_from_state(state)
    read_model = build_unified_executive_read_model(state)
    presentation = build_executive_presentation_from_state(state, reasoning=reasoning, read_model=read_model)
    brief = build_daily_brief_from_state(state, reasoning=reasoning)
    payload = get_dashboard_home(Path("evidence/alfred-inventory"), meeting_subject="Project Phoenix Review", vault_root=vault)

    assert brief.top_three_priorities == [item.title for item in presentation.sections["priorities"].items[:3]]
    assert payload["next_best_action"]["action"] == presentation.sections["recommended_actions"].items[0].title
    assert payload["meetings"]["recommended_discussion"] == list(presentation.sections["meetings"].items[0].extensions["recommended_discussion"])


def test_ask_alfred_summaries_consume_presentation_sections(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")
    reasoning = build_executive_reasoning_from_state(state)
    read_model = build_unified_executive_read_model(state)
    presentation = build_executive_presentation_from_state(state, reasoning=reasoning, read_model=read_model)

    response = ask_alfred_from_state("What should I do today?", state)

    assert response.executive_answer[1] == presentation.sections["recommended_actions"].items[0].title
    assert response.recommended_next_actions[0] == presentation.sections["recommended_actions"].items[0].title
    if presentation.sections["recommended_actions"].items[0].evidence_paths:
        assert any(presentation.sections["recommended_actions"].items[0].evidence_paths[0] in item for item in response.supporting_evidence)


def test_presentation_ordering_is_stable(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault)

    first = build_executive_presentation_from_state(state)
    second = build_executive_presentation_from_state(state)

    assert first.ordered_sections == SECTION_ORDER
    assert second.ordered_sections == SECTION_ORDER
    assert list(first.sections) == list(second.sections)
    assert [item.item_id for item in first.sections["recommended_actions"].items] == [item.item_id for item in second.sections["recommended_actions"].items]


def test_presentation_provenance_survives(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")

    presentation = build_executive_presentation_from_state(state)
    followup = presentation.sections["followups"].items[0]
    action = presentation.sections["recommended_actions"].items[0]

    assert "due_date" in followup.provenance
    assert followup.evidence_paths
    assert "evidence_paths" in action.provenance


def test_existing_consumer_output_remains_compatible(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    payload = get_dashboard_home(Path("evidence/alfred-inventory"), meeting_subject="Project Phoenix Review", vault_root=vault)
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")
    brief = build_daily_brief_from_state(state)

    assert "top_three_priorities" in payload["daily_brief"]
    assert payload["daily_brief"]["top_three_priorities"] == brief.top_three_priorities
    assert payload["meetings"]["subject"] == "Project Phoenix Review"
    assert isinstance(payload["navigation_priorities"], list)


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
