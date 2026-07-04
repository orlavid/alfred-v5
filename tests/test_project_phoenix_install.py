from pathlib import Path

from src.operations.config_registry import build_deployment_profiles


def test_install_scripts_and_docs_exist():
    expected = [
        Path("scripts/install/install_alfred_platform.sh"),
        Path("scripts/install/configure_alfred.sh"),
        Path("scripts/install/start_alfred.sh"),
        Path("scripts/install/stop_alfred.sh"),
        Path("scripts/install/status_alfred.sh"),
        Path("scripts/install/uninstall_alfred.sh"),
        Path("docs/deployment/INSTALLATION_GUIDE.md"),
        Path("docs/deployment/POST_INSTALL_VALIDATION.md"),
    ]

    for path in expected:
        assert path.exists(), path


def test_install_scripts_reference_opt_alfred_and_config_yaml():
    install_script = Path("scripts/install/install_alfred_platform.sh").read_text()
    configure_script = Path("scripts/install/configure_alfred.sh").read_text()
    status_script = Path("scripts/install/status_alfred.sh").read_text()
    uninstall_script = Path("scripts/install/uninstall_alfred.sh").read_text()

    assert "/opt/alfred" in install_script
    assert "config.yaml" in configure_script
    assert "Build version" in status_script
    assert "ExecutiveState freshness" in status_script
    assert "Dashboard API" in status_script
    assert "UI status" in status_script
    assert "Optional services" in status_script
    assert "Obsidian vault untouched" in uninstall_script
    assert "Cloudflare untouched" in uninstall_script
    assert "Telegram untouched" in uninstall_script


def test_deployment_profiles_include_gate2_targets():
    names = {profile.name for profile in build_deployment_profiles()}
    assert names == {"Local Development", "Single Machine", "VPS", "Enterprise"}


def test_post_install_validation_contains_required_checks():
    content = Path("docs/deployment/POST_INSTALL_VALIDATION.md").read_text()
    required = [
        "UI starts",
        "Dashboard loads",
        "ExecutiveState builds",
        "Pipeline succeeds",
        "Daily Brief generated",
        "Dashboard API generated",
        "Operational Readiness green",
    ]
    for item in required:
        assert item in content
