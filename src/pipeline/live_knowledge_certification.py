"""Live knowledge certification for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.knowledge.executive_knowledge_builder import DEFAULT_EVIDENCE_ROOT
from src.operations.environment_discovery import (
    COMPONENT_VAULT_PRIMARY,
    DISCOVERY_TRIGGER_BEFORE_DEPLOYMENT,
    STATUS_ACTION_REQUIRED,
    STATUS_CONFIGURED,
    build_environment_inventory,
    get_component_by_id,
)
from src.pipeline.executive_pipeline import build_executive_pipeline

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
CERTIFICATION_REPORT = OUT / "LIVE_KNOWLEDGE_CERTIFICATION.md"

EXPECTED_DOMAINS = (
    "Objectives discovered",
    "Projects discovered",
    "People discovered",
    "Companies discovered",
    "Meetings discovered",
    "Daily Logs discovered",
    "Decisions discovered",
    "Risks discovered",
    "Open Loops discovered",
    "Follow-ups discovered",
    "Executive Briefings discovered",
)


@dataclass(frozen=True)
class LiveKnowledgeCertification:
    vault_path: str
    source_mode: str
    metrics: dict[str, object]
    status: str
    reasons: tuple[str, ...]


def build_live_knowledge_certification(
    evidence_root: Path | None = None,
    *,
    vault_root: Path | None = None,
) -> LiveKnowledgeCertification:
    inventory = build_environment_inventory(
        vault_path=vault_root,
        trigger=DISCOVERY_TRIGGER_BEFORE_DEPLOYMENT,
    )
    vault_component = get_component_by_id(inventory, COMPONENT_VAULT_PRIMARY)
    effective_vault_root = Path(vault_component.install_location)
    if vault_component.status not in {STATUS_CONFIGURED, STATUS_ACTION_REQUIRED} or not effective_vault_root.exists():
        return LiveKnowledgeCertification(
            vault_path=vault_component.install_location,
            source_mode="unavailable",
            metrics={
                "Vault path": vault_component.install_location,
                "Markdown files processed": 0,
                "ExecutiveState generated": False,
                "Daily Brief generated": False,
                "Dashboard API generated": False,
            },
            status="FAIL",
            reasons=(vault_component.recommended_action,),
        )

    pipeline = build_executive_pipeline(
        evidence_root or DEFAULT_EVIDENCE_ROOT,
        vault_root=effective_vault_root,
        require_live_vault=True,
    )
    metrics = {
        "Vault path": pipeline.artifacts_summary["vault_path"],
        "Markdown files processed": pipeline.artifacts_summary["markdown_files_processed"],
        "Objectives discovered": pipeline.artifacts_summary["objectives_discovered"],
        "Projects discovered": pipeline.artifacts_summary["projects_discovered"],
        "People discovered": pipeline.artifacts_summary["people_discovered"],
        "Companies discovered": pipeline.artifacts_summary["companies_discovered"],
        "Meetings discovered": pipeline.artifacts_summary["meetings_discovered"],
        "Daily Logs discovered": pipeline.artifacts_summary["daily_logs_discovered"],
        "Decisions discovered": pipeline.artifacts_summary["decisions_discovered"],
        "Risks discovered": pipeline.artifacts_summary["risks_discovered"],
        "Open Loops discovered": pipeline.artifacts_summary["open_loops_discovered"],
        "Follow-ups discovered": pipeline.artifacts_summary["followups_discovered"],
        "Executive Briefings discovered": pipeline.artifacts_summary["executive_briefings_discovered"],
        "Knowledge Graph node count": pipeline.artifacts_summary["knowledge_graph_node_count"],
        "Knowledge Graph edge count": pipeline.artifacts_summary["knowledge_graph_edge_count"],
        "ExecutiveState generated": pipeline.artifacts_summary["executive_state_generated"],
        "Daily Brief generated": pipeline.artifacts_summary["daily_brief_generated"],
        "Dashboard API generated": pipeline.artifacts_summary["dashboard_api_generated"],
    }
    reasons = _derive_reasons(pipeline, metrics)
    status = _derive_status(pipeline, metrics, reasons)
    return LiveKnowledgeCertification(
        vault_path=str(effective_vault_root),
        source_mode=pipeline.source_mode,
        metrics=metrics,
        status=status,
        reasons=reasons,
    )


def render_live_knowledge_certification(report: LiveKnowledgeCertification) -> str:
    lines = [
        "# Live Knowledge Certification",
        "",
        f"- Source mode: {report.source_mode}",
        "",
    ]
    for key, value in report.metrics.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Certification Summary", "", f"- {report.status}"])
    for reason in report.reasons:
        lines.append(f"- {reason}")
    lines.append("")
    return "\n".join(lines)


def write_live_knowledge_certification(report: LiveKnowledgeCertification) -> Path:
    CERTIFICATION_REPORT.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATION_REPORT.write_text(render_live_knowledge_certification(report))
    return CERTIFICATION_REPORT


def _derive_reasons(pipeline, metrics: dict[str, object]) -> tuple[str, ...]:
    reasons: list[str] = []
    if pipeline.source_mode != "live_vault":
        reasons.append("Pipeline did not run against a live vault.")
    failed_stages = [stage.stage for stage in pipeline.stages if stage.status == "FAIL"]
    if failed_stages:
        reasons.append(f"Pipeline stages failed: {', '.join(failed_stages)}.")
    for label in EXPECTED_DOMAINS:
        if metrics[label] == 0:
            reasons.append(f"{label} is zero.")
    if metrics["Knowledge Graph node count"] == 0 or metrics["Knowledge Graph edge count"] == 0:
        reasons.append("Knowledge Graph is empty.")
    if metrics["ExecutiveState generated"] is not True:
        reasons.append("ExecutiveState was not generated.")
    if metrics["Daily Brief generated"] is not True:
        reasons.append("Daily Brief was not generated.")
    if metrics["Dashboard API generated"] is not True:
        reasons.append("Dashboard API was not generated.")
    if not reasons and pipeline.overall_health == "AMBER":
        reasons.append("Pipeline completed with warnings.")
    if not reasons:
        reasons.append("Live executive knowledge path is populated across all expected domains.")
    return tuple(reasons)


def _derive_status(pipeline, metrics: dict[str, object], reasons: tuple[str, ...]) -> str:
    if pipeline.source_mode != "live_vault":
        return "FAIL"
    if any(stage.status == "FAIL" for stage in pipeline.stages):
        return "FAIL"
    if any(metrics[label] == 0 for label in EXPECTED_DOMAINS):
        return "FAIL"
    if metrics["Knowledge Graph node count"] == 0 or metrics["Knowledge Graph edge count"] == 0:
        return "FAIL"
    if not all(
        (
            metrics["ExecutiveState generated"],
            metrics["Daily Brief generated"],
            metrics["Dashboard API generated"],
        )
    ):
        return "FAIL"
    if pipeline.overall_health == "AMBER" or any("warnings" in reason.lower() for reason in reasons):
        return "WARNING"
    return "PASS"
