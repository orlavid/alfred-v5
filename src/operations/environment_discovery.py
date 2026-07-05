"""Provider-based environment discovery for Alfred platform management."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from typing import Iterable

from src.obsidian.live_vault import detect_live_vault_status

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
INVENTORY_JSON = OUT / "Environment_Inventory.json"
INVENTORY_MD = OUT / "Environment_Inventory.md"
PREVIOUS_INVENTORY_JSON = OUT / "Environment_Inventory.previous.json"

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

DISCOVERY_TRIGGER_MANUAL = "manual"
DISCOVERY_TRIGGER_STARTUP = "startup"
DISCOVERY_TRIGGER_DAILY = "daily"
DISCOVERY_TRIGGER_BEFORE_OPERATIONAL_READINESS = "before_operational_readiness"
DISCOVERY_TRIGGER_BEFORE_DEPLOYMENT = "before_deployment"
SUPPORTED_DISCOVERY_TRIGGERS = (
    DISCOVERY_TRIGGER_MANUAL,
    DISCOVERY_TRIGGER_STARTUP,
    DISCOVERY_TRIGGER_DAILY,
    DISCOVERY_TRIGGER_BEFORE_OPERATIONAL_READINESS,
    DISCOVERY_TRIGGER_BEFORE_DEPLOYMENT,
)


@dataclass(frozen=True)
class AutoConfiguredValue:
    value: str
    discovery_method: str
    confidence: str
    timestamp: str


@dataclass(frozen=True)
class EnvironmentComponent:
    component_id: str
    name: str
    category: str
    status: str
    health: str
    version: str
    install_location: str
    configuration_source: str
    required: bool
    depends_on: tuple[str, ...]
    last_checked: str
    last_changed: str
    recommended_action: str
    work_instruction_link: str


@dataclass(frozen=True)
class EnvironmentDrift:
    new_components: tuple[str, ...]
    removed_components: tuple[str, ...]
    configuration_changes: tuple[str, ...]
    version_changes: tuple[str, ...]
    health_changes: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class EnvironmentInventory:
    generated_at: str
    trigger: str
    supported_triggers: tuple[str, ...]
    environment_score: int
    components: tuple[EnvironmentComponent, ...]
    auto_configured: dict[str, AutoConfiguredValue]
    required_actions: tuple[str, ...]
    architecture_rule: str
    drift: EnvironmentDrift

    def as_dict(self) -> dict[str, object]:
        return {
            "generated_at": self.generated_at,
            "trigger": self.trigger,
            "supported_triggers": list(self.supported_triggers),
            "environment_score": self.environment_score,
            "components": [asdict(component) for component in self.components],
            "auto_configured": {key: asdict(value) for key, value in self.auto_configured.items()},
            "required_actions": list(self.required_actions),
            "architecture_rule": self.architecture_rule,
            "drift": self.drift.as_dict(),
        }


@dataclass(frozen=True)
class DiscoveryContext:
    root: Path
    install_root: Path
    vault_path: Path | None
    checked_at: str


@dataclass(frozen=True)
class ProviderResult:
    components: tuple[EnvironmentComponent, ...]
    auto_configured: dict[str, AutoConfiguredValue]


COMPONENT_ENVIRONMENT_INVENTORY = "environment.inventory"
COMPONENT_VAULT_PRIMARY = "vault.primary"
COMPONENT_RUNTIME_PYTHON = "runtime.python"
COMPONENT_RUNTIME_NODE = "runtime.node"
COMPONENT_RUNTIME_NPM = "runtime.npm"
COMPONENT_RUNTIME_DOCKER = "runtime.docker"
COMPONENT_SERVICE_SYSTEMD = "service.systemd"
COMPONENT_SERVICE_OLLAMA = "service.ollama"
COMPONENT_PROVIDER_OPENROUTER = "provider.openrouter"
COMPONENT_PROVIDER_OPENAI = "provider.openai"
COMPONENT_PROVIDER_ANTHROPIC = "provider.anthropic"
COMPONENT_KNOWLEDGE_LLAMAINDEX = "knowledge.llamaindex"
COMPONENT_KNOWLEDGE_LLM_WIKI = "knowledge.llm_wiki"
COMPONENT_KNOWLEDGE_SEMANTIC = "knowledge.semantic"
COMPONENT_RESEARCH_DEEP = "research.deep_research"

LEGACY_COMPONENT_IDS = {
    "Environment Inventory": COMPONENT_ENVIRONMENT_INVENTORY,
    "Obsidian Vault": COMPONENT_VAULT_PRIMARY,
    "Python": COMPONENT_RUNTIME_PYTHON,
    "Node": COMPONENT_RUNTIME_NODE,
    "npm": COMPONENT_RUNTIME_NPM,
    "Docker": COMPONENT_RUNTIME_DOCKER,
    "systemd": COMPONENT_SERVICE_SYSTEMD,
    "Ollama": COMPONENT_SERVICE_OLLAMA,
    "OpenRouter": COMPONENT_PROVIDER_OPENROUTER,
    "OpenAI": COMPONENT_PROVIDER_OPENAI,
    "Anthropic": COMPONENT_PROVIDER_ANTHROPIC,
    "LlamaIndex": COMPONENT_KNOWLEDGE_LLAMAINDEX,
    "LLM Wiki Enrichment": COMPONENT_KNOWLEDGE_LLM_WIKI,
    "Semantic Search": COMPONENT_KNOWLEDGE_SEMANTIC,
    "Deep Research": COMPONENT_RESEARCH_DEEP,
}


class DiscoveryProvider(ABC):
    @property
    def provider_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        raise NotImplementedError


class EnvironmentInventoryDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        component = EnvironmentComponent(
            component_id=COMPONENT_ENVIRONMENT_INVENTORY,
            name="Environment Inventory",
            category="Platform",
            status=STATUS_CONFIGURED,
            health=HEALTH_HEALTHY,
            version="v1",
            install_location=str(INVENTORY_JSON),
            configuration_source="platform registry",
            required=True,
            depends_on=(),
            last_checked=context.checked_at,
            last_changed=_path_mtime(INVENTORY_JSON),
            recommended_action="No action required.",
            work_instruction_link="docs/deployment/INSTALLATION_GUIDE.md",
        )
        return ProviderResult((component,), {})


class VaultDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        vault_status = detect_live_vault_status(context.vault_path)
        component = EnvironmentComponent(
            component_id=COMPONENT_VAULT_PRIMARY,
            name="Obsidian Vault",
            category="Vault",
            status=STATUS_CONFIGURED if vault_status.status == "PASS" else STATUS_ACTION_REQUIRED,
            health=HEALTH_HEALTHY if vault_status.status == "PASS" else HEALTH_WARN,
            version="n/a",
            install_location=vault_status.vault_path,
            configuration_source=vault_status.source,
            required=True,
            depends_on=(COMPONENT_ENVIRONMENT_INVENTORY,),
            last_checked=context.checked_at,
            last_changed=_path_mtime(vault_status.vault_path),
            recommended_action=(
                "Use the detected live vault path."
                if vault_status.status == "PASS"
                else "Provide a readable vault path with markdown files."
            ),
            work_instruction_link="docs/deployment/INSTALLATION_GUIDE.md",
        )
        auto = {}
        if vault_status.status == "PASS":
            auto["vault_path"] = AutoConfiguredValue(
                value=vault_status.vault_path,
                discovery_method=f"filesystem scan via {vault_status.source}",
                confidence="HIGH",
                timestamp=context.checked_at,
            )
        return ProviderResult((component,), auto)


class PythonDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        executable = sys.executable
        component = EnvironmentComponent(
            component_id=COMPONENT_RUNTIME_PYTHON,
            name="Python",
            category="Runtime",
            status=STATUS_CONFIGURED if Path(executable).exists() else STATUS_ERROR,
            health=HEALTH_HEALTHY if Path(executable).exists() else HEALTH_ERROR,
            version=_command_output([executable, "--version"]),
            install_location=executable,
            configuration_source="runtime interpreter",
            required=True,
            depends_on=(COMPONENT_ENVIRONMENT_INVENTORY,),
            last_checked=context.checked_at,
            last_changed=_path_mtime(executable),
            recommended_action="Use detected Python executable." if Path(executable).exists() else "Install Python 3 and re-run discovery.",
            work_instruction_link="docs/deployment/INSTALLATION_GUIDE.md",
        )
        return ProviderResult(
            (component,),
            {
                "python_executable": AutoConfiguredValue(
                    value=executable,
                    discovery_method="active Python runtime",
                    confidence="HIGH",
                    timestamp=context.checked_at,
                )
            },
        )


class NodeDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _command_pair_provider(
            checked_at=context.checked_at,
            first=(COMPONENT_RUNTIME_NODE, "Node", "node", True, "node_executable"),
            second=(COMPONENT_RUNTIME_NPM, "npm", "npm", True, "npm_executable"),
            work_instruction="docs/deployment/INSTALLATION_GUIDE.md",
        )


class DockerDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _single_command_provider(
            component_id=COMPONENT_RUNTIME_DOCKER,
            name="Docker",
            category="Runtime",
            command_name="docker",
            required=False,
            checked_at=context.checked_at,
            work_instruction="docs/deployment/POST_INSTALL_VALIDATION.md",
            auto_key="docker_executable",
        )


class SystemdDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _single_command_provider(
            component_id=COMPONENT_SERVICE_SYSTEMD,
            name="systemd",
            category="Services",
            command_name="systemctl",
            required=False,
            checked_at=context.checked_at,
            work_instruction="docs/deployment/POST_INSTALL_VALIDATION.md",
            auto_key=None,
        )


class OllamaDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _single_command_provider(
            component_id=COMPONENT_SERVICE_OLLAMA,
            name="Ollama",
            category="AI Providers",
            command_name="ollama",
            required=False,
            checked_at=context.checked_at,
            work_instruction="docs/deployment/INSTALLATION_GUIDE.md",
            auto_key="ollama_executable",
        )


class OpenRouterDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _api_key_provider(COMPONENT_PROVIDER_OPENROUTER, "OpenRouter", "OPENROUTER_API_KEY", context.checked_at)


class OpenAIDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _api_key_provider(COMPONENT_PROVIDER_OPENAI, "OpenAI", "OPENAI_API_KEY", context.checked_at)


class AnthropicDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _api_key_provider(COMPONENT_PROVIDER_ANTHROPIC, "Anthropic", "ANTHROPIC_API_KEY", context.checked_at)


class LlamaIndexDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _path_or_package_provider(
            component_id=COMPONENT_KNOWLEDGE_LLAMAINDEX,
            name="LlamaIndex",
            category="Knowledge Sources",
            package_name="llama_index",
            config_path=context.install_root / "config" / "llamaindex.yaml",
            required=False,
            checked_at=context.checked_at,
            work_instruction_link="docs/deployment/LLAMAINDEX_DEPLOYMENT.md",
            depends_on=(COMPONENT_RUNTIME_PYTHON, COMPONENT_VAULT_PRIMARY),
        )


class LLMWikiDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _path_or_package_provider(
            component_id=COMPONENT_KNOWLEDGE_LLM_WIKI,
            name="LLM Wiki Enrichment",
            category="Knowledge Sources",
            package_name=None,
            config_path=context.install_root / "config" / "llm_wiki_enrichment.yaml",
            required=False,
            checked_at=context.checked_at,
            work_instruction_link="docs/deployment/LLM_WIKI_ENRICHMENT.md",
            depends_on=(COMPONENT_VAULT_PRIMARY,),
        )


class SemanticDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        return _path_or_package_provider(
            component_id=COMPONENT_KNOWLEDGE_SEMANTIC,
            name="Semantic Search",
            category="Knowledge Sources",
            package_name=None,
            config_path=context.install_root / "data" / "semantic-index",
            required=False,
            checked_at=context.checked_at,
            work_instruction_link="docs/deployment/POST_INSTALL_VALIDATION.md",
            depends_on=(COMPONENT_VAULT_PRIMARY,),
        )


class DeepResearchDiscovery(DiscoveryProvider):
    def discover(self, context: DiscoveryContext) -> ProviderResult:
        component = EnvironmentComponent(
            component_id=COMPONENT_RESEARCH_DEEP,
            name="Deep Research",
            category="AI Providers",
            status=STATUS_DISABLED,
            health=HEALTH_UNKNOWN,
            version="n/a",
            install_location="",
            configuration_source="product policy",
            required=False,
            depends_on=(COMPONENT_PROVIDER_OPENROUTER, COMPONENT_PROVIDER_OPENAI, COMPONENT_PROVIDER_ANTHROPIC),
            last_checked=context.checked_at,
            last_changed="",
            recommended_action="Enable only after explicit approval and budget controls are in place.",
            work_instruction_link="docs/deployment/DEEP_RESEARCH_CONFIGURATION.md",
        )
        return ProviderResult((component,), {})


DISCOVERY_PROVIDERS: tuple[DiscoveryProvider, ...] = (
    EnvironmentInventoryDiscovery(),
    VaultDiscovery(),
    OllamaDiscovery(),
    OpenRouterDiscovery(),
    OpenAIDiscovery(),
    AnthropicDiscovery(),
    LlamaIndexDiscovery(),
    LLMWikiDiscovery(),
    SemanticDiscovery(),
    DockerDiscovery(),
    SystemdDiscovery(),
    PythonDiscovery(),
    NodeDiscovery(),
    DeepResearchDiscovery(),
)


def build_environment_inventory(
    *,
    root: Path | None = None,
    install_root: Path | None = None,
    vault_path: Path | None = None,
    now: datetime | None = None,
    trigger: str = DISCOVERY_TRIGGER_MANUAL,
    previous_inventory: dict[str, object] | None = None,
) -> EnvironmentInventory:
    if trigger not in SUPPORTED_DISCOVERY_TRIGGERS:
        raise ValueError(f"Unsupported discovery trigger: {trigger}")

    effective_root = root or ROOT
    effective_install_root = install_root or effective_root
    checked_at = (now or datetime.now(UTC)).isoformat()
    context = DiscoveryContext(
        root=effective_root,
        install_root=effective_install_root,
        vault_path=vault_path,
        checked_at=checked_at,
    )

    components: list[EnvironmentComponent] = []
    auto_configured: dict[str, AutoConfiguredValue] = {}
    for provider in DISCOVERY_PROVIDERS:
        result = provider.discover(context)
        components.extend(result.components)
        auto_configured.update(result.auto_configured)

    components.sort(key=lambda item: (item.category, item.required is False, item.component_id))
    required_actions = tuple(
        f"{component.component_id}: {component.recommended_action}"
        for component in components
        if component.status in {STATUS_ACTION_REQUIRED, STATUS_ERROR}
    )
    previous = previous_inventory if previous_inventory is not None else load_environment_inventory()
    drift = compare_environment_inventory(previous, components)

    return EnvironmentInventory(
        generated_at=checked_at,
        trigger=trigger,
        supported_triggers=SUPPORTED_DISCOVERY_TRIGGERS,
        environment_score=_environment_score(list(components)),
        components=tuple(components),
        auto_configured=auto_configured,
        required_actions=required_actions,
        architecture_rule="Alfred should never ask the user for information it can discover automatically.",
        drift=drift,
    )


def load_environment_inventory(path: Path | None = None) -> dict[str, object] | None:
    candidate = path or INVENTORY_JSON
    if not candidate.exists():
        return None
    try:
        return json.loads(candidate.read_text())
    except Exception:
        return None


def get_component_by_id(
    inventory: EnvironmentInventory | dict[str, object],
    component_id: str,
) -> EnvironmentComponent | dict[str, object] | None:
    components = inventory.components if isinstance(inventory, EnvironmentInventory) else inventory.get("components", [])
    for component in components:
        if isinstance(component, EnvironmentComponent) and component.component_id == component_id:
            return component
        if isinstance(component, dict) and _component_id_from_payload(component) == component_id:
            return component
    return None


def compare_environment_inventory(
    previous_inventory: dict[str, object] | None,
    current_components: Iterable[EnvironmentComponent],
) -> EnvironmentDrift:
    previous_components = {
        _component_id_from_payload(component): component
        for component in (previous_inventory or {}).get("components", [])
        if _component_id_from_payload(component)
    }
    current_component_map = {component.component_id: component for component in current_components}

    new_components = sorted(component_id for component_id in current_component_map if component_id not in previous_components)
    removed_components = sorted(component_id for component_id in previous_components if component_id not in current_component_map)
    configuration_changes: list[str] = []
    version_changes: list[str] = []
    health_changes: list[str] = []

    for component_id, component in current_component_map.items():
        previous = previous_components.get(component_id)
        if previous is None:
            continue
        if previous.get("install_location") != component.install_location or previous.get("configuration_source") != component.configuration_source:
            configuration_changes.append(component_id)
        if previous.get("version") != component.version:
            version_changes.append(component_id)
        if previous.get("health") != component.health or previous.get("status") != component.status:
            health_changes.append(component_id)

    return EnvironmentDrift(
        new_components=tuple(sorted(new_components)),
        removed_components=tuple(sorted(removed_components)),
        configuration_changes=tuple(sorted(configuration_changes)),
        version_changes=tuple(sorted(version_changes)),
        health_changes=tuple(sorted(health_changes)),
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
    previous_path = effective_output_dir / PREVIOUS_INVENTORY_JSON.name
    if json_path.exists():
        previous_path.write_text(json_path.read_text())
    json_path.write_text(json.dumps(inventory.as_dict(), indent=2, sort_keys=True))
    md_path.write_text(render_environment_inventory_markdown(inventory))
    return md_path, json_path


def render_environment_inventory_markdown(inventory: EnvironmentInventory) -> str:
    lines = [
        "# Environment Inventory",
        "",
        f"- Generated At: {inventory.generated_at}",
        f"- Trigger: {inventory.trigger}",
        f"- Supported Triggers: {', '.join(inventory.supported_triggers)}",
        f"- Environment Score: {inventory.environment_score}%",
        f"- Architecture Rule: {inventory.architecture_rule}",
        "",
        "| Component ID | Name | Category | Status | Health | Version | Location | Config Source | Depends On | Required | Recommended Action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for component in inventory.components:
        lines.append(
            f"| {component.component_id} | {component.name} | {component.category} | {component.status} | {component.health} | "
            f"{component.version or 'n/a'} | {component.install_location or '-'} | "
            f"{component.configuration_source or '-'} | {', '.join(component.depends_on) or '-'} | {'Required' if component.required else 'Optional'} | "
            f"{component.recommended_action} |"
        )
    lines.extend(["", "## Auto Configured", ""])
    for key, value in sorted(inventory.auto_configured.items()):
        lines.append(f"- {key}: {value.value} | {value.discovery_method} | {value.confidence} | {value.timestamp}")
    lines.extend(["", "## Required Actions", ""])
    if inventory.required_actions:
        lines.extend([f"- {action}" for action in inventory.required_actions])
    else:
        lines.append("- None.")
    lines.extend(["", "## Drift Detection", ""])
    lines.append(f"- New Components: {', '.join(inventory.drift.new_components) or 'None'}")
    lines.append(f"- Removed Components: {', '.join(inventory.drift.removed_components) or 'None'}")
    lines.append(f"- Configuration Changes: {', '.join(inventory.drift.configuration_changes) or 'None'}")
    lines.append(f"- Version Changes: {', '.join(inventory.drift.version_changes) or 'None'}")
    lines.append(f"- Health Changes: {', '.join(inventory.drift.health_changes) or 'None'}")
    lines.append("")
    return "\n".join(lines)


def render_detected_environment_yaml(inventory: EnvironmentInventory) -> str:
    lines = ["detected_environment:"]
    for component in inventory.components:
        key = _yaml_key(component.component_id)
        lines.extend(
            [
                f"  {key}:",
                f"    component_id: {component.component_id}",
                f"    name: {component.name}",
                f"    category: {component.category}",
                f"    status: {component.status}",
                f"    health: {component.health}",
                f"    version: {component.version or 'n/a'}",
                f"    install_location: {component.install_location or ''}",
                f"    configuration_source: {component.configuration_source or ''}",
                f"    required: {'true' if component.required else 'false'}",
                f"    depends_on: [{', '.join(component.depends_on)}]",
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
    summary_lines.extend([f"✓ {component.name}" for component in healthy[:5]])
    summary_lines.extend([f"⚠ {component.name} {component.recommended_action}" for component in warnings[:5]])
    summary_lines.extend([f"- {component.name} disabled by policy" for component in disabled[:3]])
    return {
        "environment_score": inventory.environment_score,
        "healthy": [component.component_id for component in healthy],
        "warnings": [component.component_id for component in warnings],
        "disabled": [component.component_id for component in disabled],
        "recommended_actions": list(inventory.required_actions[:8]),
        "summary_lines": summary_lines,
    }


def _single_command_provider(
    *,
    component_id: str,
    name: str,
    category: str,
    command_name: str,
    required: bool,
    checked_at: str,
    work_instruction: str,
    auto_key: str | None,
) -> ProviderResult:
    executable = shutil.which(command_name) or ""
    status = STATUS_CONFIGURED if executable else (STATUS_ACTION_REQUIRED if required else STATUS_NOT_FOUND)
    health = HEALTH_HEALTHY if executable else (HEALTH_WARN if required else HEALTH_UNKNOWN)
    component = EnvironmentComponent(
        component_id=component_id,
        name=name,
        category=category,
        status=status,
        health=health,
        version=_command_output([command_name, "--version"]) if executable else "n/a",
        install_location=executable,
        configuration_source="PATH discovery" if executable else "PATH discovery failed",
        required=required,
        depends_on=(COMPONENT_ENVIRONMENT_INVENTORY,),
        last_checked=checked_at,
        last_changed=_path_mtime(executable),
        recommended_action=f"Use detected {name} executable." if executable else f"Install or configure {name}.",
        work_instruction_link=work_instruction,
    )
    auto = {}
    if executable and auto_key is not None:
        auto[auto_key] = AutoConfiguredValue(
            value=executable,
            discovery_method="PATH lookup",
            confidence="HIGH",
            timestamp=checked_at,
        )
    return ProviderResult((component,), auto)


def _command_pair_provider(
    *,
    checked_at: str,
    first: tuple[str, str, str, bool, str],
    second: tuple[str, str, str, bool, str],
    work_instruction: str,
) -> ProviderResult:
    first_result = _single_command_provider(
        component_id=first[0],
        name=first[1],
        category="Runtime",
        command_name=first[2],
        required=first[3],
        checked_at=checked_at,
        work_instruction=work_instruction,
        auto_key=first[4],
    )
    second_result = _single_command_provider(
        component_id=second[0],
        name=second[1],
        category="Runtime",
        command_name=second[2],
        required=second[3],
        checked_at=checked_at,
        work_instruction=work_instruction,
        auto_key=second[4],
    )
    return ProviderResult(first_result.components + second_result.components, {**first_result.auto_configured, **second_result.auto_configured})


def _api_key_provider(component_id: str, name: str, env_var: str, checked_at: str) -> ProviderResult:
    present = bool(os.environ.get(env_var))
    component = EnvironmentComponent(
        component_id=component_id,
        name=name,
        category="AI Providers",
        status=STATUS_CONFIGURED if present else STATUS_ACTION_REQUIRED,
        health=HEALTH_HEALTHY if present else HEALTH_WARN,
        version="n/a",
        install_location="",
        configuration_source=env_var if present else f"{env_var} not set",
        required=False,
        depends_on=(COMPONENT_ENVIRONMENT_INVENTORY,),
        last_checked=checked_at,
        last_changed="",
        recommended_action="No action required." if present else f"Add {env_var} through a secure secret store.",
        work_instruction_link="docs/deployment/INSTALLATION_GUIDE.md",
    )
    return ProviderResult((component,), {})


def _path_or_package_provider(
    *,
    component_id: str,
    name: str,
    category: str,
    package_name: str | None,
    config_path: Path,
    required: bool,
    checked_at: str,
    work_instruction_link: str,
    depends_on: tuple[str, ...],
) -> ProviderResult:
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
    component = EnvironmentComponent(
        component_id=component_id,
        name=name,
        category=category,
        status=status,
        health=health,
        version=package_name if package_present and package_name else "n/a",
        install_location=str(config_path) if path_present else "",
        configuration_source=source,
        required=required,
        depends_on=depends_on,
        last_checked=checked_at,
        last_changed=_path_mtime(config_path),
        recommended_action=("No action required." if status == STATUS_CONFIGURED else f"Review {name} setup and complete configuration if needed."),
        work_instruction_link=work_instruction_link,
    )
    return ProviderResult((component,), {})


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
    return max(0, min(100, round(score / len(components))))


def _yaml_key(name: str) -> str:
    return name.lower().replace(" ", "_").replace("/", "_").replace(".", "_")


def _component_id_from_payload(component: dict[str, object]) -> str | None:
    component_id = component.get("component_id")
    if isinstance(component_id, str) and component_id:
        return component_id
    name = component.get("name")
    if isinstance(name, str):
        return LEGACY_COMPONENT_IDS.get(name)
    return None
