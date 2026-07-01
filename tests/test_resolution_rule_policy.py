from executive.knowledge.resolution_rule_policy import get_resolution_rule

def test_resolution_rule_policy():
    assert get_resolution_rule("Julia Weeks") == "approve_person_alias"
    assert get_resolution_rule("Andy Wetmiller") == "approve_person_alias"
    assert get_resolution_rule("Jira") == "prefer_system_record"
    assert get_resolution_rule("Compliance") == "reject_for_now"
    assert get_resolution_rule("unknown-link") is None
