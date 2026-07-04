"""Configured live Obsidian vault access for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from src.knowledge.executive_knowledge_builder import DEFAULT_EVIDENCE_ROOT, DEFAULT_VAULT_ROOT
from src.obsidian.file_watcher import FileWatchState, build_file_manifest, diff_file_manifests, load_watch_state

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
LIVE_VAULT_STATE_PATH = OUT / "Live_Vault_Refresh.json"
LIVE_VAULT_STATUS_PATH = OUT / "Live_Vault_Status.md"
VAULT_ENV_VAR = "ALFRED_OBSIDIAN_VAULT"


@dataclass(frozen=True)
class LiveVaultStatus:
    configured_vault_path: str
    active_source_root: str
    source_mode: str
    vault_exists: bool
    markdown_file_count: int
    changed_files: tuple[str, ...]
    startup_refresh_required: bool
    refresh_required: bool
    last_checked_at: str
    last_successful_refresh_at: str | None
    warnings: tuple[str, ...]


def detect_configured_vault_path() -> Path:
    override = os.environ.get(VAULT_ENV_VAR)
    if override:
        return Path(override).expanduser()
    return DEFAULT_VAULT_ROOT


def validate_vault_exists(vault_path: Path) -> bool:
    return vault_path.exists() and vault_path.is_dir()


def scan_markdown_files(root: Path) -> tuple[Path, ...]:
    if not root.exists():
        return ()
    return tuple(sorted(path for path in root.rglob("*.md") if path.is_file()))


def build_live_vault_status(
    *,
    evidence_root: Path | None = None,
    vault_root: Path | None = None,
    refresh_state_path: Path = LIVE_VAULT_STATE_PATH,
) -> LiveVaultStatus:
    from src.obsidian.file_watcher import utc_now_iso

    effective_evidence_root = evidence_root or DEFAULT_EVIDENCE_ROOT
    configured_path = vault_root or detect_configured_vault_path()
    vault_exists = validate_vault_exists(configured_path)
    live_files = scan_markdown_files(configured_path) if vault_exists else ()
    warnings: list[str] = []

    if vault_exists and live_files:
        source_mode = "live_vault"
        active_source_root = configured_path
        files = live_files
    else:
        source_mode = "evidence_inventory"
        active_source_root = effective_evidence_root
        files = scan_markdown_files(effective_evidence_root)
        if not vault_exists:
            warnings.append(f"Configured vault path does not exist: {configured_path}.")
        else:
            warnings.append(f"Configured vault path contains no markdown files: {configured_path}.")
        warnings.append(f"Falling back to evidence inventory at {effective_evidence_root}.")

    previous_state = load_watch_state(refresh_state_path)
    current_manifest = build_file_manifest(active_source_root, files)
    changed_files = _compute_changed_files(previous_state, active_source_root, current_manifest)
    startup_refresh_required = previous_state is None or previous_state.last_successful_refresh_at is None

    return LiveVaultStatus(
        configured_vault_path=str(configured_path),
        active_source_root=str(active_source_root),
        source_mode=source_mode,
        vault_exists=vault_exists,
        markdown_file_count=len(files),
        changed_files=changed_files,
        startup_refresh_required=startup_refresh_required,
        refresh_required=startup_refresh_required or bool(changed_files),
        last_checked_at=utc_now_iso(),
        last_successful_refresh_at=previous_state.last_successful_refresh_at if previous_state else None,
        warnings=tuple(warnings),
    )


def render_live_vault_status(status: LiveVaultStatus) -> str:
    parts = [
        "# Live Vault Status",
        "",
        f"- Configured Vault Path: {status.configured_vault_path}",
        f"- Active Source Root: {status.active_source_root}",
        f"- Source Mode: {status.source_mode}",
        f"- Vault Exists: {'YES' if status.vault_exists else 'NO'}",
        f"- Markdown Files: {status.markdown_file_count}",
        f"- Startup Refresh Required: {'YES' if status.startup_refresh_required else 'NO'}",
        f"- Refresh Required: {'YES' if status.refresh_required else 'NO'}",
        f"- Last Checked At: {status.last_checked_at}",
        f"- Last Successful Refresh At: {status.last_successful_refresh_at or 'NONE'}",
        "",
        "## Changed Files",
        "",
    ]
    if status.changed_files:
        parts.extend(f"- {item}" for item in status.changed_files)
    else:
        parts.append("_No changed files detected._")
    parts.extend(["", "## Warnings", ""])
    if status.warnings:
        parts.extend(f"- {item}" for item in status.warnings)
    else:
        parts.append("_None._")
    parts.append("")
    return "\n".join(parts)


def write_live_vault_status(status: LiveVaultStatus, output_path: Path = LIVE_VAULT_STATUS_PATH) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_live_vault_status(status))
    return output_path


def _compute_changed_files(
    previous_state: FileWatchState | None,
    active_source_root: Path,
    current_manifest: tuple[tuple[str, int], ...],
) -> tuple[str, ...]:
    if previous_state is None:
        return tuple(path for path, _stamp in current_manifest)
    if previous_state.source_root != str(active_source_root):
        return tuple(path for path, _stamp in current_manifest)
    return diff_file_manifests(previous_state.file_manifest, current_manifest)
