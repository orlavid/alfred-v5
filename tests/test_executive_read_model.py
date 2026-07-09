from dataclasses import replace
from pathlib import Path

from src.alfred.ask import ask_alfred_from_state
from src.api.dashboard_api import _build_meetings_page
from src.daily.daily_brief import build_daily_brief_from_state
from src.executive.executive_intelligence import build_executive_intelligence_from_state
from src.executive.executive_reasoning import ExecutiveAction, ExecutiveReasoning
from src.executive.executive_state import ExecutiveState, build_executive_state
from src.executive.read_model import build_unified_executive_read_model
from src.followups.followup_intelligence import FollowupIntelligence, FollowupItem
from src.openloops.open_loop_intelligence import OpenLoopIntelligence


def test_read_model_exposes_canonical_entities_and_work_items(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")

    read_model = build_unified_executive_read_model(state)

    assert len(read_model.entities) == len(state.canonical_entities)
    assert len(read_model.work_items) == len(state.work_items)
    assert read_model.meetings[0].subject == state.meetings[0].subject
    expected_followup = (state.followups.due_today or state.followups.overdue or state.followups.high_priority)[0]
    actual_followup = (read_model.followups.due_today or read_model.followups.overdue or read_model.followups.high_priority)[0]
    assert actual_followup.summary == expected_followup.summary


def test_read_model_preserves_evidence_provenance(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")

    read_model = build_unified_executive_read_model(state)
    followup = next(item for item in read_model.work_items if item.work_item_type == "follow_up")
    summary = read_model.evidence_summaries[followup.work_item_id]

    assert summary.evidence_paths == ("08 Follow Ups/Follow Up Actions.md",)
    assert summary.provenance["due_date"] == ("08 Follow Ups/Follow Up Actions.md",)
    assert read_model.recency_signals[followup.work_item_id] == followup.due_date


def test_prioritisation_consumes_read_model(monkeypatch, tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault)
    base_read_model = build_unified_executive_read_model(state)
    custom_priority = {
        "title": "Treasury Objective",
        "priority": "CRITICAL",
        "priority_score": 99,
        "next_step": "Confirm owner and dated milestone",
        "status": "AT RISK",
        "owner": "Jane Smith",
        "deadline_or_recency": "2026-07-10",
        "evidence_paths": ["09 Objectives/Objective Alpha.md"],
        "confidence": "HIGH",
        "provider": "read_model_test",
    }
    monkeypatch.setattr(
        "src.executive.executive_intelligence.build_unified_executive_read_model",
        lambda _: replace(base_read_model, priorities=(custom_priority,)),
    )

    report = build_executive_intelligence_from_state(state)

    assert report.top_priorities[0].title == "Treasury Objective"
    assert "Confirm owner and dated milestone" in report.top_priorities[0].detail


def test_ask_alfred_consumes_read_model(monkeypatch):
    state = ExecutiveState(confidence="HIGH")
    read_model = replace(
        build_unified_executive_read_model(
            ExecutiveState(
                work_items=(),
                canonical_entities=(),
                recommendations=(),
                priorities=(),
                meetings=(),
                followups=FollowupIntelligence(
                    generated_at="2026-07-08T00:00:00+00:00",
                    followup_count=1,
                    overdue=[
                        FollowupItem(
                            title="Acme Capital",
                            path="08 Follow Ups/Follow Up Actions.md",
                            source_kind="project",
                            due_date="2026-07-08",
                            priority="HIGH",
                            waiting_on_others=False,
                            summary="Close the dated follow-up with Acme Capital.",
                        )
                    ],
                    due_today=[],
                    due_this_week=[],
                    waiting_on_others=[],
                    high_priority=[],
                    recommendations=[],
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
        ),
    )
    reasoning = ExecutiveReasoning(
        overall_health="GREEN (90 / 100)",
        confidence="HIGH",
        key_themes=[],
        top_actions=[
            ExecutiveAction(
                priority="HIGH",
                action="Close the dated follow-up with Acme Capital.",
                why_it_matters="A dated follow-up is overdue.",
                supporting_evidence="08 Follow Ups/Follow Up Actions.md",
                expected_impact="Clears a live dependency.",
                confidence="HIGH",
                score=90,
            )
        ],
        risks_requiring_immediate_attention=[],
        opportunities=[],
        decisions_required=[],
        recommended_agenda_for_today=[],
        executive_conclusion=[],
    )

    class IntelligenceStub:
        top_priorities = []
        recommended_actions_today = []
        supplier_risks = []
        followups_requiring_action = []
        open_loops = []

    monkeypatch.setattr("src.alfred.ask.build_unified_executive_read_model", lambda _: read_model)
    monkeypatch.setattr("src.alfred.ask.build_executive_reasoning_from_state", lambda _: reasoning)
    monkeypatch.setattr("src.alfred.ask.build_executive_intelligence_from_state", lambda _: IntelligenceStub())

    response = ask_alfred_from_state("What follow-ups are overdue?", state)

    assert response.executive_answer[0].startswith("There are 1 overdue follow-ups")
    assert response.executive_answer[1] == "Close the dated follow-up with Acme Capital."


def test_daily_brief_and_dashboard_compatibility_outputs_remain_unchanged(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    state = build_executive_state(Path("evidence/alfred-inventory"), vault_root=vault, meeting_subject="Project Phoenix Review")
    read_model = build_unified_executive_read_model(state)

    brief = build_daily_brief_from_state(state)
    meetings_page = _build_meetings_page(read_model)

    expected_followup = (state.followups.due_today or state.followups.overdue or state.followups.high_priority)[0]
    assert brief.followups_due_today[0] == expected_followup.summary
    expected_open_loop = (state.open_loops.waiting_for or state.open_loops.missing_owners)
    if expected_open_loop:
        assert brief.open_loops_blocking_progress[0] == expected_open_loop[0].summary
    else:
        assert brief.open_loops_blocking_progress[0] == "No active open loop identified."
    assert meetings_page["subject"] == state.meetings[0].subject
    assert meetings_page["recommended_discussion"] == state.meetings[0].recommended_discussion


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
