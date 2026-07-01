from executive.knowledge.canonical_resolution import canonicalise_resolution_index
from executive.knowledge.resolution_rule_policy import get_resolution_rule
from executive.knowledge.resolver import resolve_link_with_index

APPROVE_RULES = {
    "approve_person_alias",
    "prefer_system_record",
}

def normalise_link_key(link: str) -> str:
    import re
    key = (link or "").strip().lower()
    key = re.sub(r"[^a-z0-9 ]", " ", key)
    key = re.sub(r"\s+", " ", key).strip()
    return key

def apply_preview_rule(raw_link, current_resolved, canonical_match):
    rule = get_resolution_rule(raw_link)
    if rule in APPROVE_RULES and canonical_match is not None:
        return canonical_match
    return current_resolved

def build_policy_aware_preview_index(resolution_index):
    canonical_index, ambiguous = canonicalise_resolution_index(resolution_index)
    return resolution_index, canonical_index, ambiguous

def resolve_link_with_preview_policy(link, resolution_index, canonical_index):
    current = resolve_link_with_index(link, resolution_index)
    canonical_match = canonical_index.get(normalise_link_key(link))
    return apply_preview_rule(link, current, canonical_match)
