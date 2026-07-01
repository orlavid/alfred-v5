TYPE_PRIORITY = {
    "company": 1,
    "project": 1,
    "person": 1,
    "objective": 1,
    "daily_log": 2,
    "note": 3,
}

PATH_PRIORITY = [
    "04 Companies/",
    "03 Projects/",
    "02 People/",
    "01 Daily Logs/",
    "07 Executive Briefings/",
    "Suppliers/",
    "LLM Wiki/",
    "07 AI Memory/",
    "Phillip @FML/",
]

def path_rank(entity_id: str) -> int:
    for i, prefix in enumerate(PATH_PRIORITY):
        if entity_id.startswith(prefix):
            return i
    return len(PATH_PRIORITY)

def entity_rank(m):
    return (
        TYPE_PRIORITY.get(getattr(m, "type", "note"), 9),
        path_rank(getattr(m, "id", "")),
        len(getattr(m, "id", "")),
        getattr(m, "id", ""),
    )

def choose_canonical(matches):
    if not matches:
        return None
    ordered = sorted(matches, key=entity_rank)
    return ordered[0]

def canonicalise_resolution_index(resolution_index):
    canonical = {}
    ambiguous = {}
    for key, matches in resolution_index.items():
        if not isinstance(matches, list) or not matches:
            continue
        ordered = sorted(matches, key=entity_rank)
        chosen = ordered[0]
        canonical[key] = chosen
        if len(ordered) > 1:
            ambiguous[key] = ordered
    return canonical, ambiguous
