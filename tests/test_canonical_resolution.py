from executive.knowledge.canonical_resolution import choose_canonical

class M:
    def __init__(self, id, title, type):
        self.id = id
        self.title = title
        self.type = type

def test_choose_canonical_prefers_core_company_location():
    matches = [
        M("07 AI Memory/Entities/Abnormal.md", "Abnormal", "note"),
        M("LLM Wiki/Suppliers/abnormal.md", "abnormal", "company"),
        M("04 Companies/Abnormal.md", "Abnormal", "company"),
    ]
    chosen = choose_canonical(matches)
    assert chosen.id == "04 Companies/Abnormal.md"
    assert chosen.type == "company"
