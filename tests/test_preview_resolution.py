from executive.knowledge.preview_resolution import apply_preview_rule

class M:
    def __init__(self, id, title, type):
        self.id = id
        self.title = title
        self.type = type

def test_apply_preview_rule_approves_person_alias():
    current = [M("07 AI Memory/Entities/Julia Weeks.md", "Julia Weeks", "note")]
    canonical = M("LLM Wiki/People/julia-weeks.md", "julia-weeks", "person")
    result = apply_preview_rule("Julia Weeks", current, canonical)
    assert len(result) == 1
    assert result[0].id == "LLM Wiki/People/julia-weeks.md"

def test_apply_preview_rule_rejects_compliance_change():
    current = [M("05 Knowledge/01. Compliance/Compliance.md", "Compliance", "note")]
    canonical = M("07 AI Memory/Entities/Compliance.md", "Compliance", "note")
    result = apply_preview_rule("Compliance", current, canonical)
    assert len(result) == 1
    assert result[0].id == "05 Knowledge/01. Compliance/Compliance.md"
