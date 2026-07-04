"""Central operational configuration registry for Alfred."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import os
import shutil
import sys

from src.knowledge.executive_knowledge_builder import DEFAULT_VAULT_ROOT

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
VAULT_ENV_VAR = "ALFRED_OBSIDIAN_VAULT"


@dataclass(frozen=True)
class OptionalService:
    name: str
    status: str
    purpose: str
    config_doc: str
    artifact_placeholder: str


@dataclass(frozen=True)
class DeploymentProfile:
    name: str
    description: str
    mode: str
    required_outputs: tuple[str, ...]
    gaps: tuple[str, ...]


@dataclass(frozen=True)
class ConfigurationRegistry:
    root_dir: str
    output_dir: str
    python_executable: str
    npm_executable: str | None
    package_json_present: bool
    node_modules_present: bool
    configured_vault_path: str
    expected_outputs: tuple[str, ...]
    optional_services: tuple[OptionalService, ...]
    deployment_profiles: tuple[DeploymentProfile, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "root_dir": self.root_dir,
            "output_dir": self.output_dir,
            "python_executable": self.python_executable,
            "npm_executable": self.npm_executable,
            "package_json_present": self.package_json_present,
            "node_modules_present": self.node_modules_present,
            "configured_vault_path": self.configured_vault_path,
            "expected_outputs": list(self.expected_outputs),
            "optional_services": [asdict(service) for service in self.optional_services],
            "deployment_profiles": [asdict(profile) for profile in self.deployment_profiles],
        }


def build_configuration_registry(
    root: Path | None = None,
    *,
    output_dir: Path | None = None,
    vault_path: Path | None = None,
) -> ConfigurationRegistry:
    effective_root = root or ROOT
    effective_output_dir = output_dir or (effective_root / "output")
    configured_vault_path = vault_path or _detect_configured_vault_path()
    return ConfigurationRegistry(
        root_dir=str(effective_root),
        output_dir=str(effective_output_dir),
        python_executable=sys.executable,
        npm_executable=shutil.which("npm"),
        package_json_present=(effective_root / "package.json").exists(),
        node_modules_present=(effective_root / "node_modules").exists(),
        configured_vault_path=str(configured_vault_path),
        expected_outputs=_expected_outputs(),
        optional_services=build_optional_service_registry(),
        deployment_profiles=build_deployment_profiles(),
    )


def build_optional_service_registry() -> tuple[OptionalService, ...]:
    return (
        OptionalService(
            name="LlamaIndex",
            status="Not installed",
            purpose="Optional retrieval and indexing support for executive knowledge.",
            config_doc="docs/deployment/LLAMAINDEX_DEPLOYMENT.md",
            artifact_placeholder="downloads/deployment/README.md",
        ),
        OptionalService(
            name="LLM Wiki Enrichment",
            status="Not installed",
            purpose="Optional generated context around executive entities with evidence remaining canonical.",
            config_doc="docs/deployment/LLM_WIKI_ENRICHMENT.md",
            artifact_placeholder="downloads/deployment/README.md",
        ),
        OptionalService(
            name="Deep Research",
            status="Not installed",
            purpose="Optional high-cost research workflow with explicit controls and approval.",
            config_doc="docs/deployment/DEEP_RESEARCH_CONFIGURATION.md",
            artifact_placeholder="downloads/deployment/README.md",
        ),
    )


def build_deployment_profiles() -> tuple[DeploymentProfile, ...]:
    common_outputs = _expected_outputs()
    return (
        DeploymentProfile(
            name="Local Mac",
            description="Current default profile for single-machine Alfred usage.",
            mode="active",
            required_outputs=common_outputs,
            gaps=(
                "Repeatable installer packaging is not yet defined.",
                "Authentication and multi-user controls are not yet enabled.",
            ),
        ),
        DeploymentProfile(
            name="Repeatable Package",
            description="Target profile for packaging Alfred into a repeatable local deployment bundle.",
            mode="target",
            required_outputs=common_outputs,
            gaps=(
                "No packaged config template bundle exists yet.",
                "Doctor remediation scripts are not yet provided.",
                "Write-back and hosted sync controls remain deferred.",
            ),
        ),
    )


def _expected_outputs() -> tuple[str, ...]:
    return (
        "Dashboard_Home.json",
        "ExecutiveState_Summary.md",
        "Executive_Reasoning.md",
        "Daily_Brief.md",
        "Executive_Knowledge.json",
        "Knowledge_Graph.json",
        "Executive_Pipeline_Report.md",
        "Live_Vault_Status.md",
    )


def _detect_configured_vault_path() -> Path:
    override = os.environ.get(VAULT_ENV_VAR)
    if override:
        return Path(override).expanduser()
    return DEFAULT_VAULT_ROOT
