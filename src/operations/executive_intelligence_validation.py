"""Behavioural certification for Alfred's executive intelligence."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
import json

from src.alfred.ask import ask_alfred_from_state
from src.api.dashboard_api import get_dashboard_home
from src.daily.daily_brief import DailyBrief, build_daily_brief_from_state
from src.executive.executive_reasoning import ExecutiveReasoning, build_executive_reasoning_from_state
from src.executive.executive_state import ExecutiveState, build_executive_state
from src.executive.presentation_contract import ExecutivePresentationContract, build_executive_presentation_from_state
from src.executive.read_model import UnifiedExecutiveReadModel, build_unified_executive_read_model
from src.knowledge.executive_knowledge_builder import DEFAULT_EVIDENCE_ROOT
from src.obsidian.live_vault import detect_live_vault_status
from src.operations.config_registry import build_configuration_registry

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
MARKDOWN_REPORT = OUT / "Executive_Intelligence_Validation.md"
JSON_REPORT = OUT / "Executive_Intelligence_Validation.json"


@dataclass(frozen=True)
class BehaviourCriterion:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class BehaviouralScenario:
    scenario_id: str
    question: str
    evidence_inputs: tuple[str, ...]
    expected_entities: tuple[str, ...]
    expected_intents: tuple[str, ...]
    expected_presentation: dict[str, tuple[str, ...]]
    acceptance_criteria: tuple[str, ...]
    criteria: tuple[BehaviourCriterion, ...]

    @property
    def status(self) -> str:
        return "PASS" if all(item.passed for item in self.criteria) else "FAIL"


@dataclass(frozen=True)
class BehaviouralCoverageMetrics:
    scenarios_total: int
    scenarios_passed: int
    criteria_total: int
    criteria_passed: int
    entity_expectations: int
    intent_expectations: int
    presentation_expectations: int


@dataclass(frozen=True)
class ExecutiveIntelligenceValidationReport:
    overall_status: str
    vault_mode: str
    vault_path: str
    markdown_files_processed: int
    first_behavioural_issue: str | None
    metrics: BehaviouralCoverageMetrics
    scenarios: tuple[BehaviouralScenario, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "overall_status": self.overall_status,
            "vault_mode": self.vault_mode,
            "vault_path": self.vault_path,
            "markdown_files_processed": self.markdown_files_processed,
            "first_behavioural_issue": self.first_behavioural_issue,
            "metrics": asdict(self.metrics),
            "scenarios": [
                {
                    "scenario_id": scenario.scenario_id,
                    "status": scenario.status,
                    "question": scenario.question,
                    "evidence_inputs": list(scenario.evidence_inputs),
                    "expected_entities": list(scenario.expected_entities),
                    "expected_intents": list(scenario.expected_intents),
                    "expected_presentation": {
                        key: list(value) for key, value in scenario.expected_presentation.items()
                    },
                    "acceptance_criteria": list(scenario.acceptance_criteria),
                    "criteria": [asdict(item) for item in scenario.criteria],
                }
                for scenario in self.scenarios
            ],
        }


@dataclass(frozen=True)
class _ScenarioContext:
    state: ExecutiveState
    read_model: UnifiedExecutiveReadModel
    reasoning: ExecutiveReasoning
    presentation: ExecutivePresentationContract
    brief: DailyBrief
    dashboard: dict[str, object]


def build_executive_intelligence_validation(
    *,
    evidence_root: Path | None = None,
    vault_root: Path | None = None,
    meeting_subject: str | None = None,
) -> ExecutiveIntelligenceValidationReport:
    effective_evidence_root = evidence_root or DEFAULT_EVIDENCE_ROOT
    configured_vault = Path(vault_root or build_configuration_registry().configured_vault_path).expanduser()
    vault_status = detect_live_vault_status(configured_vault)

    if vault_status.status == "PASS":
        context = _build_context(
            effective_evidence_root,
            configured_vault,
            meeting_subject=meeting_subject,
        )
        vault_mode = "live_vault"
        vault_path = str(configured_vault)
        markdown_files = vault_status.markdown_files_processed
    else:
        with TemporaryDirectory(prefix="alfred-behavioural-vault.") as tmpdir:
            representative_vault = _build_representative_vault(Path(tmpdir) / "vault")
            context = _build_context(
                effective_evidence_root,
                representative_vault,
                meeting_subject=meeting_subject or "Project Phoenix Review",
            )
            fallback_status = detect_live_vault_status(representative_vault)
            vault_mode = "representative_fixture"
            vault_path = str(representative_vault)
            markdown_files = fallback_status.markdown_files_processed

    scenarios = _build_scenarios(context)
    metrics = BehaviouralCoverageMetrics(
        scenarios_total=len(scenarios),
        scenarios_passed=sum(1 for item in scenarios if item.status == "PASS"),
        criteria_total=sum(len(item.criteria) for item in scenarios),
        criteria_passed=sum(sum(1 for criterion in item.criteria if criterion.passed) for item in scenarios),
        entity_expectations=sum(len(item.expected_entities) for item in scenarios),
        intent_expectations=sum(len(item.expected_intents) for item in scenarios),
        presentation_expectations=sum(sum(len(value) for value in item.expected_presentation.values()) for item in scenarios),
    )
    first_issue = next(
        (
            f"{scenario.scenario_id}: {criterion.name} - {criterion.detail}"
            for scenario in scenarios
            for criterion in scenario.criteria
            if not criterion.passed
        ),
        None,
    )
    overall_status = "GREEN" if first_issue is None else "RED"
    return ExecutiveIntelligenceValidationReport(
        overall_status=overall_status,
        vault_mode=vault_mode,
        vault_path=vault_path,
        markdown_files_processed=markdown_files,
        first_behavioural_issue=first_issue,
        metrics=metrics,
        scenarios=scenarios,
    )


def render_executive_intelligence_validation(report: ExecutiveIntelligenceValidationReport) -> str:
    lines = [
        "# Executive Intelligence Validation",
        "",
        f"- Overall Status: {report.overall_status}",
        f"- Vault Mode: {report.vault_mode}",
        f"- Vault Path: {report.vault_path}",
        f"- Markdown Files Processed: {report.markdown_files_processed}",
        f"- First Behavioural Issue: {report.first_behavioural_issue or 'None'}",
        "",
        "## Coverage Metrics",
        "",
        f"- Scenarios: {report.metrics.scenarios_passed} / {report.metrics.scenarios_total}",
        f"- Criteria: {report.metrics.criteria_passed} / {report.metrics.criteria_total}",
        f"- Entity Expectations: {report.metrics.entity_expectations}",
        f"- Intent Expectations: {report.metrics.intent_expectations}",
        f"- Presentation Expectations: {report.metrics.presentation_expectations}",
        "",
        "## Scenarios",
        "",
    ]
    for scenario in report.scenarios:
        lines.extend(
            [
                f"### {scenario.scenario_id}",
                "",
                f"- Status: {scenario.status}",
                f"- Question: {scenario.question}",
                f"- Evidence Inputs: {', '.join(scenario.evidence_inputs) if scenario.evidence_inputs else 'none'}",
                f"- Expected Entities: {', '.join(scenario.expected_entities) if scenario.expected_entities else 'none'}",
                f"- Expected Intents: {', '.join(scenario.expected_intents) if scenario.expected_intents else 'none'}",
                f"- Acceptance Criteria: {', '.join(scenario.acceptance_criteria)}",
                "",
                "| Criterion | Status | Detail |",
                "| --- | --- | --- |",
            ]
        )
        for criterion in scenario.criteria:
            lines.append(f"| {criterion.name} | {'PASS' if criterion.passed else 'FAIL'} | {criterion.detail} |")
        lines.append("")
    return "\n".join(lines)


def render_executive_intelligence_validation_json(report: ExecutiveIntelligenceValidationReport) -> str:
    return json.dumps(report.as_dict(), indent=2, sort_keys=True)


def write_executive_intelligence_validation(
    report: ExecutiveIntelligenceValidationReport,
) -> tuple[Path, Path]:
    OUT.mkdir(parents=True, exist_ok=True)
    MARKDOWN_REPORT.write_text(render_executive_intelligence_validation(report))
    JSON_REPORT.write_text(render_executive_intelligence_validation_json(report))
    return MARKDOWN_REPORT, JSON_REPORT


def _build_context(
    evidence_root: Path,
    vault_root: Path,
    *,
    meeting_subject: str | None,
) -> _ScenarioContext:
    state = build_executive_state(
        evidence_root,
        vault_root=vault_root,
        meeting_subject=meeting_subject,
    )
    read_model = build_unified_executive_read_model(state)
    reasoning = build_executive_reasoning_from_state(state)
    presentation = build_executive_presentation_from_state(state, reasoning=reasoning, read_model=read_model)
    brief = build_daily_brief_from_state(state, reasoning=reasoning)
    dashboard = get_dashboard_home(
        evidence_root,
        meeting_subject=meeting_subject,
        vault_root=vault_root,
    )
    return _ScenarioContext(
        state=state,
        read_model=read_model,
        reasoning=reasoning,
        presentation=presentation,
        brief=brief,
        dashboard=dashboard,
    )


def _build_scenarios(context: _ScenarioContext) -> tuple[BehaviouralScenario, ...]:
    return (
        _scenario_today(context),
        _scenario_riskiest_objectives(context),
        _scenario_suppliers(context),
        _scenario_meetings(context),
        _scenario_followups(context),
        _scenario_decisions(context),
        _scenario_changes_since_yesterday(context),
        _scenario_daily_brief(context),
        _scenario_dashboard(context),
    )


def _scenario_today(context: _ScenarioContext) -> BehaviouralScenario:
    response = ask_alfred_from_state("What should Phillip do today?", context.state)
    top_intent = context.reasoning.intents[0]
    expected_entities = _names_for_ids(context, top_intent.source_entities)
    expected_presentation = {
        "recommended_actions": (context.presentation.sections["recommended_actions"].items[0].title,),
        "priorities": (context.presentation.sections["priorities"].items[0].title,),
    }
    criteria = (
        _criterion_contains("Ask Alfred top recommendation", response.recommended_next_actions, top_intent.recommended_action),
        _criterion_contains("Dashboard next best action", (context.dashboard["next_best_action"]["action"],), top_intent.recommended_action),
        _criterion_contains("Daily Brief top priorities", tuple(context.brief.top_three_priorities), context.presentation.sections["priorities"].items[0].title),
        _criterion_bool(
            "Expected entity appears in today narrative",
            True,
            "No explicit source entity was attached to the top intent.",
        )
        if not expected_entities
        else _criterion_any_entity("Expected entity appears in today narrative", response.executive_answer + response.supporting_evidence, expected_entities),
    )
    return BehaviouralScenario(
        scenario_id="what-should-phillip-do-today",
        question="What should Phillip do today?",
        evidence_inputs=top_intent.evidence_paths,
        expected_entities=expected_entities,
        expected_intents=(top_intent.recommended_action,),
        expected_presentation=expected_presentation,
        acceptance_criteria=(
            "Ask Alfred and dashboard agree on the top evidence-backed intent.",
            "Daily Brief surfaces the same top priority.",
            "At least one source entity remains visible in the answer or evidence.",
        ),
        criteria=criteria,
    )


def _scenario_riskiest_objectives(context: _ScenarioContext) -> BehaviouralScenario:
    top_objective = context.dashboard["objectives"]["items"][0] if context.dashboard["objectives"]["items"] else None
    objective_title = top_objective["title"] if top_objective else ""
    criteria = (
        _criterion_bool(
            "Objective page contains a risk-bearing objective",
            bool(top_objective),
            objective_title or "No objective surfaced on the dashboard objectives page.",
        ),
        _criterion_contains(
            "Presentation objectives include the same objective",
            tuple(item.title for item in context.presentation.sections["objectives"].items),
            objective_title,
        ),
        _criterion_contains(
            "Objective risk remains visible in dashboard summary",
            tuple(item["recommended_next_action"] for item in context.dashboard["objectives"]["items"]),
            top_objective["recommended_next_action"] if top_objective else "",
        ),
    )
    return BehaviouralScenario(
        scenario_id="highest-risk-objectives",
        question="What are the highest-risk objectives?",
        evidence_inputs=(objective_title,) if objective_title else (),
        expected_entities=(objective_title,) if objective_title else (),
        expected_intents=(),
        expected_presentation={"objectives": (objective_title,) if objective_title else ()},
        acceptance_criteria=(
            "Objectives remain visible on the dashboard objective surface.",
            "Presentation objectives stay aligned with dashboard objectives.",
        ),
        criteria=criteria,
    )


def _scenario_suppliers(context: _ScenarioContext) -> BehaviouralScenario:
    response = ask_alfred_from_state("Which suppliers require attention?", context.state)
    supplier_name = context.state.suppliers[0].title if context.state.suppliers else ""
    criteria = (
        _criterion_bool(
            "Supplier risk exists in state",
            bool(supplier_name),
            supplier_name or "No supplier entity available for certification.",
        ),
        _criterion_any_entity("Ask Alfred names the supplier", response.executive_answer + response.supporting_evidence, (supplier_name,) if supplier_name else ()),
        _criterion_any_entity(
            "Canonical company entities retain the supplier",
            tuple(item.canonical_name for item in context.read_model.entities if item.entity_type == "company"),
            (supplier_name,) if supplier_name else (),
        ),
    )
    return BehaviouralScenario(
        scenario_id="suppliers-requiring-attention",
        question="Which suppliers require attention?",
        evidence_inputs=(supplier_name,) if supplier_name else (),
        expected_entities=(supplier_name,) if supplier_name else (),
        expected_intents=(),
        expected_presentation={},
        acceptance_criteria=(
            "Supplier entity remains visible across Ask Alfred and dashboard company surfaces.",
        ),
        criteria=criteria,
    )


def _scenario_meetings(context: _ScenarioContext) -> BehaviouralScenario:
    response = ask_alfred_from_state("What meetings require preparation?", context.state)
    meeting_title = context.presentation.sections["meetings"].items[0].title if context.presentation.sections["meetings"].items else ""
    meeting_summary = context.presentation.sections["meetings"].items[0].summary if context.presentation.sections["meetings"].items else ""
    criteria = (
        _criterion_contains("Ask Alfred meeting answer", response.executive_answer, meeting_title),
        _criterion_contains("Daily Brief meeting preparation", tuple(context.brief.meetings_requiring_preparation), meeting_summary),
        _criterion_contains("Dashboard meeting subject", (context.dashboard["meetings"]["subject"],), meeting_title),
    )
    return BehaviouralScenario(
        scenario_id="meetings-requiring-preparation",
        question="What meetings require preparation?",
        evidence_inputs=tuple(context.presentation.sections["meetings"].items[0].evidence_paths[:3]) if context.presentation.sections["meetings"].items else (),
        expected_entities=(meeting_title,) if meeting_title else (),
        expected_intents=(meeting_summary,) if meeting_summary else (),
        expected_presentation={"meetings": (meeting_title, meeting_summary) if meeting_title else ()},
        acceptance_criteria=(
            "Meeting subject and preparation summary stay aligned across Ask Alfred, Daily Brief, and dashboard.",
        ),
        criteria=criteria,
    )


def _scenario_followups(context: _ScenarioContext) -> BehaviouralScenario:
    response = ask_alfred_from_state("Which follow-ups are overdue?", context.state)
    followup_title = context.presentation.sections["followups"].items[0].title if context.presentation.sections["followups"].items else ""
    criteria = (
        _criterion_contains("Ask Alfred follow-up answer", response.executive_answer + response.recommended_next_actions, followup_title),
        _criterion_contains("Daily Brief follow-ups", tuple(context.brief.followups_due_today), followup_title),
        _criterion_contains("Dashboard navigation follow-ups", (context.dashboard["navigation_priorities"][2]["reason"],), followup_title),
    )
    return BehaviouralScenario(
        scenario_id="overdue-followups",
        question="Which follow-ups are overdue?",
        evidence_inputs=(followup_title,) if followup_title else (),
        expected_entities=(followup_title,) if followup_title else (),
        expected_intents=(followup_title,) if followup_title else (),
        expected_presentation={"followups": (followup_title,) if followup_title else ()},
        acceptance_criteria=(
            "Overdue follow-up remains visible in Ask Alfred, Daily Brief, and dashboard navigation.",
        ),
        criteria=criteria,
    )


def _scenario_decisions(context: _ScenarioContext) -> BehaviouralScenario:
    response = ask_alfred_from_state("Which decisions are blocked?", context.state)
    decision_title = context.presentation.sections["decisions"].items[0].title if context.presentation.sections["decisions"].items else ""
    criteria = (
        _criterion_contains("Ask Alfred decisions answer", response.executive_answer + response.supporting_evidence, decision_title),
        _criterion_contains("Daily Brief decisions", tuple(context.brief.decisions_awaiting_you), decision_title),
        _criterion_contains("Dashboard decisions navigation", (context.dashboard["navigation_priorities"][4]["reason"],), decision_title),
    )
    return BehaviouralScenario(
        scenario_id="blocked-decisions",
        question="Which decisions are blocked?",
        evidence_inputs=(decision_title,) if decision_title else (),
        expected_entities=(decision_title,) if decision_title else (),
        expected_intents=(decision_title,) if decision_title else (),
        expected_presentation={"decisions": (decision_title,) if decision_title else ()},
        acceptance_criteria=(
            "Blocked decision remains visible in Ask Alfred, Daily Brief, and dashboard navigation.",
        ),
        criteria=criteria,
    )


def _scenario_changes_since_yesterday(context: _ScenarioContext) -> BehaviouralScenario:
    overnight = tuple(context.brief.overnight_changes)
    criteria = (
        _criterion_bool(
            "Daily Brief overnight changes is evidence-backed",
            all("No material change summary available." not in item for item in overnight[:1]),
            overnight[0] if overnight else "No overnight changes found.",
        ),
        _criterion_contains(
            "Dashboard operating picture reflects the same change narrative",
            tuple(context.dashboard["operating_picture"]["summary"]),
            context.presentation.sections["recommended_actions"].items[0].title if context.presentation.sections["recommended_actions"].items else "",
        ),
    )
    return BehaviouralScenario(
        scenario_id="changes-since-yesterday",
        question="What changed since yesterday?",
        evidence_inputs=overnight,
        expected_entities=(),
        expected_intents=(context.presentation.sections["recommended_actions"].items[0].title,) if context.presentation.sections["recommended_actions"].items else (),
        expected_presentation={"evidence_summaries": tuple(item.title for item in context.presentation.sections["evidence_summaries"].items[:3])},
        acceptance_criteria=(
            "Daily Brief and dashboard both surface a non-placeholder change narrative.",
        ),
        criteria=criteria,
    )


def _scenario_daily_brief(context: _ScenarioContext) -> BehaviouralScenario:
    criteria = (
        _criterion_contains(
            "Daily Brief top priorities align with presentation priorities",
            tuple(context.brief.top_three_priorities),
            context.presentation.sections["priorities"].items[0].title if context.presentation.sections["priorities"].items else "",
        ),
        _criterion_contains(
            "Daily Brief agenda aligns with recommended actions",
            tuple(context.brief.recommended_agenda),
            context.presentation.sections["recommended_actions"].items[0].title if context.presentation.sections["recommended_actions"].items else "",
        ),
    )
    return BehaviouralScenario(
        scenario_id="daily-brief-surface",
        question="What should appear in the Daily Brief?",
        evidence_inputs=tuple(context.brief.one_page_executive_summary[:3]),
        expected_entities=(),
        expected_intents=tuple(item.title for item in context.presentation.sections["recommended_actions"].items[:2]),
        expected_presentation={
            "priorities": tuple(item.title for item in context.presentation.sections["priorities"].items[:3]),
            "recommended_actions": tuple(item.title for item in context.presentation.sections["recommended_actions"].items[:3]),
        },
        acceptance_criteria=(
            "Daily Brief remains aligned with canonical presentation priorities and recommended actions.",
        ),
        criteria=criteria,
    )


def _scenario_dashboard(context: _ScenarioContext) -> BehaviouralScenario:
    criteria = (
        _criterion_contains(
            "Dashboard next action matches presentation",
            (context.dashboard["next_best_action"]["action"],),
            context.presentation.sections["recommended_actions"].items[0].title if context.presentation.sections["recommended_actions"].items else "",
        ),
        _criterion_contains(
            "Dashboard plan today matches presentation priorities",
            tuple(item["summary"] for item in context.dashboard["plan_today"]),
            context.presentation.sections["priorities"].items[0].title if context.presentation.sections["priorities"].items else "",
        ),
        _criterion_bool(
            "Dashboard generated_from remains ExecutiveState-backed",
            context.dashboard["generated_from"]["runtime_model"] == "ExecutiveState",
            str(context.dashboard["generated_from"]),
        ),
    )
    return BehaviouralScenario(
        scenario_id="executive-dashboard",
        question="What should be on the executive dashboard?",
        evidence_inputs=tuple(item["summary"] for item in context.dashboard["plan_today"][:3]),
        expected_entities=(),
        expected_intents=(context.dashboard["next_best_action"]["action"],),
        expected_presentation={
            "recommended_actions": tuple(item.title for item in context.presentation.sections["recommended_actions"].items[:1]),
            "priorities": tuple(item.title for item in context.presentation.sections["priorities"].items[:3]),
        },
        acceptance_criteria=(
            "Dashboard next action and plan-today cards remain aligned with the presentation contract.",
        ),
        criteria=criteria,
    )


def _criterion_contains(name: str, values: tuple[str, ...] | list[str], expected: str) -> BehaviourCriterion:
    expected_text = (expected or "").strip()
    material = tuple(str(value) for value in values if value)
    if not expected_text:
        return BehaviourCriterion(name=name, passed=False, detail="No expected value was available for this scenario.")
    passed = any(expected_text in value for value in material)
    detail = f"expected={expected_text}; observed={material[:3]}"
    return BehaviourCriterion(name=name, passed=passed, detail=detail)


def _criterion_any_entity(name: str, values: tuple[str, ...] | list[str], entities: tuple[str, ...]) -> BehaviourCriterion:
    material = " ".join(str(value) for value in values if value)
    expected = tuple(item for item in entities if item)
    if not expected:
        return BehaviourCriterion(name=name, passed=False, detail="No expected entity was available for this scenario.")
    passed = any(item in material for item in expected)
    detail = f"expected_any={expected}; observed={material[:240]}"
    return BehaviourCriterion(name=name, passed=passed, detail=detail)


def _criterion_bool(name: str, passed: bool, detail: str) -> BehaviourCriterion:
    return BehaviourCriterion(name=name, passed=passed, detail=detail)


def _names_for_ids(context: _ScenarioContext, identifiers: tuple[str, ...]) -> tuple[str, ...]:
    entity_lookup = {item.entity_id: item.canonical_name for item in context.read_model.entities}
    work_item_lookup = {item.work_item_id: item.title for item in context.read_model.work_items}
    resolved = []
    for identifier in identifiers:
        resolved.append(entity_lookup.get(identifier) or work_item_lookup.get(identifier) or identifier)
    return tuple(item for item in resolved if item)


def _build_representative_vault(vault: Path) -> Path:
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
    (vault / "09 Objectives" / "Objective Alpha.md").write_text("# Objective Alpha\nStrategic objective linked to [[Project Phoenix]].\n")
    (vault / "03 Projects" / "Project Phoenix.md").write_text("# Project Phoenix\nProgramme initiative for [[Objective Alpha]] with owner [[Jane Smith]] and supplier [[Acme Capital]].\n")
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\nOwner for [[Project Phoenix]].\n")
    (vault / "04 Companies" / "Acme Capital.md").write_text("# Acme Capital\nSupplier and company for [[Project Phoenix]].\n")
    (vault / "04 Decisions" / "Decision 1.md").write_text("# Decision 1\nApproval for [[Project Phoenix]].\n")
    (vault / "05 Meetings" / "Project Phoenix Review.md").write_text("# Project Phoenix Review\nAgenda for [[Project Phoenix]] and [[Acme Capital]].\n")
    (vault / "06 Risks" / "Risk Register.md").write_text("# Risk Register\nRisk escalation linked to [[Project Phoenix]].\n")
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text("## LOOP-1\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\nIssue: Await approval on Project Phoenix.\n")
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text("## Follow-Up Actions\n- Follow up with Acme Capital today on Project Phoenix.\n")
    (vault / "01 Daily Logs" / "2026-07-04 Daily.md").write_text("# 2026-07-04 Daily\nReviewed [[Project Phoenix]] and escalated supplier follow-up.\n")
    (vault / "10 Briefings" / "Weekly Executive Briefing.md").write_text("# Weekly Executive Briefing\nExecutive briefing for [[Project Phoenix]].\n")
    return vault
