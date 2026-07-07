"""Production knowledge certification for Alfred."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json

from src.daily.daily_brief import DailyBrief, build_daily_brief_from_state
from src.executive.executive_state import ExecutiveState, build_executive_state
from src.knowledge.executive_knowledge_builder import DEFAULT_EVIDENCE_ROOT
from src.knowledge.providers.legacy_adapter import LegacyKnowledgeAdapter, build_legacy_knowledge_adapter
from src.obsidian.live_vault import detect_live_vault_status
from src.operations.config_registry import ConfigurationRegistry, build_configuration_registry

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
MARKDOWN_REPORT = OUT / "Knowledge_Certification.md"
JSON_REPORT = OUT / "Knowledge_Certification.json"

FALLBACK_MARKERS = (
    "No evidence found",
    "No active follow-up identified.",
    "No active open loop identified.",
)

ENGINEERING_PREFIXES = (
    "output/",
    "analysis/",
    "trees/",
    "python/",
    "system/",
    "docs/",
    ".git/",
    ".obsidian/",
    ".smart-env/",
    "node_modules/",
)


@dataclass(frozen=True)
class KnowledgeCertificationCheck:
    name: str
    status: str
    detail: str
    remediation: str


@dataclass(frozen=True)
class KnowledgeCertificationReport:
    overall_status: str
    vault_path: str
    markdown_files_processed: int
    knowledge_provider: str
    checks: tuple[KnowledgeCertificationCheck, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "overall_status": self.overall_status,
            "vault_path": self.vault_path,
            "markdown_files_processed": self.markdown_files_processed,
            "knowledge_provider": self.knowledge_provider,
            "checks": [asdict(check) for check in self.checks],
        }


def build_knowledge_certification(
    registry: ConfigurationRegistry | None = None,
    *,
    evidence_root: Path | None = None,
    vault_root: Path | None = None,
) -> KnowledgeCertificationReport:
    effective_registry = registry or build_configuration_registry(vault_path=vault_root)
    effective_vault_root = Path(vault_root or effective_registry.configured_vault_path).expanduser()
    effective_evidence_root = evidence_root or DEFAULT_EVIDENCE_ROOT
    vault_status = detect_live_vault_status(effective_vault_root)

    if vault_status.status != "PASS":
        checks = (
            KnowledgeCertificationCheck(
                name="Live vault accessibility",
                status="FAIL",
                detail=(
                    f"Configured vault path is {vault_status.vault_path}; "
                    f"status={vault_status.status}; markdown_files_processed={vault_status.markdown_files_processed}."
                ),
                remediation="Configure a readable live vault at /docker/obsidian-vault before certifying knowledge population.",
            ),
        )
        return KnowledgeCertificationReport(
            overall_status="RED",
            vault_path=vault_status.vault_path,
            markdown_files_processed=vault_status.markdown_files_processed,
            knowledge_provider=effective_registry.default_knowledge_provider,
            checks=checks,
        )

    adapter = build_legacy_knowledge_adapter(effective_evidence_root, vault_root=effective_vault_root)
    state = build_executive_state(
        effective_evidence_root,
        vault_root=effective_vault_root,
        knowledge_provider=effective_registry.default_knowledge_provider,
    )
    daily_brief = build_daily_brief_from_state(state)

    checks = (
        _check_live_vault(vault_status),
        _check_provider_activation(effective_registry, adapter, state),
        _check_source_modes(adapter, state),
        _check_domain_items("Objectives", state.objectives, minimum=1),
        _check_domain_items("Projects", state.projects, minimum=1),
        _check_followups(state),
        _check_open_loops(state),
        _check_daily_brief(daily_brief),
    )
    overall_status = _derive_overall_status(checks)
    return KnowledgeCertificationReport(
        overall_status=overall_status,
        vault_path=vault_status.vault_path,
        markdown_files_processed=vault_status.markdown_files_processed,
        knowledge_provider=effective_registry.default_knowledge_provider,
        checks=checks,
    )


def render_knowledge_certification(report: KnowledgeCertificationReport) -> str:
    lines = [
        "# Knowledge Certification",
        "",
        f"- Overall Status: {report.overall_status}",
        f"- Vault Path: {report.vault_path}",
        f"- Markdown Files Processed: {report.markdown_files_processed}",
        f"- Knowledge Provider: {report.knowledge_provider}",
        "",
        "| Check | Status | Detail | Remediation |",
        "| --- | --- | --- | --- |",
    ]
    for check in report.checks:
        lines.append(f"| {check.name} | {check.status} | {check.detail} | {check.remediation} |")
    lines.append("")
    return "\n".join(lines)


def render_knowledge_certification_json(report: KnowledgeCertificationReport) -> str:
    return json.dumps(report.as_dict(), indent=2, sort_keys=True)


def write_knowledge_certification(report: KnowledgeCertificationReport) -> tuple[Path, Path]:
    MARKDOWN_REPORT.parent.mkdir(parents=True, exist_ok=True)
    MARKDOWN_REPORT.write_text(render_knowledge_certification(report))
    JSON_REPORT.write_text(render_knowledge_certification_json(report))
    return MARKDOWN_REPORT, JSON_REPORT


def _check_live_vault(vault_status) -> KnowledgeCertificationCheck:
    return KnowledgeCertificationCheck(
        name="Live vault accessibility",
        status="PASS",
        detail=(
            f"Vault path {vault_status.vault_path} is readable; "
            f"markdown_files_processed={vault_status.markdown_files_processed}."
        ),
        remediation="Keep /docker/obsidian-vault mounted and readable by Alfred.",
    )


def _check_provider_activation(
    registry: ConfigurationRegistry,
    adapter: LegacyKnowledgeAdapter,
    state: ExecutiveState,
) -> KnowledgeCertificationCheck:
    expected = registry.default_knowledge_provider
    actual = adapter.__class__.__name__
    state_has_adapter = state.adapter is not None and state.adapter.__class__.__name__ == "LegacyKnowledgeAdapter"
    status = "PASS" if expected == "legacy_adapter" and actual == "LegacyKnowledgeAdapter" and state_has_adapter else "FAIL"
    detail = (
        f"Configured provider={expected}; adapter_class={actual}; "
        f"executive_state_adapter={state.adapter.__class__.__name__ if state.adapter else 'missing'}."
    )
    remediation = "Configure default_knowledge_provider=legacy_adapter and ensure ExecutiveState is built through that adapter."
    return KnowledgeCertificationCheck("Legacy knowledge provider activation", status, detail, remediation)


def _check_source_modes(adapter: LegacyKnowledgeAdapter, state: ExecutiveState) -> KnowledgeCertificationCheck:
    adapter_mode = adapter.knowledge_model.source_mode
    state_mode = state.knowledge_model.source_mode if state.knowledge_model is not None else "missing"
    counts = {
        "objectives": len(state.objectives),
        "projects": len(state.projects),
        "people": len(state.people),
        "companies": len(state.companies),
        "decisions": len(state.decisions),
    }
    if adapter_mode == "live_vault" and state_mode == "live_vault" and any(counts.values()):
        status = "PASS"
    elif adapter_mode == "live_vault" and state_mode == "live_vault":
        status = "AMBER"
    else:
        status = "FAIL"
    detail = (
        f"adapter_source_mode={adapter_mode}; state_source_mode={state_mode}; "
        f"counts={counts}."
    )
    remediation = "Ensure ExecutiveState consumes the configured provider against the live vault rather than evidence inventory fallback."
    return KnowledgeCertificationCheck("ExecutiveState live-vault population", status, detail, remediation)


def _check_domain_items(name: str, items: tuple[object, ...], *, minimum: int) -> KnowledgeCertificationCheck:
    valid_paths = [getattr(item, "path", "") for item in items if _is_valid_evidence_path(getattr(item, "path", ""))]
    status = "PASS" if len(items) >= minimum and len(valid_paths) == len(items) else ("AMBER" if items else "FAIL")
    sample = ", ".join(valid_paths[:3]) if valid_paths else "none"
    detail = f"count={len(items)}; evidence_backed={len(valid_paths)}; sample_paths={sample}."
    remediation = f"Confirm {name.lower()} are being sourced from executive Obsidian notes rather than fallback inventory or excluded engineering paths."
    return KnowledgeCertificationCheck(f"{name} evidence coverage", status, detail, remediation)


def _check_followups(state: ExecutiveState) -> KnowledgeCertificationCheck:
    followups = state.followups
    candidates = tuple(followups.overdue) + tuple(followups.due_today) + tuple(followups.high_priority)
    valid = [item.path for item in candidates if _is_valid_evidence_path(item.path)]
    status = "PASS" if candidates and valid else ("AMBER" if followups.followup_count else "FAIL")
    detail = (
        f"followup_count={followups.followup_count}; overdue={len(followups.overdue)}; "
        f"due_today={len(followups.due_today)}; high_priority={len(followups.high_priority)}; "
        f"sample_paths={', '.join(valid[:3]) if valid else 'none'}."
    )
    remediation = "Confirm follow-up notes and actionable lines are present in the live vault and are not being replaced by no-evidence summaries."
    return KnowledgeCertificationCheck("Follow-up evidence coverage", status, detail, remediation)


def _check_open_loops(state: ExecutiveState) -> KnowledgeCertificationCheck:
    open_loops = state.open_loops
    candidates = (
        tuple(open_loops.critical_open_loops)
        + tuple(open_loops.waiting_for)
        + tuple(open_loops.missing_owners)
    )
    valid = [item.path for item in candidates if _is_valid_evidence_path(item.path)]
    status = "PASS" if candidates and valid else ("AMBER" if open_loops.open_loop_count else "FAIL")
    detail = (
        f"open_loop_count={open_loops.open_loop_count}; critical={len(open_loops.critical_open_loops)}; "
        f"waiting_for={len(open_loops.waiting_for)}; missing_owners={len(open_loops.missing_owners)}; "
        f"sample_paths={', '.join(valid[:3]) if valid else 'none'}."
    )
    remediation = "Confirm open-loop register notes are present in the live vault and are being parsed into ExecutiveState."
    return KnowledgeCertificationCheck("Open-loop evidence coverage", status, detail, remediation)


def _check_daily_brief(brief: DailyBrief) -> KnowledgeCertificationCheck:
    sections = (
        tuple(brief.top_three_priorities)
        + tuple(brief.followups_due_today)
        + tuple(brief.open_loops_blocking_progress)
        + tuple(brief.one_page_executive_summary)
    )
    fallback_hits = sorted({marker for marker in FALLBACK_MARKERS if any(marker in value for value in sections)})
    status = "PASS" if sections and not fallback_hits else ("AMBER" if sections else "FAIL")
    detail = (
        f"confidence={brief.confidence}; top_priorities={brief.top_three_priorities[:3]}; "
        f"fallback_markers={fallback_hits or ['none']}."
    )
    remediation = "Daily Brief should be derived from evidence-backed ExecutiveState output rather than fallback no-evidence strings."
    return KnowledgeCertificationCheck("Daily Brief evidence coverage", status, detail, remediation)


def _derive_overall_status(checks: tuple[KnowledgeCertificationCheck, ...]) -> str:
    statuses = {check.status for check in checks}
    if "FAIL" in statuses:
        return "RED"
    if "AMBER" in statuses:
        return "AMBER"
    return "GREEN"


def _is_valid_evidence_path(path: str) -> bool:
    if not path or path == "none":
        return False
    lowered = path.replace("\\", "/").lstrip("./")
    return not any(lowered.startswith(prefix) for prefix in ENGINEERING_PREFIXES)
