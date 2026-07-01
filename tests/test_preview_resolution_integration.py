from executive.knowledge.preview_resolution import resolve_link_with_preview_policy

class M:
    def __init__(self, id, title, type):
        self.id = id
        self.title = title
        self.type = type

def test_preview_policy_changes_only_approved_aliases():
    current_person = M("07 AI Memory/Entities/Julia Weeks.md", "Julia Weeks", "note")
    current_topic = M("05 Knowledge/01. Compliance/Compliance.md", "Compliance", "note")

    canonical_index = {
        "julia weeks": M("LLM Wiki/People/julia-weeks.md", "julia-weeks", "person"),
        "compliance": M("07 AI Memory/Entities/Compliance.md", "Compliance", "note"),
    }

    import executive.knowledge.preview_resolution as pr
    import executive.knowledge.resolution_rule_policy as rp

    original_resolve = pr.resolve_link_with_index
    original_rule = rp.get_resolution_rule

    def fake_resolve(link, resolution_index):
        if link == "Julia Weeks":
            return current_person
        if link == "Compliance":
            return current_topic
        return None

    def fake_rule(raw_link):
        if raw_link == "Julia Weeks":
            return "approve_person_alias"
        if raw_link == "Compliance":
            return "reject_for_now"
        return None

    pr.resolve_link_with_index = fake_resolve
    rp.get_resolution_rule = fake_rule
    try:
        person_result = resolve_link_with_preview_policy("Julia Weeks", {}, canonical_index)
        topic_result = resolve_link_with_preview_policy("Compliance", {}, canonical_index)

        assert person_result.id == "LLM Wiki/People/julia-weeks.md"
        assert topic_result.id == "05 Knowledge/01. Compliance/Compliance.md"
    finally:
        pr.resolve_link_with_index = original_resolve
        rp.get_resolution_rule = original_rule
