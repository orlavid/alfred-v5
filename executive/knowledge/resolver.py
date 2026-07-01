import re
from collections import defaultdict

def normalise_name(value):
    value = value.lower().strip()
    value = re.sub(r"\.md$", "", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value

def unresolved_links(entities):
    titles = {e.title for e in entities}
    unresolved = []

    for entity in entities:
        for link in entity.links:
            if link not in titles:
                unresolved.append({
                    "source": entity.title,
                    "source_path": entity.path,
                    "missing": link,
                })

    return unresolved

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
                index[key].append(entity.id)

    return dict(index)

def resolve_link(link, entities):
    index = build_resolution_index(entities)
    key = normalise_name(link)
    matches = index.get(key, [])

    return matches

def resolution_summary(entities):
    index = build_resolution_index(entities)
    ambiguous = {k: v for k, v in index.items() if len(v) > 1}

    return {
        "resolution_keys": len(index),
        "ambiguous_keys": len(ambiguous),
        "ambiguous_examples": dict(list(ambiguous.items())[:10]),
    }
