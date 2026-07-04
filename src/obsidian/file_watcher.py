"""File change tracking for live Obsidian refresh."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path
import json


@dataclass(frozen=True)
class FileWatchState:
    source_root: str
    last_checked_at: str
    last_successful_refresh_at: str | None
    file_manifest: tuple[tuple[str, int], ...]


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def build_file_manifest(root: Path, files: tuple[Path, ...]) -> tuple[tuple[str, int], ...]:
    manifest: list[tuple[str, int]] = []
    for file_path in sorted(files):
        manifest.append((str(file_path.relative_to(root)), file_path.stat().st_mtime_ns))
    return tuple(manifest)


def diff_file_manifests(
    previous_manifest: tuple[tuple[str, int], ...],
    current_manifest: tuple[tuple[str, int], ...],
) -> tuple[str, ...]:
    previous = dict(previous_manifest)
    current = dict(current_manifest)
    changed = {
        path
        for path in set(previous) | set(current)
        if previous.get(path) != current.get(path)
    }
    return tuple(sorted(changed))


def load_watch_state(path: Path) -> FileWatchState | None:
    if not path.exists():
        return None
    payload = json.loads(path.read_text())
    return FileWatchState(
        source_root=payload.get("source_root", ""),
        last_checked_at=payload.get("last_checked_at", ""),
        last_successful_refresh_at=payload.get("last_successful_refresh_at"),
        file_manifest=tuple((item[0], int(item[1])) for item in payload.get("file_manifest", [])),
    )


def save_watch_state(path: Path, state: FileWatchState) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "source_root": state.source_root,
                "last_checked_at": state.last_checked_at,
                "last_successful_refresh_at": state.last_successful_refresh_at,
                "file_manifest": list(state.file_manifest),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return path
