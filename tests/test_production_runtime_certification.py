import os
from pathlib import Path

from src.operations.runtime_certification import build_runtime_certification


class _Response:
    def __init__(self, status: int):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_runtime_certification_passes_with_canonical_layout(tmp_path, monkeypatch):
    install_root = tmp_path / "opt" / "alfred"
    app = install_root / "app"
    output = app / "output"
    config_dir = install_root / "config"
    runtime_dir = install_root / "runtime"
    venv_python = install_root / ".venv" / "bin" / "python"

    output.mkdir(parents=True)
    config_dir.mkdir(parents=True)
    runtime_dir.mkdir(parents=True)
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("")
    venv_python.chmod(0o755)
    (output / "ExecutiveState_Summary.md").write_text("ok")
    (output / "Dashboard_Home.json").write_text("{}")
    (runtime_dir / "BUILD_INFO").write_text("build_version=abc123\nbuild_tree_state=clean\n")
    real_is_dir = Path.is_dir
    monkeypatch.setattr(
        Path,
        "is_dir",
        lambda self: True if str(self) == "/docker/obsidian-vault" else real_is_dir(self),
    )
    monkeypatch.setattr(
        "src.operations.runtime_certification.os.access",
        lambda path, mode: True if str(path) == "/docker/obsidian-vault" else os.access(path, mode),
    )
    (config_dir / "config.yaml").write_text(
        f"""paths:
  vault: /docker/obsidian-vault
python:
  executable: {venv_python}
runtime:
  host: 127.0.0.1
  ui_port: 4173
  output: {output}
"""
    )

    monkeypatch.setattr("src.operations.runtime_certification.urlopen", lambda *args, **kwargs: _Response(200))
    monkeypatch.setattr(
        "src.operations.runtime_certification._run",
        lambda argv: "active" if argv[:2] == ["systemctl", "is-active"] else f"123 1 00:10:00 {install_root}/app/scripts/install/run_alfred_service.sh",
    )

    report = build_runtime_certification(install_root, expected_commit="abc123")

    assert report.overall_status == "GREEN"
    assert all(check.status == "PASS" for check in report.checks)


def test_runtime_certification_fails_for_noncanonical_runtime(tmp_path, monkeypatch):
    install_root = tmp_path / "opt" / "alfred"
    app = install_root / "app"
    output = app / "output"
    config_dir = install_root / "config"
    runtime_dir = install_root / "runtime"

    output.mkdir(parents=True)
    config_dir.mkdir(parents=True)
    runtime_dir.mkdir(parents=True)
    (output / "ExecutiveState_Summary.md").write_text("ok")
    (runtime_dir / "BUILD_INFO").write_text("build_version=wrong\nbuild_tree_state=dirty\n")
    (config_dir / "config.yaml").write_text(
        """paths:
  vault: /wrong/vault
python:
  executable: /usr/bin/python3
runtime:
  host: 127.0.0.1
  ui_port: 4173
"""
    )

    monkeypatch.setattr("src.operations.runtime_certification.urlopen", lambda *args, **kwargs: _Response(404))
    monkeypatch.setattr(
        "src.operations.runtime_certification._run",
        lambda argv: "inactive" if argv[:2] == ["systemctl", "is-active"] else "",
    )

    report = build_runtime_certification(install_root, expected_commit="abc123")
    statuses = {check.name: check.status for check in report.checks}

    assert report.overall_status == "RED"
    assert statuses["Deployed commit matches expected commit"] == "FAIL"
    assert statuses["Canonical Python runtime is active"] == "FAIL"
    assert statuses["alfred.service is running from /opt/alfred"] == "FAIL"
