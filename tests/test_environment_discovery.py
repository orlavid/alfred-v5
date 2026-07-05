from datetime import UTC, datetime
from pathlib import Path
import json
import os
import subprocess
import sys

from src.operations.environment_discovery import (
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
    components = {component.name: component for component in inventory.components}

    assert components["Obsidian Vault"].status == STATUS_CONFIGURED
    assert components["Python"].status == STATUS_CONFIGURED
    assert "vault_path" in inventory.auto_configured
    assert components["OpenAI"].status == STATUS_CONFIGURED
    assert inventory.environment_score > 0
    assert inventory.trigger == DISCOVERY_TRIGGER_MANUAL
    assert DISCOVERY_TRIGGER_STARTUP in inventory.supported_triggers
    assert DISCOVERY_TRIGGER_DAILY in inventory.supported_triggers
    assert DISCOVERY_TRIGGER_BEFORE_OPERATIONAL_READINESS in inventory.supported_triggers


def test_environment_inventory_marks_missing_optional_provider_as_action_required(tmp_path, monkeypatch):
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")
    monkeypatch.setenv("ALFRED_LIVE_VAULT_PATH", str(vault))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    inventory = build_environment_inventory(root=tmp_path, install_root=tmp_path)
    components = {component.name: component for component in inventory.components}

    assert components["OpenRouter"].status == STATUS_ACTION_REQUIRED
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
    assert "obsidian_vault:" in rendered


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
    vault_component = next(component for component in previous["components"] if component["name"] == "Obsidian Vault")
    vault_component["health"] = "ERROR"
    vault_component["version"] = "old"
    vault_component["install_location"] = "/old/path"
    previous["components"].append(
        {
            "name": "Removed Service",
            "category": "Services",
            "status": "FOUND",
            "health": "HEALTHY",
            "version": "1.0",
            "install_location": "/tmp/removed",
            "configuration_source": "fixture",
            "required": False,
            "dependencies": [],
            "last_checked": inventory.generated_at,
            "last_changed": inventory.generated_at,
            "recommended_action": "None",
            "work_instruction_link": "docs/deployment/INSTALLATION_GUIDE.md",
        }
    )

    drift = compare_environment_inventory(previous, inventory.components)

    assert "Removed Service" in drift.removed_components
    assert "Obsidian Vault" in drift.configuration_changes
    assert "Obsidian Vault" in drift.version_changes
    assert "Obsidian Vault" in drift.health_changes


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
