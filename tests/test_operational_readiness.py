from datetime import UTC, datetime, timedelta
from pathlib import Path
import json
import subprocess
import sys

from src.operations.config_registry import build_configuration_registry
from src.operations.doctor import build_operational_readiness, render_operational_readiness_json


def test_configuration_registry_declares_profiles_and_services(tmp_path):
    root = tmp_path / "repo"
    output = root / "output"
    package_json = root / "package.json"
    node_modules = root / "node_modules"
    vault = tmp_path / "vault"
    output.mkdir(parents=True)
    node_modules.mkdir(parents=True)
    vault.mkdir()
    package_json.write_text("{}")

    registry = build_configuration_registry(root, output_dir=output, vault_path=vault)

    assert registry.package_json_present is True
    assert registry.node_modules_present is True
    assert any(service.name == "LlamaIndex" for service in registry.optional_services)
    assert {profile.name for profile in registry.deployment_profiles} == {
        "Local Development",
        "Single Machine",
        "VPS",
        "Enterprise",
    }


def test_build_operational_readiness_reports_freshness_and_services(tmp_path):
    root = tmp_path / "repo"
    output = root / "output"
    package_json = root / "package.json"
    node_modules = root / "node_modules"
    venv_python = root / ".venv" / "bin" / "python"
    vault = tmp_path / "vault"
    output.mkdir(parents=True)
    node_modules.mkdir(parents=True)
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("")
    package_json.write_text("{}")
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")

    for name in (
        "Dashboard_Home.json",
        "ExecutiveState_Summary.md",
        "Executive_Reasoning.md",
        "Daily_Brief.md",
        "Executive_Knowledge.json",
        "Knowledge_Graph.json",
        "Executive_Pipeline_Report.md",
        "Live_Vault_Status.md",
        "LIVE_KNOWLEDGE_CERTIFICATION.md",
        "Knowledge_Certification.md",
        "Knowledge_Certification.json",
    ):
        (output / name).write_text("ok")

    fresh_state = output / "ExecutiveState_Summary.md"
    now = datetime(2026, 7, 4, 12, 0, tzinfo=UTC)
    fresh_timestamp = (now - timedelta(hours=2)).timestamp()
    fresh_state.touch()
    fresh_state.chmod(0o644)
    import os

    os.utime(fresh_state, (fresh_timestamp, fresh_timestamp))

    registry = build_configuration_registry(root, output_dir=output, vault_path=vault)
    report = build_operational_readiness(registry, output_dir=output, now=now)
    payload = json.loads(render_operational_readiness_json(report))
    checks = {check["name"]: check for check in payload["checks"]}

    assert report.freshness.status == "FRESH"
    assert checks["Python inventory"]["status"] == "PASS"
    assert checks["npm inventory"]["status"] == "PASS"
    assert checks["LlamaIndex inventory"]["status"] == "PASS"
    assert payload["overall_health"] == "GREEN"
    assert "environment_inventory" in payload
    assert "doctor_summary" in payload


def test_build_operational_readiness_uses_installed_config_vault_path(tmp_path, monkeypatch):
    install_root = tmp_path / "opt" / "alfred"
    app_root = install_root / "app"
    output = app_root / "output"
    config_dir = install_root / "config"
    vault = tmp_path / "vault"

    output.mkdir(parents=True)
    (app_root / "node_modules").mkdir(parents=True)
    (app_root / "package.json").write_text("{}")
    config_dir.mkdir(parents=True)
    vault.mkdir()
    (vault / "Daily.md").write_text("# Daily\n")

    config_dir.joinpath("config.yaml").write_text(
        f"""deployment:
  profile: VPS
paths:
  install_root: {install_root}
  app: {app_root}
  vault: {vault}
  output: {output}
python:
  executable: {sys.executable}
"""
    )

    for name in (
        "Dashboard_Home.json",
        "ExecutiveState_Summary.md",
        "Executive_Reasoning.md",
        "Daily_Brief.md",
        "Executive_Knowledge.json",
        "Knowledge_Graph.json",
        "Executive_Pipeline_Report.md",
        "Live_Vault_Status.md",
        "LIVE_KNOWLEDGE_CERTIFICATION.md",
        "Knowledge_Certification.md",
        "Knowledge_Certification.json",
        "Environment_Inventory.json",
        "Environment_Inventory.md",
    ):
        (output / name).write_text("ok")

    monkeypatch.delenv("ALFRED_LIVE_VAULT_PATH", raising=False)
    monkeypatch.delenv("ALFRED_OBSIDIAN_VAULT", raising=False)
    monkeypatch.delenv("ALFRED_CONFIG_FILE", raising=False)
    monkeypatch.setenv("ALFRED_INSTALL_ROOT", str(install_root))

    registry = build_configuration_registry(app_root, output_dir=output)
    report = build_operational_readiness(registry, output_dir=output, now=datetime(2026, 7, 4, 12, 0, tzinfo=UTC))
    checks = {check.name: check for check in report.checks}

    assert registry.configured_vault_path == str(vault)
    assert checks["Obsidian Vault inventory"].status == "PASS"
    assert report.overall_health == "GREEN"


def test_build_operational_readiness_generates_outputs():
    markdown_output = Path("output/Operational_Readiness_Report.md")
    json_output = Path("output/Operational_Readiness.json")
    if markdown_output.exists():
        markdown_output.unlink()
    if json_output.exists():
        json_output.unlink()

    result = subprocess.run(
        [sys.executable, "build_operational_readiness.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert markdown_output.exists()
    assert json_output.exists()
    assert "# Operational Readiness Report" in markdown_output.read_text()
    payload = json.loads(json_output.read_text())
    assert "overall_health" in payload
    assert "checks" in payload
