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

def test_choose_canonical_prefers_system_record_for_jira():
    matches = [
        M("07 AI Memory/Entities/JIRA.md", "JIRA", "note"),
        M("06 Systems/Jira.md", "Jira", "note"),
    ]
    chosen = choose_canonical(matches)
    assert chosen.id == "06 Systems/Jira.md"

def test_choose_canonical_prefers_llm_wiki_person_over_ai_memory_entity():
    matches = [
        M("07 AI Memory/Entities/Julia Weeks.md", "Julia Weeks", "note"),
        M("LLM Wiki/People/julia-weeks.md", "julia-weeks", "person"),
    ]
    chosen = choose_canonical(matches)
    assert chosen.id == "LLM Wiki/People/julia-weeks.md"
    assert chosen.type == "person"

def test_choose_canonical_prefers_llm_wiki_person_for_andy_wetmiller():
    matches = [
        M("07 AI Memory/Entities/Andy Wetmiller.md", "Andy Wetmiller", "note"),
        M("LLM Wiki/People/andy-wetmiller.md", "andy-wetmiller", "person"),
    ]
    chosen = choose_canonical(matches)
    assert chosen.id == "LLM Wiki/People/andy-wetmiller.md"
    assert chosen.type == "person"
