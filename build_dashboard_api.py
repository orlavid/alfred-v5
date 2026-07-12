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

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    shutil.copytree(current_api_dir, PUBLIC, dirs_exist_ok=True)

    bootstrap = json.loads((current_api_dir / "dashboard-home.json").read_text())
    output = OUT / "Dashboard_Home.json"
    output.write_text(json.dumps(bootstrap, indent=2, sort_keys=True))
    print(output)
    print(json.dumps({
        "snapshot_version": result.version,
        "bootstrap_payload_size_bytes": result.bootstrap_size_bytes,
        "domain_payload_sizes": result.domain_sizes,
        "detail_domain_payload_sizes": {
            domain_name: {
                "count": len(items),
                "total_bytes": sum(items.values()),
                "max_bytes": max(items.values()) if items else 0,
            }
            for domain_name, items in result.detail_domain_sizes.items()
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
