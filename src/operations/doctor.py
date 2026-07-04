"""Operational readiness checks for Alfred."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
import json
import os

from src.operations.config_registry import ConfigurationRegistry, build_configuration_registry

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
    optional_services: tuple[dict[str, str], ...]
    deployment_profiles: tuple[dict[str, object], ...]
    deployment_package_gaps: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "overall_health": self.overall_health,
            "generated_at": self.generated_at,
            "freshness": asdict(self.freshness),
            "checks": [asdict(check) for check in self.checks],
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
    freshness = _build_freshness(effective_output_dir / "ExecutiveState_Summary.md", effective_now)
    checks = (
        _check_python_environment(effective_registry),
        _check_npm_environment(effective_registry),
        _check_vault_path(effective_registry),
        _check_output_files_present(effective_registry, effective_output_dir),
        _check_executive_state_freshness(freshness),
        _check_build_outputs_present(effective_output_dir),
        _check_optional_services_declared(effective_registry),
        _check_specific_service_status(effective_registry, "LlamaIndex"),
        _check_specific_service_status(effective_registry, "LLM Wiki Enrichment"),
        _check_specific_service_status(effective_registry, "Deep Research"),
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


def _check_python_environment(registry: ConfigurationRegistry) -> DoctorCheck:
    executable = Path(registry.python_executable)
    venv_python = Path(registry.root_dir) / ".venv" / "bin" / "python"
    status = "PASS" if executable.exists() and venv_python.exists() else "WARN"
    detail = f"Runtime python is {registry.python_executable}; .venv python {'found' if venv_python.exists() else 'missing'}."
    recommendation = "Use .venv/bin/python for repeatable local builds." if status != "PASS" else "Python environment looks consistent."
    return DoctorCheck("Python environment", status, detail, recommendation)


def _check_npm_environment(registry: ConfigurationRegistry) -> DoctorCheck:
    npm_present = registry.npm_executable is not None
    status = "PASS" if npm_present and registry.package_json_present and registry.node_modules_present else "WARN"
    detail = (
        f"npm executable is {registry.npm_executable or 'missing'}; "
        f"package.json is {'present' if registry.package_json_present else 'missing'}; "
        f"node_modules is {'present' if registry.node_modules_present else 'missing'}."
    )
    recommendation = "Run npm install before packaging Alfred." if status != "PASS" else "npm environment is ready."
    return DoctorCheck("npm environment", status, detail, recommendation)


def _check_vault_path(registry: ConfigurationRegistry) -> DoctorCheck:
    vault_path = Path(registry.configured_vault_path)
    exists = vault_path.exists() and vault_path.is_dir()
    status = "PASS" if exists else "WARN"
    detail = f"Configured vault path is {vault_path} and is {'available' if exists else 'not available'}."
    recommendation = "Set ALFRED_OBSIDIAN_VAULT or create the configured vault path." if status != "PASS" else "Vault path is configured."
    return DoctorCheck("vault path configured", status, detail, recommendation)


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


def _check_optional_services_declared(registry: ConfigurationRegistry) -> DoctorCheck:
    status = "PASS" if registry.optional_services else "WARN"
    detail = f"{len(registry.optional_services)} optional services are declared in the central registry."
    recommendation = "Declare optional services centrally before packaging Alfred." if not registry.optional_services else "Optional services are centrally declared."
    return DoctorCheck("optional services declared", status, detail, recommendation)


def _check_specific_service_status(registry: ConfigurationRegistry, service_name: str) -> DoctorCheck:
    service = next((item for item in registry.optional_services if item.name == service_name), None)
    if service is None:
        return DoctorCheck(service_name + " status", "WARN", "Service is not declared.", "Add the service to the central registry.")
    detail = f"Status is {service.status}; config doc is {service.config_doc}."
    recommendation = "Keep as placeholder until the service is intentionally deployed." if service.status == "Not installed" else "Validate the live service state."
    return DoctorCheck(f"{service_name} status placeholder", "PASS", detail, recommendation)


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
