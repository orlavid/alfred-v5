from datetime import UTC, datetime
from pathlib import Path
import json
import os
import subprocess
import sys

from src.operations.environment_discovery import (
    COMPONENT_ENVIRONMENT_INVENTORY,
    COMPONENT_KNOWLEDGE_LLM_WIKI,
    COMPONENT_KNOWLEDGE_SEMANTIC,
    COMPONENT_PROVIDER_OPENAI,
    COMPONENT_PROVIDER_OPENROUTER,
    COMPONENT_RUNTIME_PYTHON,
    COMPONENT_VAULT_PRIMARY,
    DISCOVERY_PROVIDERS,
    DISCOVERY_TRIGGER_BEFORE_OPERATIONAL_READINESS,
    DISCOVERY_TRIGGER_DAILY,
    DISCOVERY_TRIGGER_MANUAL,
    DISCOVERY_TRIGGER_STARTUP,
    STATUS_ACTION_REQUIRED,
    STATUS_CONFIGURED,
    build_doctor_summary,
    build_environment_inventory,
    compare_environment_inventory,
    get_component_by_id,
    render_detected_environment_yaml,
    write_environment_inventory,
)


def test_build_environment_inventory_detects_core_runtime_and_vault(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")
    monkeypatch.setenv("ALFRED_LIVE_VAULT_PATH", str(vault))
    monkeypatch.setenv("OPENAI_API_KEY", "present-only")

    inventory = build_environment_inventory(root=tmp_path, install_root=tmp_path, now=datetime(2026, 7, 5, tzinfo=UTC))
    components = {component.component_id: component for component in inventory.components}

    assert components[COMPONENT_VAULT_PRIMARY].status == STATUS_CONFIGURED
    assert components[COMPONENT_RUNTIME_PYTHON].status == STATUS_CONFIGURED
    assert "vault_path" in inventory.auto_configured
    assert components[COMPONENT_PROVIDER_OPENAI].status == STATUS_CONFIGURED
    assert inventory.environment_score > 0
    assert inventory.trigger == DISCOVERY_TRIGGER_MANUAL
    assert DISCOVERY_TRIGGER_STARTUP in inventory.supported_triggers
    assert DISCOVERY_TRIGGER_DAILY in inventory.supported_triggers
    assert DISCOVERY_TRIGGER_BEFORE_OPERATIONAL_READINESS in inventory.supported_triggers
    assert components[COMPONENT_VAULT_PRIMARY].depends_on == (COMPONENT_ENVIRONMENT_INVENTORY,)


def test_environment_inventory_marks_missing_optional_provider_as_action_required(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")
    monkeypatch.setenv("ALFRED_LIVE_VAULT_PATH", str(vault))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    inventory = build_environment_inventory(root=tmp_path, install_root=tmp_path)
    components = {component.component_id: component for component in inventory.components}

    assert components[COMPONENT_PROVIDER_OPENROUTER].status == STATUS_ACTION_REQUIRED
    assert any("OPENROUTER_API_KEY" in action for action in inventory.required_actions)


def test_environment_inventory_writes_persistent_outputs(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")
    monkeypatch.setenv("ALFRED_LIVE_VAULT_PATH", str(vault))

    inventory = build_environment_inventory(root=tmp_path, install_root=tmp_path)
    markdown_path, json_path = write_environment_inventory(inventory, output_dir=tmp_path / "output")

    assert markdown_path.exists()
    assert json_path.exists()
    payload = json.loads(json_path.read_text())
    assert "components" in payload
    assert "auto_configured" in payload


def test_render_detected_environment_yaml_contains_components_and_auto_configured(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")
    monkeypatch.setenv("ALFRED_LIVE_VAULT_PATH", str(vault))

    inventory = build_environment_inventory(root=tmp_path, install_root=tmp_path)
    rendered = render_detected_environment_yaml(inventory)

    assert "detected_environment:" in rendered
    assert "auto_configured:" in rendered
    assert "vault_primary:" in rendered


def test_build_doctor_summary_uses_environment_inventory(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")
    monkeypatch.setenv("ALFRED_LIVE_VAULT_PATH", str(vault))

    inventory = build_environment_inventory(root=tmp_path, install_root=tmp_path)
    summary = build_doctor_summary(inventory)

    assert "environment_score" in summary
    assert "summary_lines" in summary
    assert summary["summary_lines"][0].startswith("Environment Score:")
    assert COMPONENT_VAULT_PRIMARY in summary["healthy"]


def test_environment_discovery_uses_provider_architecture():
    provider_names = {provider.__class__.__name__ for provider in DISCOVERY_PROVIDERS}
    assert {
        "VaultDiscovery",
        "OllamaDiscovery",
        "OpenRouterDiscovery",
        "OpenAIDiscovery",
        "AnthropicDiscovery",
        "LlamaIndexDiscovery",
        "LLMWikiDiscovery",
        "SemanticDiscovery",
        "DockerDiscovery",
        "SystemdDiscovery",
        "PythonDiscovery",
        "NodeDiscovery",
    }.issubset(provider_names)


def test_environment_inventory_drift_detection_reports_changes(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")
    monkeypatch.setenv("ALFRED_LIVE_VAULT_PATH", str(vault))

    inventory = build_environment_inventory(root=tmp_path, install_root=tmp_path)
    previous = inventory.as_dict()
    vault_component = get_component_by_id(previous, COMPONENT_VAULT_PRIMARY)
    vault_component["health"] = "ERROR"
    vault_component["version"] = "old"
    vault_component["install_location"] = "/old/path"
    previous["components"].append(
        {
            "component_id": "service.removed_fixture",
            "name": "Removed Service",
            "category": "Services",
            "status": "FOUND",
            "health": "HEALTHY",
            "version": "1.0",
            "install_location": "/tmp/removed",
            "configuration_source": "fixture",
            "required": False,
            "depends_on": [],
            "last_checked": inventory.generated_at,
            "last_changed": inventory.generated_at,
            "recommended_action": "None",
            "work_instruction_link": "docs/deployment/INSTALLATION_GUIDE.md",
        }
    )

    drift = compare_environment_inventory(previous, inventory.components)

    assert "service.removed_fixture" in drift.removed_components
    assert COMPONENT_VAULT_PRIMARY in drift.configuration_changes
    assert COMPONENT_VAULT_PRIMARY in drift.version_changes
    assert COMPONENT_VAULT_PRIMARY in drift.health_changes


def test_environment_inventory_records_dependency_graph(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")
    monkeypatch.setenv("ALFRED_LIVE_VAULT_PATH", str(vault))

    inventory = build_environment_inventory(root=tmp_path, install_root=tmp_path)

    semantic = get_component_by_id(inventory, COMPONENT_KNOWLEDGE_SEMANTIC)
    llm_wiki = get_component_by_id(inventory, COMPONENT_KNOWLEDGE_LLM_WIKI)

    assert semantic is not None
    assert llm_wiki is not None
    assert COMPONENT_VAULT_PRIMARY in semantic.depends_on
    assert COMPONENT_VAULT_PRIMARY in llm_wiki.depends_on


def test_build_environment_inventory_script_generates_outputs():
    output_json = Path("output/Environment_Inventory.json")
    output_md = Path("output/Environment_Inventory.md")
    if output_json.exists():
        output_json.unlink()
    if output_md.exists():
        output_md.unlink()

    result = subprocess.run(
        [sys.executable, "build_environment_inventory.py"],
        check=False,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )

    assert result.returncode == 0
    assert output_json.exists()
    assert output_md.exists()
