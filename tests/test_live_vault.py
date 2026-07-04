from pathlib import Path

from src.obsidian.file_watcher import FileWatchState, build_file_manifest, diff_file_manifests, save_watch_state
from src.obsidian.live_vault import build_live_vault_status, detect_configured_vault_path, validate_vault_exists


def test_detect_configured_vault_path_uses_env(monkeypatch, tmp_path):
    vault_root = tmp_path / "vault"
    monkeypatch.setenv("ALFRED_OBSIDIAN_VAULT", str(vault_root))

    assert detect_configured_vault_path() == vault_root


def test_build_live_vault_status_detects_changed_files(tmp_path):
    vault_root = tmp_path / "vault"
    vault_root.mkdir()
    file_path = vault_root / "note.md"
    file_path.write_text("# Note")

    refresh_state_path = tmp_path / "refresh.json"
    initial_status = build_live_vault_status(vault_root=vault_root, refresh_state_path=refresh_state_path)

    assert initial_status.vault_exists is True
    assert initial_status.refresh_required is True
    assert "note.md" in initial_status.changed_files

    state = FileWatchState(
        source_root=str(vault_root),
        last_checked_at="2026-07-04T00:00:00Z",
        last_successful_refresh_at="2026-07-04T00:00:00Z",
        file_manifest=build_file_manifest(vault_root, (file_path,)),
    )
    save_watch_state(refresh_state_path, state)

    unchanged_status = build_live_vault_status(vault_root=vault_root, refresh_state_path=refresh_state_path)
    assert unchanged_status.refresh_required is False
    assert unchanged_status.changed_files == ()

    file_path.write_text("# Updated")
    changed_status = build_live_vault_status(vault_root=vault_root, refresh_state_path=refresh_state_path)
    assert changed_status.refresh_required is True
    assert changed_status.changed_files == ("note.md",)


def test_validate_vault_exists_and_manifest_diff(tmp_path):
    vault_root = tmp_path / "vault"
    vault_root.mkdir()
    first = vault_root / "a.md"
    first.write_text("a")
    second = vault_root / "b.md"
    second.write_text("b")

    assert validate_vault_exists(vault_root) is True

    manifest_a = build_file_manifest(vault_root, (first,))
    manifest_b = build_file_manifest(vault_root, (first, second))
    assert diff_file_manifests(manifest_a, manifest_b) == ("b.md",)
