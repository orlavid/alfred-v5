from pathlib import Path

from src.alfred.ask import ask_alfred_from_state
from src.daily.daily_brief import build_daily_brief_from_state
from src.executive.executive_intelligence import ExecutiveIntelligence, ExecutiveLineItem, build_executive_intelligence_from_state
from src.executive.executive_reasoning import build_executive_reasoning_from_state
from src.executive.executive_state import ExecutiveState, build_executive_state
from src.executive.intent_contract import build_executive_intents, build_executive_intents_from_state
from src.executive.read_model import build_unified_executive_read_model
from src.followups.followup_intelligence import FollowupIntelligence, FollowupItem
from src.openloops.open_loop_intelligence import OpenLoopIntelligence


def test_identical_evidence_produces_stable_intents(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")

    first = build_executive_intents_from_state(state)
    second = build_executive_intents_from_state(state)

    assert [item.intent_id for item in first] == [item.intent_id for item in second]
    assert [item.recommended_action for item in first] == [item.recommended_action for item in second]


def test_multiple_consumers_receive_identical_intents(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")

    expected = build_executive_intents_from_state(state)
    reasoning = build_executive_reasoning_from_state(state)
    brief = build_daily_brief_from_state(state, reasoning=reasoning)
    response = ask_alfred_from_state("What should I do today?", state)

    assert tuple(item.intent_id for item in reasoning.intents) == tuple(item.intent_id for item in expected)
    assert brief.top_three_priorities[0] == expected[0].recommended_action
    assert response.recommended_next_actions[0] == expected[0].recommended_action


def test_intent_provenance_survives(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault)

    intents = build_executive_intents_from_state(state)
    assert any(intent.evidence_paths for intent in intents)
    followup_intent = next(intent for intent in intents if "Follow up" in intent.recommended_action or "follow-up" in intent.recommended_action.lower())

    assert "evidence_paths" in followup_intent.provenance
    assert "08 Follow Ups/Follow Up Actions.md" in followup_intent.evidence_paths


def test_duplicate_intents_are_merged():
    state = ExecutiveState(
        followups=FollowupIntelligence(
            generated_at="2026-07-08T00:00:00+00:00",
            followup_count=1,
            overdue=[],
            due_today=[],
            due_this_week=[],
            waiting_on_others=[],
            high_priority=[],
            recommendations=["Close the dated follow-up with Acme Capital."],
            executive_summary=[],
        ),
        open_loops=OpenLoopIntelligence(
            generated_at="2026-07-08T00:00:00+00:00",
            open_loop_count=0,
            critical_open_loops=[],
            waiting_for=[],
            stalled_projects=[],
            missing_decisions=[],
            missing_owners=[],
            recommended_actions=[],
            executive_summary=[],
        ),
    )
    read_model = build_unified_executive_read_model(state)
    intelligence = ExecutiveIntelligence(
        executive_health=[],
        top_priorities=[],
        objectives_requiring_attention=[],
        critical_meetings=[],
        projects_at_risk=[],
        followups_requiring_action=[],
        open_loops=[],
        key_people=[],
        supplier_risks=[],
        decisions_awaiting_attention=[],
        recommended_actions_today=["Close the dated follow-up with Acme Capital."],
        executive_summary=[],
    )

    intents = build_executive_intents(read_model, intelligence)

    assert len(intents) == 1
    assert intents[0].recommended_action == "Close the dated follow-up with Acme Capital."
    assert intents[0].intent_type == "recommendation"


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
