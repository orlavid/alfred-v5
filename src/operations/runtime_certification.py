"""Production runtime certification for deployed Alfred installs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen
import json
import os
import subprocess


@dataclass(frozen=True)
class RuntimeCheck:
    name: str
    status: str
    detail: str
    remediation: str


@dataclass(frozen=True)
class RuntimeCertification:
    overall_status: str
    install_root: str
    expected_commit: str
    checks: tuple[RuntimeCheck, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "overall_status": self.overall_status,
            "install_root": self.install_root,
            "expected_commit": self.expected_commit,
            "checks": [asdict(check) for check in self.checks],
        }


def build_runtime_certification(
    install_root: Path | None = None,
    *,
    expected_commit: str | None = None,
) -> RuntimeCertification:
    effective_install_root = (install_root or Path(os.environ.get("ALFRED_INSTALL_ROOT", "/opt/alfred"))).resolve()
    expected = expected_commit or os.environ.get("ALFRED_EXPECTED_COMMIT", "unknown")
    config = _read_config(effective_install_root / "config" / "config.yaml")
    build_info = _read_kv(effective_install_root / "runtime" / "BUILD_INFO")
    output_dir = Path(config.get("output", str(effective_install_root / "app" / "output")))
    host = config.get("host", "127.0.0.1")
    port = config.get("ui_port", "4173")
    state_summary = output_dir / "ExecutiveState_Summary.md"
    dashboard_json = output_dir / "Dashboard_Home.json"
    app_dir = effective_install_root / "app"
    venv_python = effective_install_root / ".venv" / "bin" / "python"
    checks = (
        _check_build_commit(build_info, expected),
        _check_python_layout(config, venv_python),
        _check_vault(config),
        _check_service_process(effective_install_root),
        _check_service_endpoint(host, port),
        _check_output_presence(state_summary, dashboard_json),
    )
    overall_status = "GREEN" if all(check.status == "PASS" for check in checks) else "RED"
    return RuntimeCertification(
        overall_status=overall_status,
        install_root=str(effective_install_root),
        expected_commit=expected,
        checks=checks,
    )


def render_runtime_certification(report: RuntimeCertification) -> str:
    lines = [
        "# Production Runtime Certification",
        "",
        f"- Overall Status: {report.overall_status}",
        f"- Install Root: {report.install_root}",
        f"- Expected Commit: {report.expected_commit}",
        "",
        "| Check | Status | Detail | Remediation |",
        "| --- | --- | --- | --- |",
    ]
    for check in report.checks:
        lines.append(f"| {check.name} | {check.status} | {check.detail} | {check.remediation} |")
    lines.append("")
    return "\n".join(lines)


def render_runtime_certification_json(report: RuntimeCertification) -> str:
    return json.dumps(report.as_dict(), indent=2, sort_keys=True)


def write_runtime_certification(report: RuntimeCertification, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / "Production_Runtime_Certification.md"
    json_path = output_dir / "Production_Runtime_Certification.json"
    markdown_path.write_text(render_runtime_certification(report))
    json_path.write_text(render_runtime_certification_json(report))
    return markdown_path, json_path


def _check_build_commit(build_info: dict[str, str], expected_commit: str) -> RuntimeCheck:
    actual = build_info.get("build_version", "unknown")
    tree_state = build_info.get("build_tree_state", "unknown")
    expected_known = expected_commit != "unknown"
    if expected_known:
        status = "PASS" if actual == expected_commit and tree_state == "clean" else "FAIL"
        detail = f"BUILD_INFO commit is {actual}; expected commit is {expected_commit}; tree state is {tree_state}."
    else:
        status = "PASS" if actual != "unknown" and tree_state == "clean" else "FAIL"
        detail = f"BUILD_INFO commit is {actual}; tree state is {tree_state}; no external expected commit was supplied."
    remediation = "Deploy only from a clean git worktree and pass ALFRED_BUILD_COMMIT/ALFRED_BUILD_TREE_STATE into the VPS install."
    return RuntimeCheck("Deployed commit matches expected commit", status, detail, remediation)


def _check_python_layout(config: dict[str, str], expected_python: Path) -> RuntimeCheck:
    actual = config.get("python_executable", "")
    status = "PASS" if actual == str(expected_python) and expected_python.exists() else "FAIL"
    detail = f"Configured python executable is {actual or 'missing'}; canonical runtime is {expected_python}."
    remediation = "Reinstall Alfred so /opt/alfred/.venv exists and paths.python_executable points to /opt/alfred/.venv/bin/python."
    return RuntimeCheck("Canonical Python runtime is active", status, detail, remediation)


def _check_vault(config: dict[str, str]) -> RuntimeCheck:
    vault = Path(config.get("vault", ""))
    status = "PASS" if str(vault) == "/docker/obsidian-vault" and vault.is_dir() and os.access(vault, os.R_OK) else "FAIL"
    detail = f"Configured vault path is {vault}."
    remediation = "Set paths.vault to /docker/obsidian-vault and ensure the directory is readable by Alfred."
    return RuntimeCheck("Live executive vault is configured and readable", status, detail, remediation)


def _check_service_process(install_root: Path) -> RuntimeCheck:
    service_active = _run(["systemctl", "is-active", "alfred.service"]).strip()
    ps_output = _run(["ps", "-Ao", "pid=,ppid=,etime=,command="])
    matching = [line.strip() for line in ps_output.splitlines() if str(install_root) in line]
    status = "PASS" if service_active == "active" and matching else "FAIL"
    detail = " ; ".join([f"service={service_active}"] + matching[:2]) or f"service={service_active}"
    remediation = "Run systemctl daemon-reload && systemctl enable --now alfred.service, then confirm the process command references /opt/alfred."
    return RuntimeCheck("alfred.service is running from /opt/alfred", status, detail, remediation)


def _check_service_endpoint(host: str, port: str) -> RuntimeCheck:
    url = f"http://{host}:{port}/"
    api_url = f"http://{host}:{port}/api/dashboard-home.json"
    try:
        with urlopen(url, timeout=5) as response:
            root_ok = response.status == 200
    except URLError:
        root_ok = False
    try:
        with urlopen(api_url, timeout=5) as response:
            api_ok = response.status == 200
    except URLError:
        api_ok = False
    status = "PASS" if root_ok and api_ok else "FAIL"
    detail = f"root={root_ok}; dashboard_api={api_ok}; host={host}; port={port}."
    remediation = "Restart alfred.service and verify dist/index.html plus dist/api/dashboard-home.json are present and being served."
    return RuntimeCheck("Dashboard runtime endpoint responds", status, detail, remediation)


def _check_output_presence(state_summary: Path, dashboard_json: Path) -> RuntimeCheck:
    status = "PASS" if state_summary.exists() and dashboard_json.exists() else "FAIL"
    detail = f"ExecutiveState summary present={state_summary.exists()}; dashboard json present={dashboard_json.exists()}."
    remediation = "Run build_executive_state.py and build_dashboard_api.py with the canonical runtime python before starting the service."
    return RuntimeCheck("Core runtime artefacts are present", status, detail, remediation)


def _read_config(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    section = None
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            section = line.rstrip(":")
            continue
        if indent != 2:
            continue
        stripped = line.strip()
        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        namespaced = f"{section}_{key}" if section else key
        values[namespaced] = value.strip()
        if key not in values:
            values[key] = value.strip()
    return values


def _read_kv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text().splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value
    return values


def _run(argv: list[str]) -> str:
    result = subprocess.run(argv, check=False, capture_output=True, text=True)
    return result.stdout.strip()
