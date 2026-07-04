from pathlib import Path
import os
import shutil
import subprocess
import sys
import tarfile

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


def test_install_script_requires_explicit_source_mode(tmp_path):
    script = Path("scripts/install/install_alfred_platform.sh")
    result = subprocess.run(
        ["bash", str(script)],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "ALFRED_INSTALL_ROOT": str(tmp_path / "install")},
    )

    assert result.returncode != 0
    assert "install mode is required" in result.stderr


def test_install_script_rejects_invalid_source_structure(tmp_path):
    invalid_source = tmp_path / "invalid-source"
    invalid_source.mkdir()

    result = _run_installer(
        Path("scripts/install/install_alfred_platform.sh"),
        tmp_path / "install",
        "--mode",
        "local",
        "--source-dir",
        str(invalid_source),
    )

    assert result.returncode != 0
    assert "invalid Alfred source" in result.stderr


def test_install_script_supports_standalone_local_source_install(tmp_path):
    source = _create_fake_alfred_source(tmp_path / "source")
    install_root = tmp_path / "install"
    installer_copy = tmp_path / "standalone-install.sh"
    shutil.copy2("scripts/install/install_alfred_platform.sh", installer_copy)

    result = _run_installer(
        installer_copy,
        install_root,
        "--mode",
        "local",
        "--source-dir",
        str(source),
    )

    assert result.returncode == 0, result.stderr
    assert (install_root / "app" / "build_everything.py").exists()
    assert (install_root / "config" / "config.yaml").exists()
    build_info = (install_root / "runtime" / "BUILD_INFO").read_text()
    assert "installed_mode=local" in build_info
    assert f"installed_from={source.resolve()}" in build_info


def test_install_script_supports_tarball_mode(tmp_path):
    source = _create_fake_alfred_source(tmp_path / "source")
    tarball = tmp_path / "alfred-release.tar.gz"
    with tarfile.open(tarball, "w:gz") as archive:
        archive.add(source, arcname="alfred-release")

    install_root = tmp_path / "install"
    result = _run_installer(
        Path("scripts/install/install_alfred_platform.sh"),
        install_root,
        "--mode",
        "tarball",
        "--tarball",
        str(tarball),
    )

    assert result.returncode == 0, result.stderr
    assert (install_root / "app" / "build_everything.py").exists()
    assert "installed_mode=tarball" in (install_root / "runtime" / "BUILD_INFO").read_text()


def test_install_script_supports_git_mode(tmp_path):
    source = _create_fake_alfred_source(tmp_path / "source")
    subprocess.run(["git", "init"], cwd=source, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "alfred@example.com"], cwd=source, check=True)
    subprocess.run(["git", "config", "user.name", "Alfred"], cwd=source, check=True)
    subprocess.run(["git", "add", "."], cwd=source, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=source, check=True, capture_output=True, text=True)

    install_root = tmp_path / "install"
    result = _run_installer(
        Path("scripts/install/install_alfred_platform.sh"),
        install_root,
        "--mode",
        "git",
        "--git-url",
        str(source),
    )

    assert result.returncode == 0, result.stderr
    assert (install_root / "app" / "build_everything.py").exists()
    assert "installed_mode=git" in (install_root / "runtime" / "BUILD_INFO").read_text()


def test_install_script_rejects_destination_inside_source_tree(tmp_path):
    source = _create_fake_alfred_source(tmp_path / "source")
    install_root = source / "nested-install"

    result = _run_installer(
        Path("scripts/install/install_alfred_platform.sh"),
        install_root,
        "--mode",
        "local",
        "--source-dir",
        str(source),
    )

    assert result.returncode != 0
    assert "refusing recursive self-copy" in result.stderr


def _run_installer(script: Path, install_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "ALFRED_INSTALL_ROOT": str(install_root),
        "ALFRED_OBSIDIAN_VAULT": str(install_root.parent / "vault"),
    }
    Path(env["ALFRED_OBSIDIAN_VAULT"]).mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        ["bash", str(script), *args],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def _create_fake_alfred_source(root: Path) -> Path:
    (root / "src").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "scripts" / "install").mkdir(parents=True)
    (root / "build_everything.py").write_text("print('ok')\n")
    (root / "package.json").write_text("{}\n")
    (root / "src" / "__init__.py").write_text("")
    (root / "tests" / "test_placeholder.py").write_text("def test_placeholder():\n    assert True\n")
    (root / "scripts" / "install" / "configure_alfred.sh").write_text(
        Path("scripts/install/configure_alfred.sh").read_text()
    )
    (root / "scripts" / "install" / "start_alfred.sh").write_text("#!/bin/bash\nexit 0\n")
    (root / "scripts" / "install" / "install_alfred_platform.sh").write_text("# placeholder\n")
    return root
