APPROVAL_RULES = {
    "Julia Weeks": "approve_person_alias",
    "Andy Wetmiller": "approve_person_alias",
    "Pinewalk": "review_supplier_alias",
    "Jira": "prefer_system_record",
    "vendor-governance": "reject_for_now",
    "Compliance": "reject_for_now",
    "Vendor Management": "reject_for_now",
    "governance drift": "reject_for_now",
}

def get_resolution_rule(raw_link: str) -> str | None:
    return APPROVAL_RULES.get(raw_link)
