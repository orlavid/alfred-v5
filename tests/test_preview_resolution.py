from executive.knowledge.preview_resolution import (
    apply_preview_rule,
    normalise_link_key,
    resolve_link_with_preview_policy,
)

class M:
    def __init__(self, id, title, type):
        self.id = id
        self.title = title
        self.type = type

def test_apply_preview_rule_uses_policy_approved_alias():
    current = M("current-id", "Current", "note")
    canonical = M("canonical-id", "Canonical", "person")

    import executive.knowledge.preview_resolution as pr
    import executive.knowledge.resolution_rule_policy as rp

    original = rp.get_resolution_rule
    rp.get_resolution_rule = lambda raw_link: "approve_person_alias"
    try:
        result = apply_preview_rule("Any Person", current, canonical)
        assert result.id == "canonical-id"
    finally:
        rp.get_resolution_rule = original

def test_apply_preview_rule_preserves_current_when_rejected():
    current = M("current-id", "Current", "note")
    canonical = M("canonical-id", "Canonical", "note")

    import executive.knowledge.preview_resolution as pr
    import executive.knowledge.resolution_rule_policy as rp

    original = rp.get_resolution_rule
    rp.get_resolution_rule = lambda raw_link: "reject_for_now"
    try:
        result = apply_preview_rule("Any Topic", current, canonical)
        assert result.id == "current-id"
    finally:
        rp.get_resolution_rule = original

def test_normalise_link_key():
    assert normalise_link_key("Julia-Weeks") == "julia weeks"

def test_resolve_link_with_preview_policy_imports_and_runs():
    current = M("current-id", "Current", "note")
    canonical = {"example person": M("canonical-id", "Canonical", "person")}

    import executive.knowledge.preview_resolution as pr
    import executive.knowledge.resolution_rule_policy as rp

    original_resolve = pr.resolve_link_with_index
    original_rule = rp.get_resolution_rule

    pr.resolve_link_with_index = lambda link, resolution_index: current
    rp.get_resolution_rule = lambda raw_link: "approve_person_alias"
    try:
        result = resolve_link_with_preview_policy("Example Person", {}, canonical)
        assert result.id == "canonical-id"
    finally:
        pr.resolve_link_with_index = original_resolve
        rp.get_resolution_rule = original_rule
