"""Production mode validation for generated Alfred outputs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from src.operations.config_registry import ConfigurationRegistry, build_configuration_registry

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
REPORT_PATH = OUT / "Production_Validation_Report.md"
RECENT_OUTPUT_WINDOW_SECONDS = 900
VALIDATED_OUTPUT_PREFIXES = (
    "Board_",
    "Dashboard_",
    "Daily_Brief",
    "Environment_",
    "Executive_",
    "Followup_",
    "Knowledge_",
    "LIVE_",
    "Meeting_Brief",
    "Objective_",
    "Open_Loop_",
    "Operational_",
    "Production_Validation_",
)


@dataclass(frozen=True)
class ProductionValidationFinding:
    path: str
    forbidden_string: str


@dataclass(frozen=True)
class ProductionValidationReport:
    production_mode: bool
    scanned_files: tuple[str, ...]
    findings: tuple[ProductionValidationFinding, ...]

    @property
    def status(self) -> str:
        return "PASS" if not self.findings else "FAIL"


def build_production_validation(
    registry: ConfigurationRegistry | None = None,
    *,
    output_dir: Path | None = None,
) -> ProductionValidationReport:
    effective_registry = registry or build_configuration_registry()
    effective_output_dir = output_dir or Path(effective_registry.output_dir)
    effective_root = Path(effective_registry.root_dir)
    now = datetime.now(UTC).timestamp()
    files = sorted(
        [
            path
            for path in effective_output_dir.rglob("*")
            if path.is_file()
            and path.suffix.lower() in {".md", ".json"}
            and now - path.stat().st_mtime <= RECENT_OUTPUT_WINDOW_SECONDS
            and path.name != REPORT_PATH.name
            and path.name.startswith(VALIDATED_OUTPUT_PREFIXES)
        ]
    )
    public_dashboard = effective_root / "web" / "public" / "api" / "dashboard-home.json"
    if public_dashboard.exists() and now - public_dashboard.stat().st_mtime <= RECENT_OUTPUT_WINDOW_SECONDS:
        files.append(public_dashboard)

    findings: list[ProductionValidationFinding] = []
    if effective_registry.production_mode:
        for path in files:
            text = path.read_text(errors="ignore")
            for forbidden in effective_registry.forbidden_output_strings:
                if forbidden in text:
                    findings.append(
                        ProductionValidationFinding(
                            path=str(path.relative_to(effective_root) if path.is_relative_to(effective_root) else path),
                            forbidden_string=forbidden,
                        )
                    )

    return ProductionValidationReport(
        production_mode=effective_registry.production_mode,
        scanned_files=tuple(str(path.relative_to(effective_root) if path.is_relative_to(effective_root) else path) for path in files),
        findings=tuple(findings),
    )


def render_production_validation(report: ProductionValidationReport) -> str:
    lines = [
        "# Production Validation",
        "",
        f"- Production mode: {'true' if report.production_mode else 'false'}",
        f"- Status: {report.status}",
        f"- Files scanned: {len(report.scanned_files)}",
        "",
        "## Findings",
        "",
    ]
    if report.findings:
        for finding in report.findings:
            lines.append(f"- {finding.path}: forbidden string `{finding.forbidden_string}`")
    else:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def write_production_validation(report: ProductionValidationReport) -> Path:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_production_validation(report))
    return REPORT_PATH
