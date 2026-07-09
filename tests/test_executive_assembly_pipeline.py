from pathlib import Path
from dataclasses import FrozenInstanceError, is_dataclass

from src.api.dashboard_api import get_dashboard_home
from src.daily.daily_brief import build_daily_brief_from_state
from src.executive.executive_state import (
    ExecutiveAssemblyRequest,
    build_executive_state,
    run_entity_projection_stage,
    run_executive_assembly_pipeline,
    run_executive_state_finalisation_stage,
    run_intent_generation_stage,
    run_knowledge_acquisition_stage,
    run_presentation_generation_stage,
    run_read_model_assembly_stage,
    run_work_item_projection_stage,
)


def test_executive_assembly_pipeline_stage_ordering():
    result = run_executive_assembly_pipeline(Path("evidence/alfred-inventory"))

    assert [stage.name for stage in result.stages] == [
        "knowledge_acquisition",
        "entity_projection",
        "work_item_projection",
        "read_model_assembly",
        "intent_generation",
        "presentation_generation",
        "executive_state_finalisation",
    ]


def test_executive_assembly_pipeline_is_deterministic():
    first = run_executive_assembly_pipeline(Path("evidence/alfred-inventory"))
    second = run_executive_assembly_pipeline(Path("evidence/alfred-inventory"))

    assert first.state.summary == second.state.summary
    assert first.state.recommendations == second.state.recommendations
    assert tuple(entity.entity_id for entity in first.state.canonical_entities) == tuple(entity.entity_id for entity in second.state.canonical_entities)
    assert tuple(item.work_item_id for item in first.state.work_items) == tuple(item.work_item_id for item in second.state.work_items)


def test_identical_input_produces_identical_executive_state():
    first = build_executive_state(Path("evidence/alfred-inventory"))
    second = build_executive_state(Path("evidence/alfred-inventory"))

    assert first.summary == second.summary
    assert first.confidence == second.confidence
    assert first.recommendations == second.recommendations
    assert tuple(entity.entity_id for entity in first.canonical_entities) == tuple(entity.entity_id for entity in second.canonical_entities)


def test_executive_assembly_pipeline_exposes_stage_diagnostics():
    result = run_executive_assembly_pipeline(Path("evidence/alfred-inventory"))

    assert "knowledge_acquisition" in result.diagnostics
    assert "entity_projection" in result.diagnostics
    assert "presentation_generation" in result.diagnostics
    assert result.diagnostics["knowledge_acquisition"]["entity_count"] >= 0
    assert result.diagnostics["entity_projection"]["canonical_entity_count"] >= 0
    assert "ordered_sections" in result.diagnostics["presentation_generation"]
    assert all(stage.duration_ms >= 0 for stage in result.stages)
    assert result.stages[0].dependencies == ("request",)
    assert result.stages[0].produces == ("knowledge",)


def test_presentation_output_remains_unchanged_across_pipeline_entrypoints(tmp_path: Path):
    vault = _build_obsidian_vault(tmp_path / "vault")
    pipeline_state = run_executive_assembly_pipeline(
        Path("evidence/alfred-inventory"),
        vault_root=vault,
        meeting_subject="Project Phoenix Review",
    ).state
    direct_state = build_executive_state(
        Path("evidence/alfred-inventory"),
        vault_root=vault,
        meeting_subject="Project Phoenix Review",
    )

    pipeline_brief = build_daily_brief_from_state(pipeline_state)
    direct_brief = build_daily_brief_from_state(direct_state)
    pipeline_dashboard = get_dashboard_home(
        Path("evidence/alfred-inventory"),
        vault_root=vault,
        meeting_subject="Project Phoenix Review",
    )

    assert pipeline_brief.top_three_priorities == direct_brief.top_three_priorities
    assert pipeline_brief.followups_due_today == direct_brief.followups_due_today
    assert pipeline_brief.recommended_agenda == direct_brief.recommended_agenda
    assert pipeline_dashboard["daily_brief"]["top_three_priorities"] == direct_brief.top_three_priorities
    assert pipeline_dashboard["meetings"]["subject"] == "Project Phoenix Review"


def test_stage_contracts_are_immutable_where_practical():
    request = ExecutiveAssemblyRequest(evidence_root=Path("evidence/alfred-inventory"))
    knowledge, _ = run_knowledge_acquisition_stage(request)
    entity_projection, _ = run_entity_projection_stage(knowledge)
    work_item_projection, _ = run_work_item_projection_stage(knowledge, entity_projection)

    for value in (request, knowledge, entity_projection, work_item_projection):
        assert is_dataclass(value)
    try:
        request.evidence_root = Path("changed")
        assert False, "request should be immutable"
    except FrozenInstanceError:
        pass


def test_stages_can_be_executed_independently_and_replayed():
    request = ExecutiveAssemblyRequest(evidence_root=Path("evidence/alfred-inventory"))
    knowledge, knowledge_diag = run_knowledge_acquisition_stage(request)
    entity_projection, entity_diag = run_entity_projection_stage(knowledge)
    work_item_projection, work_item_diag = run_work_item_projection_stage(knowledge, entity_projection)
    read_model_assembly, read_model_diag = run_read_model_assembly_stage(knowledge, entity_projection, work_item_projection)
    intent_generation, intent_diag = run_intent_generation_stage(read_model_assembly)
    presentation_generation, presentation_diag = run_presentation_generation_stage(read_model_assembly, intent_generation)
    finalisation, final_diag = run_executive_state_finalisation_stage(
        knowledge,
        entity_projection,
        work_item_projection,
        presentation_generation,
    )

    pipeline = run_executive_assembly_pipeline(Path("evidence/alfred-inventory"))

    assert finalisation.state.summary == pipeline.state.summary
    assert finalisation.state.recommendations == pipeline.state.recommendations
    assert knowledge_diag["entity_count"] == pipeline.diagnostics["knowledge_acquisition"]["entity_count"]
    assert entity_diag["canonical_entity_count"] == pipeline.diagnostics["entity_projection"]["canonical_entity_count"]
    assert work_item_diag["work_item_count"] == pipeline.diagnostics["work_item_projection"]["work_item_count"]
    assert read_model_diag["entity_count"] == pipeline.diagnostics["read_model_assembly"]["entity_count"]
    assert intent_diag["intent_count"] == pipeline.diagnostics["intent_generation"]["intent_count"]
    assert presentation_diag["section_count"] == pipeline.diagnostics["presentation_generation"]["section_count"]
    assert final_diag["state_confidence"] == pipeline.diagnostics["executive_state_finalisation"]["state_confidence"]


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
