from executive.knowledge.canonical_resolution import canonicalise_resolution_index
from executive.knowledge.resolution_rule_policy import get_resolution_rule

APPROVE_RULES = {
    "approve_person_alias",
    "prefer_system_record",
}

def build_preview_resolution_index(resolution_index):
    canonical_index, ambiguous = canonicalise_resolution_index(resolution_index)
    preview_index = {}

    for key, matches in resolution_index.items():
        if not isinstance(matches, list) or not matches:
            preview_index[key] = matches
            continue

        raw_link = None
        if matches and hasattr(matches[0], "title"):
            raw_link = matches[0].title

        preview_index[key] = matches

    return preview_index, ambiguous

def apply_preview_rule(raw_link, current_matches, canonical_match):
    rule = get_resolution_rule(raw_link)

    if rule in APPROVE_RULES and canonical_match is not None:
        return [canonical_match]

    return current_matches
