"""Operational readiness checks for Alfred."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
import json
import os

from src.operations.config_registry import ConfigurationRegistry, build_configuration_registry
from src.operations.environment_discovery import (
    build_doctor_summary,
    build_environment_inventory,
    write_environment_inventory,
    STATUS_ACTION_REQUIRED,
    STATUS_CONFIGURED,
    STATUS_DISABLED,
    STATUS_ERROR,
    STATUS_FOUND,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
REPORT_PATH = OUT / "Operational_Readiness_Report.md"
JSON_PATH = OUT / "Operational_Readiness.json"
FRESHNESS_WINDOW_HOURS = 24


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    status: str
    detail: str
    recommendation: str


@dataclass(frozen=True)
class DataFreshness:
    status: str
    age_hours: float | None
    detail: str


@dataclass(frozen=True)
class OperationalReadiness:
    overall_health: str
    generated_at: str
    freshness: DataFreshness
    checks: tuple[DoctorCheck, ...]
    environment_inventory: dict[str, object]
    doctor_summary: dict[str, object]
    optional_services: tuple[dict[str, str], ...]
    deployment_profiles: tuple[dict[str, object], ...]
    deployment_package_gaps: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "overall_health": self.overall_health,
            "generated_at": self.generated_at,
            "freshness": asdict(self.freshness),
            "checks": [asdict(check) for check in self.checks],
            "environment_inventory": self.environment_inventory,
            "doctor_summary": self.doctor_summary,
            "optional_services": list(self.optional_services),
            "deployment_profiles": list(self.deployment_profiles),
            "deployment_package_gaps": list(self.deployment_package_gaps),
        }


def build_operational_readiness(
    registry: ConfigurationRegistry | None = None,
    *,
    output_dir: Path | None = None,
    now: datetime | None = None,
) -> OperationalReadiness:
    effective_registry = registry or build_configuration_registry()
    effective_output_dir = output_dir or Path(effective_registry.output_dir)
    effective_now = now or datetime.now(UTC)
    environment_inventory = build_environment_inventory(
        root=Path(effective_registry.root_dir),
        install_root=Path(effective_registry.root_dir),
        vault_path=Path(effective_registry.configured_vault_path),
        now=effective_now,
        trigger="before_operational_readiness",
    )
    write_environment_inventory(environment_inventory, output_dir=effective_output_dir)
    doctor_summary = build_doctor_summary(environment_inventory)
    freshness = _build_freshness(effective_output_dir / "ExecutiveState_Summary.md", effective_now)
    checks = (
        _check_inventory_component(environment_inventory.as_dict(), "Python", "Python runtime is configured from environment discovery."),
        _check_inventory_component(environment_inventory.as_dict(), "npm", "npm runtime is configured from environment discovery."),
        _check_inventory_component(environment_inventory.as_dict(), "Obsidian Vault", "Vault path is configured from environment discovery."),
        _check_output_files_present(effective_registry, effective_output_dir),
        _check_executive_state_freshness(freshness),
        _check_build_outputs_present(effective_output_dir),
        _check_inventory_component(environment_inventory.as_dict(), "LlamaIndex", "LlamaIndex capability is tracked in the persistent environment inventory."),
        _check_inventory_component(environment_inventory.as_dict(), "LLM Wiki Enrichment", "LLM Wiki capability is tracked in the persistent environment inventory."),
        _check_inventory_component(environment_inventory.as_dict(), "Deep Research", "Deep Research capability is tracked in the persistent environment inventory."),
        _check_deployment_package_gaps(effective_registry),
    )
    overall_health = _derive_overall_health(checks)
    deployment_package_gaps = tuple(
        gap
        for profile in effective_registry.deployment_profiles
        if profile.mode == "target"
        for gap in profile.gaps
    )
    return OperationalReadiness(
        overall_health=overall_health,
        generated_at=effective_now.isoformat(),
        freshness=freshness,
        checks=checks,
        environment_inventory=environment_inventory.as_dict(),
        doctor_summary=doctor_summary,
        optional_services=tuple(asdict(service) for service in effective_registry.optional_services),
        deployment_profiles=tuple(asdict(profile) for profile in effective_registry.deployment_profiles),
        deployment_package_gaps=deployment_package_gaps,
    )


def render_operational_readiness(report: OperationalReadiness) -> str:
    lines = [
        "# Operational Readiness Report",
        "",
        "## Summary",
        "",
        f"- Overall Health: {report.overall_health}",
        f"- Generated At: {report.generated_at}",
        f"- ExecutiveState Freshness: {report.freshness.status}",
        f"- Freshness Detail: {report.freshness.detail}",
        f"- Environment Score: {report.doctor_summary['environment_score']}%",
        "",
        "| Check | Status | Detail | Recommendation |",
        "| --- | --- | --- | --- |",
    ]
    for check in report.checks:
        lines.append(
            f"| {check.name} | {check.status} | {check.detail} | {check.recommendation} |"
        )
    lines.extend(["", "## Optional Services", ""])
    for service in report.optional_services:
        lines.append(f"- {service['name']} | {service['status']} | {service['purpose']}")
    lines.extend(["", "## Deployment Profiles", ""])
    for profile in report.deployment_profiles:
        lines.append(f"- {profile['name']} ({profile['mode']}): {profile['description']}")
        for output in profile["required_outputs"]:
            lines.append(f"  - required output: {output}")
    lines.extend(["", "## Deployment Package Gaps", ""])
    for gap in report.deployment_package_gaps:
        lines.append(f"- {gap}")
    lines.extend(["", "## Alfred Doctor", ""])
    for item in report.doctor_summary["summary_lines"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def render_operational_readiness_json(report: OperationalReadiness) -> str:
    return json.dumps(report.as_dict(), indent=2, sort_keys=True)


def write_operational_readiness(report: OperationalReadiness) -> tuple[Path, Path]:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_operational_readiness(report))
    JSON_PATH.write_text(render_operational_readiness_json(report))
    return REPORT_PATH, JSON_PATH


def _build_freshness(state_summary_path: Path, now: datetime) -> DataFreshness:
    if not state_summary_path.exists():
        return DataFreshness(
            status="MISSING",
            age_hours=None,
            detail="ExecutiveState summary is missing; build outputs need regeneration.",
        )
    modified_at = datetime.fromtimestamp(state_summary_path.stat().st_mtime, UTC)
    age_hours = (now - modified_at).total_seconds() / 3600
    if age_hours <= FRESHNESS_WINDOW_HOURS:
        status = "FRESH"
    elif age_hours <= FRESHNESS_WINDOW_HOURS * 7:
        status = "STALE"
    else:
        status = "OLD"
    return DataFreshness(
        status=status,
        age_hours=round(age_hours, 2),
        detail=f"ExecutiveState summary age is {age_hours:.2f} hours.",
    )


def _check_inventory_component(inventory: dict[str, object], name: str, detail_prefix: str) -> DoctorCheck:
    component = next((item for item in inventory["components"] if item["name"] == name), None)
    if component is None:
        return DoctorCheck(f"{name} inventory", "WARN", f"{name} is missing from the environment inventory.", "Re-run environment discovery before continuing.")

    if component["status"] in {STATUS_CONFIGURED, STATUS_FOUND, STATUS_DISABLED}:
        status = "PASS"
    elif component["status"] == "NOT_FOUND" and component.get("required") is False:
        status = "PASS"
    elif component["status"] == STATUS_ERROR:
        status = "FAIL"
    else:
        status = "WARN"

    detail = f"{detail_prefix} Status is {component['status']}; health is {component['health']}."
    recommendation = component["recommended_action"]
    return DoctorCheck(f"{name} inventory", status, detail, recommendation)


def _check_output_files_present(registry: ConfigurationRegistry, output_dir: Path) -> DoctorCheck:
    missing = [name for name in registry.expected_outputs if not (output_dir / name).exists()]
    status = "PASS" if not missing else "WARN"
    detail = "All expected output files are present." if not missing else f"Missing outputs: {', '.join(missing)}."
    recommendation = "Run python build_everything.py to regenerate missing outputs." if missing else "Output directory is populated."
    return DoctorCheck("output files present", status, detail, recommendation)


def _check_executive_state_freshness(freshness: DataFreshness) -> DoctorCheck:
    status = "PASS" if freshness.status == "FRESH" else "WARN"
    recommendation = "Rebuild ExecutiveState and downstream outputs if freshness is stale." if status != "PASS" else "ExecutiveState freshness is within the target window."
    return DoctorCheck("ExecutiveState freshness", status, freshness.detail, recommendation)


def _check_build_outputs_present(output_dir: Path) -> DoctorCheck:
    required = ("Dashboard_Home.json", "Executive_Pipeline_Report.md", "Live_Vault_Status.md")
    missing = [name for name in required if not (output_dir / name).exists()]
    status = "PASS" if not missing else "WARN"
    detail = "Core build outputs are present." if not missing else f"Missing core build outputs: {', '.join(missing)}."
    recommendation = "Re-run the pipeline and dashboard builds." if missing else "Core build outputs are available."
    return DoctorCheck("build outputs present", status, detail, recommendation)


def _check_deployment_package_gaps(registry: ConfigurationRegistry) -> DoctorCheck:
    gaps = [
        gap
        for profile in registry.deployment_profiles
        if profile.mode == "target"
        for gap in profile.gaps
    ]
    status = "WARN" if gaps else "PASS"
    detail = "No deployment package gaps recorded." if not gaps else f"{len(gaps)} package gaps remain."
    recommendation = "Address the target profile gaps before treating Alfred as a repeatable package." if gaps else "No packaging gaps remain."
    return DoctorCheck("deployment package gaps", status, detail, recommendation)


def _derive_overall_health(checks: tuple[DoctorCheck, ...]) -> str:
    failures = sum(1 for check in checks if check.status == "FAIL")
    warnings = sum(1 for check in checks if check.status == "WARN")
    if failures:
        return "RED"
    if warnings:
        return "AMBER"
    return "GREEN"
