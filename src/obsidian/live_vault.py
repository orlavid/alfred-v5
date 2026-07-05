"""Live Obsidian vault configuration and status helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from executive.knowledge.vault import load_vault
from src.knowledge.executive_knowledge_builder import DEFAULT_VAULT_ROOT

LIVE_VAULT_ENV_VAR = "ALFRED_LIVE_VAULT_PATH"
LEGACY_VAULT_ENV_VAR = "ALFRED_OBSIDIAN_VAULT"


@dataclass(frozen=True)
class LiveVaultStatus:
    vault_path: str
    source: str
    exists: bool
    markdown_files_processed: int
    status: str
    reason: str


def resolve_live_vault_path(vault_root: Path | None = None) -> Path:
    if vault_root is not None:
        return vault_root.expanduser()
    explicit = os.environ.get(LIVE_VAULT_ENV_VAR)
    if explicit:
        return Path(explicit).expanduser()
    legacy = os.environ.get(LEGACY_VAULT_ENV_VAR)
    if legacy:
        return Path(legacy).expanduser()
    return DEFAULT_VAULT_ROOT


def detect_live_vault_status(vault_root: Path | None = None) -> LiveVaultStatus:
    resolved = resolve_live_vault_path(vault_root)
    if vault_root is not None:
        source = "function_argument"
    elif os.environ.get(LIVE_VAULT_ENV_VAR):
        source = LIVE_VAULT_ENV_VAR
    elif os.environ.get(LEGACY_VAULT_ENV_VAR):
        source = LEGACY_VAULT_ENV_VAR
    else:
        source = "default"

    exists = resolved.exists() and resolved.is_dir()
    markdown_count = len(load_vault(resolved)) if exists else 0

    if not exists:
        return LiveVaultStatus(
            vault_path=str(resolved),
            source=source,
            exists=False,
            markdown_files_processed=0,
            status="FAIL",
            reason="Configured live vault path does not exist or is not a directory.",
        )
    if markdown_count == 0:
        return LiveVaultStatus(
            vault_path=str(resolved),
            source=source,
            exists=True,
            markdown_files_processed=0,
            status="FAIL",
            reason="Configured live vault contains no executive markdown notes after exclusions.",
        )
    return LiveVaultStatus(
        vault_path=str(resolved),
        source=source,
        exists=True,
        markdown_files_processed=markdown_count,
        status="PASS",
        reason="Configured live vault is readable and contains executive markdown notes.",
    )


def render_live_vault_status(status: LiveVaultStatus) -> str:
    return "\n".join(
        [
            "# Live Vault Status",
            "",
            f"- Vault path: {status.vault_path}",
            f"- Source: {status.source}",
            f"- Exists: {'yes' if status.exists else 'no'}",
            f"- Markdown files processed: {status.markdown_files_processed}",
            f"- Status: {status.status}",
            f"- Reason: {status.reason}",
            "",
        ]
    )
