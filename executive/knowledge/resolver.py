import re
from collections import defaultdict

CANONICAL_FOLDER_PRIORITY = [
    "09 Governance/",
    "03 Projects/",
    "04 Companies/",
    "02 People/",
    "01 Daily Logs/",
    "06 Systems/",
    "05 Knowledge/",
    "07 AI Memory/Entities/",
]

def normalise_name(value):
    value = value.lower().strip()
    value = re.sub(r"\.md$", "", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value

def canonical_rank(entity):
    for i, prefix in enumerate(CANONICAL_FOLDER_PRIORITY):
        if entity.path.startswith(prefix):
            return i
    return 999

def build_resolution_index(entities):
    index = defaultdict(list)

    for entity in entities:
        keys = {
            normalise_name(entity.title),
            normalise_name(entity.path.split("/")[-1]),
        }

        for alias in entity.aliases:
            keys.add(normalise_name(alias))

        for key in keys:
            if key:
                index[key].append(entity)

    return dict(index)

def choose_canonical(candidates):
    return sorted(candidates, key=lambda e: (canonical_rank(e), len(e.path), e.path))[0]

def resolve_link_with_index(link, index):
    candidates = index.get(normalise_name(link), [])
    if not candidates:
        return None
    return choose_canonical(candidates)

def auto_resolution_map_from_index(index):
    resolved = {}

    for key, candidates in index.items():
        if len(candidates) > 1:
            canonical = choose_canonical(candidates)
            resolved[key] = {
                "canonical": canonical.id,
                "variants": [e.id for e in candidates if e.id != canonical.id],
            }

    return resolved

def unresolved_links_with_index(entities, index):
    unresolved = []

    for entity in entities:
        for link in entity.links:
            if not resolve_link_with_index(link, index):
                unresolved.append({
                    "source": entity.title,
                    "source_path": entity.path,
                    "missing": link,
                })

    return unresolved

def resolution_summary_from_index(index):
    auto_map = auto_resolution_map_from_index(index)

    ambiguous = {
        k: [e.id for e in v]
        for k, v in index.items()
        if len(v) > 1
    }

    return {
        "resolution_keys": len(index),
        "ambiguous_keys": len(ambiguous),
        "auto_resolvable_keys": len(auto_map),
        "ambiguous_examples": dict(list(ambiguous.items())[:10]),
        "auto_resolution_examples": dict(list(auto_map.items())[:10]),
    }
