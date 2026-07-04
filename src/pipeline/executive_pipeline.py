"""Executive knowledge refresh pipeline for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import time
from typing import Any, Callable

from executive.knowledge.extractor import extract_entities
from executive.knowledge.vault import load_vault
from src.api.dashboard_api import get_dashboard_home
from src.daily.daily_brief import build_daily_brief_from_state, render_daily_brief
from src.executive.executive_reasoning import build_executive_reasoning_from_state, render_executive_reasoning
from src.executive.executive_state import build_executive_state, render_executive_state_summary
from src.knowledge.entity_resolution import build_entity_resolution
from src.knowledge.executive_knowledge_builder import (
    DEFAULT_EVIDENCE_ROOT,
    DEFAULT_VAULT_ROOT,
    ExecutiveKnowledgeModel,
    _build_entities_from_notes,
    _load_evidence_notes,
    build_executive_knowledge,
    render_executive_knowledge,
    render_executive_knowledge_json,
)
from src.knowledge.knowledge_graph import (
    build_knowledge_graph_from_model,
    render_knowledge_graph,
    render_knowledge_graph_json,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
PUBLIC_API = ROOT / "web" / "public" / "api"
PIPELINE_REPORT = OUT / "Executive_Pipeline_Report.md"


@dataclass(frozen=True)
class PipelineStageResult:
    stage: str
    status: str
    duration_seconds: float
    records_processed: int
    warnings: tuple[str, ...]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class ExecutivePipelineReport:
    stages: tuple[PipelineStageResult, ...]
    overall_health: str
    summary: tuple[str, ...]
    source_mode: str
    source_root: str


@dataclass(frozen=True)
class _ScanContext:
    source_mode: str
    source_root: Path
    notes: tuple[Any, ...]
    entities: tuple[Any, ...]
    warnings: tuple[str, ...]


StageRunner = Callable[[dict[str, Any]], tuple[int, list[str]]]


def build_executive_pipeline(
    evidence_root: Path | None = None,
    *,
    vault_root: Path | None = None,
) -> ExecutivePipelineReport:
    OUT.mkdir(exist_ok=True)
    PUBLIC_API.mkdir(parents=True, exist_ok=True)

    effective_evidence_root = evidence_root or DEFAULT_EVIDENCE_ROOT
    effective_vault_root = vault_root or DEFAULT_VAULT_ROOT
    context: dict[str, Any] = {
      "evidence_root": effective_evidence_root,
      "vault_root": effective_vault_root,
      "warnings": [],
      "artifacts": {},
    }

    stage_specs = [
        ("Vault Scan", (), _run_vault_scan),
        ("Entity Resolution", ("Vault Scan",), _run_entity_resolution),
        ("Executive Knowledge Builder", ("Vault Scan",), _run_executive_knowledge_builder),
        ("Knowledge Graph", ("Executive Knowledge Builder",), _run_knowledge_graph),
        ("ExecutiveState", ("Executive Knowledge Builder",), _run_executive_state_stage),
        ("Executive Reasoning", ("ExecutiveState",), _run_executive_reasoning),
        ("Daily Brief", ("ExecutiveState",), _run_daily_brief),
        ("Dashboard API Refresh", ("ExecutiveState",), _run_dashboard_api_refresh),
    ]

    results: list[PipelineStageResult] = []
    status_by_stage: dict[str, str] = {}

    for stage_name, dependencies, runner in stage_specs:
        blocked = [dependency for dependency in dependencies if status_by_stage.get(dependency) != "PASS"]
        if blocked:
            result = PipelineStageResult(
                stage=stage_name,
                status="SKIPPED",
                duration_seconds=0.0,
                records_processed=0,
                warnings=(),
                errors=(f"Blocked by failed or skipped dependency: {', '.join(blocked)}.",),
            )
        else:
            result = _execute_stage(stage_name, context, runner)
        results.append(result)
        status_by_stage[stage_name] = result.status

    overall_health = _derive_overall_health(results)
    scan_context: _ScanContext | None = context["artifacts"].get("scan")
    summary = _build_summary(results, overall_health, scan_context)
    return ExecutivePipelineReport(
        stages=tuple(results),
        overall_health=overall_health,
        summary=summary,
        source_mode=scan_context.source_mode if scan_context else "unknown",
        source_root=str(scan_context.source_root if scan_context else effective_evidence_root),
    )


def render_executive_pipeline(report: ExecutivePipelineReport) -> str:
    parts = [
        "# Executive Pipeline",
        "",
        "| Stage | Status | Duration | Records Processed | Warnings | Errors |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for stage in report.stages:
        warnings = "<br>".join(stage.warnings) if stage.warnings else "-"
        errors = "<br>".join(stage.errors) if stage.errors else "-"
        parts.append(
            f"| {stage.stage} | {stage.status} | {stage.duration_seconds:.3f}s | {stage.records_processed} | {warnings} | {errors} |"
        )
    parts.extend(["", "## Summary", ""])
    parts.extend([f"- {line}" for line in report.summary])
    parts.extend(["", "## Overall Health", "", f"- {report.overall_health}", ""])
    return "\n".join(parts)


def write_executive_pipeline_report(report: ExecutivePipelineReport, output_path: Path = PIPELINE_REPORT) -> Path:
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(render_executive_pipeline(report))
    return output_path


def _execute_stage(
    stage_name: str,
    context: dict[str, Any],
    runner: StageRunner,
) -> PipelineStageResult:
    started = time.perf_counter()
    warnings: list[str] = []
    try:
        records_processed, stage_warnings = runner(context)
        warnings.extend(stage_warnings)
        status = "PASS" if not warnings else "PASS"
        errors: tuple[str, ...] = ()
    except Exception as exc:
        status = "FAIL"
        errors = (str(exc),)
        records_processed = 0
    duration = time.perf_counter() - started
    return PipelineStageResult(
        stage=stage_name,
        status=status,
        duration_seconds=duration,
        records_processed=records_processed,
        warnings=tuple(warnings),
        errors=errors,
    )


def _run_vault_scan(context: dict[str, Any]) -> tuple[int, list[str]]:
    vault_root: Path = context["vault_root"]
    evidence_root: Path = context["evidence_root"]
    warnings: list[str] = []

    if vault_root.exists() and any(vault_root.rglob("*.md")):
        notes = tuple(load_vault(vault_root))
        entities = tuple(extract_entities(vault_root))
        scan = _ScanContext(
            source_mode="live_vault",
            source_root=vault_root,
            notes=notes,
            entities=entities,
            warnings=(),
        )
    else:
        notes = tuple(_load_evidence_notes(evidence_root))
        entities = tuple(_build_entities_from_notes(list(notes)))
        warnings.append(f"Live vault unavailable. Fell back to evidence inventory at {evidence_root}.")
        scan = _ScanContext(
            source_mode="evidence_inventory",
            source_root=evidence_root,
            notes=notes,
            entities=entities,
            warnings=tuple(warnings),
        )

    context["artifacts"]["scan"] = scan
    return len(scan.notes), warnings


def _run_entity_resolution(context: dict[str, Any]) -> tuple[int, list[str]]:
    scan: _ScanContext = context["artifacts"]["scan"]
    resolution = build_entity_resolution(scan.entities)
    context["artifacts"]["entity_resolution"] = resolution
    return len(resolution.canonical_entities), []


def _run_executive_knowledge_builder(context: dict[str, Any]) -> tuple[int, list[str]]:
    scan: _ScanContext = context["artifacts"]["scan"]
    if scan.source_mode == "live_vault":
        report = build_executive_knowledge(context["evidence_root"], vault_root=scan.source_root)
    else:
        report = build_executive_knowledge(context["evidence_root"], vault_root=context["vault_root"])
    context["artifacts"]["knowledge_model"] = report

    (OUT / "Executive_Knowledge.md").write_text(render_executive_knowledge(report))
    (OUT / "Executive_Knowledge.json").write_text(render_executive_knowledge_json(report))
    return len(report.entities), list(scan.warnings)


def _run_knowledge_graph(context: dict[str, Any]) -> tuple[int, list[str]]:
    knowledge_model: ExecutiveKnowledgeModel = context["artifacts"]["knowledge_model"]
    graph = build_knowledge_graph_from_model(knowledge_model)
    context["artifacts"]["knowledge_graph"] = graph
    (OUT / "Knowledge_Graph.md").write_text(render_knowledge_graph(graph))
    (OUT / "Knowledge_Graph.json").write_text(render_knowledge_graph_json(graph))
    return graph.statistics["node_count"] + graph.statistics["edge_count"], []


def _run_executive_state_stage(context: dict[str, Any]) -> tuple[int, list[str]]:
    state = build_executive_state(context["evidence_root"])
    context["artifacts"]["executive_state"] = state
    (OUT / "ExecutiveState_Summary.md").write_text(render_executive_state_summary(state))
    count = (
        len(state.objectives)
        + len(state.projects)
        + len(state.companies)
        + len(state.people)
        + len(state.decisions)
        + len(state.policies)
    )
    return count, []


def _run_executive_reasoning(context: dict[str, Any]) -> tuple[int, list[str]]:
    state = context["artifacts"]["executive_state"]
    reasoning = build_executive_reasoning_from_state(state)
    context["artifacts"]["executive_reasoning"] = reasoning
    (OUT / "Executive_Reasoning.md").write_text(render_executive_reasoning(reasoning))
    return len(reasoning.top_actions), []


def _run_daily_brief(context: dict[str, Any]) -> tuple[int, list[str]]:
    state = context["artifacts"]["executive_state"]
    reasoning = context["artifacts"].get("executive_reasoning")
    brief = build_daily_brief_from_state(state, reasoning=reasoning)
    context["artifacts"]["daily_brief"] = brief
    (OUT / "Daily_Brief.md").write_text(render_daily_brief(brief))
    return len(brief.top_three_priorities) + len(brief.recommended_agenda), []


def _run_dashboard_api_refresh(context: dict[str, Any]) -> tuple[int, list[str]]:
    payload = get_dashboard_home(context["evidence_root"])
    context["artifacts"]["dashboard_api"] = payload
    output = OUT / "Dashboard_Home.json"
    public_output = PUBLIC_API / "dashboard-home.json"
    content = json.dumps(payload, indent=2, sort_keys=True)
    output.write_text(content)
    public_output.write_text(content)
    count = (
        len(payload.get("burning_fires", []))
        + len(payload.get("plan_today", []))
        + len(payload.get("navigation_priorities", []))
    )
    return count, []


def _derive_overall_health(results: list[PipelineStageResult]) -> str:
    if any(result.status == "FAIL" for result in results):
        return "RED"
    if any(result.status == "SKIPPED" for result in results) or any(result.warnings for result in results):
        return "AMBER"
    return "GREEN"


def _build_summary(
    results: list[PipelineStageResult],
    overall_health: str,
    scan_context: _ScanContext | None,
) -> tuple[str, ...]:
    passed = sum(1 for result in results if result.status == "PASS")
    failed = sum(1 for result in results if result.status == "FAIL")
    skipped = sum(1 for result in results if result.status == "SKIPPED")
    source_line = (
        f"Source mode: {scan_context.source_mode} from {scan_context.source_root}."
        if scan_context
        else "Source mode could not be determined."
    )
    return (
        source_line,
        f"Stages passed: {passed}.",
        f"Stages failed: {failed}.",
        f"Stages skipped: {skipped}.",
        f"Overall pipeline health: {overall_health}.",
    )
