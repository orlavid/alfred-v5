def build_briefing(vault):
    briefing = []

    objectives = vault.get("objectives", {})
    projects = vault.get("projects", {})
    findings = vault.get("findings", [])

    if objectives.get("at_risk", 0):
        briefing.append({
            "priority": 1,
            "category": "Objectives",
            "headline": f"{objectives['at_risk']} strategic objective(s) require attention",
            "detail": "One or more executive objectives have insufficient supporting evidence.",
        })

    if projects.get("at_risk", 0):
        briefing.append({
            "priority": 2,
            "category": "Projects",
            "headline": f"{projects['at_risk']} project(s) are at risk",
            "detail": "Projects exist without sufficient supporting relationships.",
        })

    for finding in findings:
        briefing.append({
            "priority": 3,
            "category": finding.category,
            "headline": finding.title,
            "detail": finding.evidence,
        })

    briefing.sort(key=lambda b: b["priority"])

    return briefing
