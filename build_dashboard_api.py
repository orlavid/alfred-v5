#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import json
import os
import shutil

from src.runtime.published_snapshot import SnapshotStore

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
PUBLIC = ROOT / "web" / "public" / "api"
OUT.mkdir(exist_ok=True)
PUBLIC.mkdir(parents=True, exist_ok=True)


def main() -> None:
    store = SnapshotStore(
        install_root=ROOT,
        evidence_root=ROOT / "evidence" / "alfred-inventory",
        vault_root=Path(os.environ.get("ALFRED_OBSIDIAN_VAULT", "/docker/obsidian-vault")),
    )
    result = store.publish_snapshot(trigger="build_dashboard_api")
    current_api_dir = store.current_snapshot_dir() / "api"

    for existing in PUBLIC.glob("*.json"):
        existing.unlink()
    for file in current_api_dir.glob("*.json"):
        shutil.copy2(file, PUBLIC / file.name)

    bootstrap = json.loads((current_api_dir / "dashboard-home.json").read_text())
    output = OUT / "Dashboard_Home.json"
    output.write_text(json.dumps(bootstrap, indent=2, sort_keys=True))
    print(output)
    print(json.dumps({
        "snapshot_version": result.version,
        "bootstrap_payload_size_bytes": result.bootstrap_size_bytes,
        "domain_payload_sizes": result.domain_sizes,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
