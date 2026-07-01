from pathlib import Path
import json
from executive.knowledge.extractor import extract_entities
from executive.knowledge.resolver import build_resolution_index, resolve_link_with_index
from executive.knowledge.canonical_resolution import canonicalise_resolution_index
from executive.knowledge.preview_resolution import resolve_link_with_preview_policy

VAULT_ROOT = Path.home() / "Documents" / "My Vault" / "My Vault"

def main():
    entities = extract_entities(VAULT_ROOT)
    resolution_index = build_resolution_index(entities)
    canonical_index, _ = canonicalise_resolution_index(resolution_index)

    changed = []
    for entity in entities:
        for link in getattr(entity, "links", []):
            current = resolve_link_with_index(link, resolution_index)
            preview = resolve_link_with_preview_policy(link, resolution_index, canonical_index)

            current_id = getattr(current, "id", None) if current else None
            preview_id = getattr(preview, "id", None) if preview else None

            if current_id != preview_id:
                changed.append({
                    "source_id": getattr(entity, "id", None),
                    "source_title": getattr(entity, "title", None),
                    "raw_link": link,
                    "current_target_id": current_id,
                    "preview_target_id": preview_id,
                })

    out = Path("output")
    out.mkdir(exist_ok=True)

    json_path = out / "policy_aware_preview_report.json"
    json_path.write_text(json.dumps({
        "changed_target_count": len(changed),
        "changes": changed,
    }, indent=2))

    md_path = out / "policy_aware_preview_report.md"
    lines = [
        "# Policy-Aware Preview Resolution Report",
        "",
        f"Changed targets: **{len(changed)}**",
        "",
    ]
    for item in changed[:100]:
        lines.extend([
            f"## {item['raw_link']}",
            f"- Source: `{item['source_id']}`",
            f"- Source title: {item['source_title']}",
            f"- Current target: `{item['current_target_id']}`",
            f"- Preview target: `{item['preview_target_id']}`",
            "",
        ])
    md_path.write_text("\n".join(lines))

    print(json_path)
    print(md_path)

if __name__ == "__main__":
    main()
