"""Environment discovery and inventory for Alfred platform management."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
import importlib.util
import json
import os
import shutil
import subprocess
import sys

from src.obsidian.live_vault import detect_live_vault_status, resolve_live_vault_path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
INVENTORY_JSON = OUT / "Environment_Inventory.json"
INVENTORY_MD = OUT / "Environment_Inventory.md"

STATUS_FOUND = "FOUND"
STATUS_NOT_FOUND = "NOT_FOUND"
STATUS_CONFIGURED = "CONFIGURED"
STATUS_ACTION_REQUIRED = "ACTION_REQUIRED"
STATUS_DISABLED = "DISABLED"
STATUS_ERROR = "ERROR"

HEALTH_HEALTHY = "HEALTHY"
HEALTH_WARN = "WARN"
HEALTH_UNKNOWN = "UNKNOWN"
HEALTH_ERROR = "ERROR"


@dataclass(frozen=True)
class AutoConfiguredValue:
    value: str
    discovery_method: str
    confidence: str
    timestamp: str


@dataclass(frozen=True)
class EnvironmentComponent:
    name: str
    category: str
    status: str
    health: str
    version: str
    install_location: str
    configuration_source: str
    required: bool
    dependencies: tuple[str, ...]
    last_checked: str
    last_changed: str
    recommended_action: str
    work_instruction_link: str


@dataclass(frozen=True)
class EnvironmentInventory:
    generated_at: str
    environment_score: int
    components: tuple[EnvironmentComponent, ...]
    auto_configured: dict[str, AutoConfiguredValue]
    required_actions: tuple[str, ...]
    architecture_rule: str

    def as_dict(self) -> dict[str, object]:
        return {
            "generated_at": self.generated_at,
            "environment_score": self.environment_score,
            "components": [asdict(component) for component in self.components],
            "auto_configured": {
                key: asdict(value) for key, value in self.auto_configured.items()
            },
            "required_actions": list(self.required_actions),
            "architecture_rule": self.architecture_rule,
        }


def build_environment_inventory(
    *,
    root: Path | None = None,
    install_root: Path | None = None,
    vault_path: Path | None = None,
    now: datetime | None = None,
) -> EnvironmentInventory:
    effective_root = root or ROOT
    effective_install_root = install_root or effective_root
    checked_at = (now or datetime.now(UTC)).isoformat()
    components: list[EnvironmentComponent] = []
    auto_configured: dict[str, AutoConfiguredValue] = {}

    vault_status = detect_live_vault_status(vault_path)
    vault_component = EnvironmentComponent(
        name="Obsidian Vault",
        category="Vault",
        status=STATUS_CONFIGURED if vault_status.status == "PASS" else STATUS_ACTION_REQUIRED,
        health=HEALTH_HEALTHY if vault_status.status == "PASS" else HEALTH_WARN,
        version="n/a",
        install_location=vault_status.vault_path,
        configuration_source=vault_status.source,
        required=True,
        dependencies=(),
        last_checked=checked_at,
        last_changed=_path_mtime(vault_status.vault_path),
        recommended_action="Use the detected live vault path." if vault_status.status == "PASS" else "Provide a readable vault path with markdown files.",
        work_instruction_link="docs/deployment/INSTALLATION_GUIDE.md",
    )
    components.append(vault_component)
    if vault_status.status == "PASS":
        auto_configured["vault_path"] = AutoConfiguredValue(
            value=vault_status.vault_path,
            discovery_method=f"filesystem scan via {vault_status.source}",
            confidence="HIGH",
            timestamp=checked_at,
        )

    python_exec = sys.executable
    components.append(
        EnvironmentComponent(
            name="Python",
            category="Runtime",
            status=STATUS_CONFIGURED if Path(python_exec).exists() else STATUS_ERROR,
            health=HEALTH_HEALTHY if Path(python_exec).exists() else HEALTH_ERROR,
            version=_command_output([python_exec, "--version"]),
            install_location=python_exec,
            configuration_source="runtime interpreter",
            required=True,
            dependencies=(),
            last_checked=checked_at,
            last_changed=_path_mtime(python_exec),
            recommended_action="Use detected Python executable." if Path(python_exec).exists() else "Install Python 3 and re-run discovery.",
            work_instruction_link="docs/deployment/INSTALLATION_GUIDE.md",
        )
    )
    auto_configured["python_executable"] = AutoConfiguredValue(
        value=python_exec,
        discovery_method="active Python runtime",
        confidence="HIGH",
        timestamp=checked_at,
    )

    _append_command_component(
        components,
        auto_configured,
        key="node_executable",
        name="Node",
        category="Runtime",
        command_name="node",
        required=True,
        checked_at=checked_at,
        work_instruction="docs/deployment/INSTALLATION_GUIDE.md",
    )
    _append_command_component(
        components,
        auto_configured,
        key="npm_executable",
        name="npm",
        category="Runtime",
        command_name="npm",
        required=True,
        checked_at=checked_at,
        work_instruction="docs/deployment/INSTALLATION_GUIDE.md",
    )
    _append_command_component(
        components,
        auto_configured,
        key="docker_executable",
        name="Docker",
        category="Runtime",
        command_name="docker",
        required=False,
        checked_at=checked_at,
        work_instruction="docs/deployment/POST_INSTALL_VALIDATION.md",
    )
    _append_command_component(
        components,
        auto_configured,
        key="ollama_executable",
        name="Ollama",
        category="AI Providers",
        command_name="ollama",
        required=False,
        checked_at=checked_at,
        work_instruction="docs/deployment/INSTALLATION_GUIDE.md",
    )

    components.extend(
        [
            _api_key_component("OpenRouter", "OPENROUTER_API_KEY", checked_at),
            _api_key_component("OpenAI", "OPENAI_API_KEY", checked_at),
            _api_key_component("Anthropic", "ANTHROPIC_API_KEY", checked_at),
            _path_or_package_component(
                name="LlamaIndex",
                category="Knowledge Sources",
                package_name="llama_index",
                config_path=effective_install_root / "config" / "llamaindex.yaml",
                required=False,
                checked_at=checked_at,
                work_instruction_link="docs/deployment/LLAMAINDEX_DEPLOYMENT.md",
            ),
            _path_or_package_component(
                name="LLM Wiki Enrichment",
                category="Knowledge Sources",
                package_name=None,
                config_path=effective_install_root / "config" / "llm_wiki_enrichment.yaml",
                required=False,
                checked_at=checked_at,
                work_instruction_link="docs/deployment/LLM_WIKI_ENRICHMENT.md",
            ),
            _path_or_package_component(
                name="Semantic Search",
                category="Knowledge Sources",
                package_name=None,
                config_path=effective_install_root / "data" / "semantic-index",
                required=False,
                checked_at=checked_at,
                work_instruction_link="docs/deployment/POST_INSTALL_VALIDATION.md",
            ),
            EnvironmentComponent(
                name="Deep Research",
                category="AI Providers",
                status=STATUS_DISABLED,
                health=HEALTH_UNKNOWN,
                version="n/a",
                install_location="",
                configuration_source="product policy",
                required=False,
                dependencies=("OpenRouter", "OpenAI", "Anthropic"),
                last_checked=checked_at,
                last_changed="",
                recommended_action="Enable only after explicit approval and budget controls are in place.",
                work_instruction_link="docs/deployment/DEEP_RESEARCH_CONFIGURATION.md",
            ),
            _systemd_component(checked_at),
        ]
    )

    components.sort(key=lambda item: (item.category, item.required is False, item.name.lower()))
    required_actions = tuple(
        component.recommended_action
        for component in components
        if component.status in {STATUS_ACTION_REQUIRED, STATUS_ERROR}
    )

    return EnvironmentInventory(
        generated_at=checked_at,
        environment_score=_environment_score(components),
        components=tuple(components),
        auto_configured=auto_configured,
        required_actions=required_actions,
        architecture_rule="Alfred should never ask the user for information it can discover automatically.",
    )


def write_environment_inventory(
    inventory: EnvironmentInventory,
    *,
    output_dir: Path | None = None,
) -> tuple[Path, Path]:
    effective_output_dir = output_dir or OUT
    effective_output_dir.mkdir(parents=True, exist_ok=True)
    json_path = effective_output_dir / INVENTORY_JSON.name
    md_path = effective_output_dir / INVENTORY_MD.name
    json_path.write_text(json.dumps(inventory.as_dict(), indent=2, sort_keys=True))
    md_path.write_text(render_environment_inventory_markdown(inventory))
    return md_path, json_path


def render_environment_inventory_markdown(inventory: EnvironmentInventory) -> str:
    lines = [
        "# Environment Inventory",
        "",
        f"- Generated At: {inventory.generated_at}",
        f"- Environment Score: {inventory.environment_score}%",
        f"- Architecture Rule: {inventory.architecture_rule}",
        "",
        "| Name | Category | Status | Health | Version | Location | Config Source | Required | Recommended Action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for component in inventory.components:
        lines.append(
            f"| {component.name} | {component.category} | {component.status} | {component.health} | "
            f"{component.version or 'n/a'} | {component.install_location or '-'} | "
            f"{component.configuration_source or '-'} | {'Required' if component.required else 'Optional'} | "
            f"{component.recommended_action} |"
        )
    lines.extend(["", "## Auto Configured", ""])
    for key, value in sorted(inventory.auto_configured.items()):
        lines.append(
            f"- {key}: {value.value} | {value.discovery_method} | {value.confidence} | {value.timestamp}"
        )
    lines.extend(["", "## Required Actions", ""])
    for action in inventory.required_actions:
        lines.append(f"- {action}")
    if not inventory.required_actions:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def render_detected_environment_yaml(inventory: EnvironmentInventory) -> str:
    lines = ["detected_environment:"]
    for component in inventory.components:
        key = _yaml_key(component.name)
        lines.extend(
            [
                f"  {key}:",
                f"    category: {component.category}",
                f"    status: {component.status}",
                f"    health: {component.health}",
                f"    version: {component.version or 'n/a'}",
                f"    install_location: {component.install_location or ''}",
                f"    configuration_source: {component.configuration_source or ''}",
                f"    required: {'true' if component.required else 'false'}",
                f"    dependencies: [{', '.join(component.dependencies)}]",
                f"    last_checked: {component.last_checked}",
                f"    last_changed: {component.last_changed}",
                f"    recommended_action: {component.recommended_action}",
                f"    work_instruction_link: {component.work_instruction_link}",
            ]
        )
    lines.append("auto_configured:")
    for key, value in sorted(inventory.auto_configured.items()):
        lines.extend(
            [
                f"  {key}:",
                f"    value: {value.value}",
                f"    discovery_method: {value.discovery_method}",
                f"    confidence: {value.confidence}",
                f"    timestamp: {value.timestamp}",
            ]
        )
    return "\n".join(lines) + "\n"


def build_doctor_summary(inventory: EnvironmentInventory) -> dict[str, object]:
    healthy = [component for component in inventory.components if component.status in {STATUS_FOUND, STATUS_CONFIGURED}]
    warnings = [component for component in inventory.components if component.status == STATUS_ACTION_REQUIRED]
    disabled = [component for component in inventory.components if component.status == STATUS_DISABLED]
    summary_lines = [f"Environment Score: {inventory.environment_score}%"]
    summary_lines.extend([f"✓ {component.name} {component.status.lower()}" for component in healthy[:5]])
    summary_lines.extend([f"⚠ {component.name} {component.recommended_action}" for component in warnings[:5]])
    summary_lines.extend([f"- {component.name} disabled by policy" for component in disabled[:3]])
    return {
        "environment_score": inventory.environment_score,
        "healthy": [component.name for component in healthy],
        "warnings": [component.name for component in warnings],
        "disabled": [component.name for component in disabled],
        "recommended_actions": list(inventory.required_actions[:8]),
        "summary_lines": summary_lines,
    }


def _append_command_component(
    components: list[EnvironmentComponent],
    auto_configured: dict[str, AutoConfiguredValue],
    *,
    key: str,
    name: str,
    category: str,
    command_name: str,
    required: bool,
    checked_at: str,
    work_instruction: str,
) -> None:
    executable = shutil.which(command_name) or ""
    status = STATUS_CONFIGURED if executable else (STATUS_ACTION_REQUIRED if required else STATUS_NOT_FOUND)
    health = HEALTH_HEALTHY if executable else (HEALTH_WARN if required else HEALTH_UNKNOWN)
    version = _command_output([command_name, "--version"]) if executable else "n/a"
    components.append(
        EnvironmentComponent(
            name=name,
            category=category,
            status=status,
            health=health,
            version=version,
            install_location=executable,
            configuration_source="PATH discovery" if executable else "PATH discovery failed",
            required=required,
            dependencies=(),
            last_checked=checked_at,
            last_changed=_path_mtime(executable),
            recommended_action=f"Use detected {name} executable." if executable else f"Install or configure {name}.",
            work_instruction_link=work_instruction,
        )
    )
    if executable:
        auto_configured[key] = AutoConfiguredValue(
            value=executable,
            discovery_method="PATH lookup",
            confidence="HIGH",
            timestamp=checked_at,
        )


def _api_key_component(name: str, env_var: str, checked_at: str) -> EnvironmentComponent:
    present = bool(os.environ.get(env_var))
    return EnvironmentComponent(
        name=name,
        category="AI Providers",
        status=STATUS_CONFIGURED if present else STATUS_ACTION_REQUIRED,
        health=HEALTH_HEALTHY if present else HEALTH_WARN,
        version="n/a",
        install_location="",
        configuration_source=env_var if present else f"{env_var} not set",
        required=False,
        dependencies=(),
        last_checked=checked_at,
        last_changed="",
        recommended_action="No action required." if present else f"Add {env_var} through a secure secret store.",
        work_instruction_link="docs/deployment/INSTALLATION_GUIDE.md",
    )


def _path_or_package_component(
    *,
    name: str,
    category: str,
    package_name: str | None,
    config_path: Path,
    required: bool,
    checked_at: str,
    work_instruction_link: str,
) -> EnvironmentComponent:
    package_present = importlib.util.find_spec(package_name) is not None if package_name else False
    path_present = config_path.exists()
    if path_present:
        status = STATUS_CONFIGURED
        health = HEALTH_HEALTHY
        source = "filesystem"
    elif package_present:
        status = STATUS_FOUND
        health = HEALTH_WARN
        source = "python package"
    else:
        status = STATUS_NOT_FOUND if not required else STATUS_ACTION_REQUIRED
        health = HEALTH_UNKNOWN if not required else HEALTH_WARN
        source = "not detected"
    return EnvironmentComponent(
        name=name,
        category=category,
        status=status,
        health=health,
        version=package_name if package_present and package_name else "n/a",
        install_location=str(config_path) if path_present else "",
        configuration_source=source,
        required=required,
        dependencies=("Python",),
        last_checked=checked_at,
        last_changed=_path_mtime(config_path),
        recommended_action=(
            "No action required."
            if status == STATUS_CONFIGURED
            else f"Review {name} setup and complete configuration if needed."
        ),
        work_instruction_link=work_instruction_link,
    )


def _systemd_component(checked_at: str) -> EnvironmentComponent:
    executable = shutil.which("systemctl") or ""
    if not executable:
        return EnvironmentComponent(
            name="systemd",
            category="Services",
            status=STATUS_NOT_FOUND,
            health=HEALTH_UNKNOWN,
            version="n/a",
            install_location="",
            configuration_source="PATH lookup failed",
            required=False,
            dependencies=(),
            last_checked=checked_at,
            last_changed="",
            recommended_action="No action required on non-systemd hosts.",
            work_instruction_link="docs/deployment/POST_INSTALL_VALIDATION.md",
        )
    return EnvironmentComponent(
        name="systemd",
        category="Services",
        status=STATUS_FOUND,
        health=HEALTH_HEALTHY,
        version=_command_output(["systemctl", "--version"]).splitlines()[0] if executable else "n/a",
        install_location=executable,
        configuration_source="PATH lookup",
        required=False,
        dependencies=(),
        last_checked=checked_at,
        last_changed=_path_mtime(executable),
        recommended_action="Review service registration during VPS deployment.",
        work_instruction_link="docs/deployment/POST_INSTALL_VALIDATION.md",
    )


def _command_output(command: list[str]) -> str:
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except Exception:
        return "n/a"
    output = (result.stdout or result.stderr).strip()
    return output.splitlines()[0] if output else "n/a"


def _path_mtime(path_value: str | Path) -> str:
    if not path_value:
        return ""
    path = Path(path_value)
    if not path.exists():
        return ""
    return datetime.fromtimestamp(path.stat().st_mtime, UTC).isoformat()


def _environment_score(components: list[EnvironmentComponent]) -> int:
    if not components:
        return 0
    total = len(components) * 100
    score = 0
    for component in components:
        if component.status in {STATUS_CONFIGURED, STATUS_FOUND}:
            score += 100
        elif component.status == STATUS_DISABLED:
            score += 90
        elif component.status == STATUS_ACTION_REQUIRED:
            score += 50 if not component.required else 20
        elif component.status == STATUS_NOT_FOUND:
            score += 80 if not component.required else 0
        elif component.status == STATUS_ERROR:
            score += 0
    return max(0, min(100, round(score / len(components))))


def _yaml_key(name: str) -> str:
    return name.lower().replace(" ", "_").replace("/", "_")
