from collections import defaultdict


def _priority_weight(priority):
    return {
        "CRITICAL": 100,
        "HIGH": 75,
        "MEDIUM": 50,
        "LOW": 25,
    }.get(priority, 0)


def _dedupe(actions):
    seen = set()
    result = []

    for item in actions:
        key = (
            item["title"].lower(),
            item["action"].lower(),
        )

        if key in seen:
            continue

        seen.add(key)
        result.append(item)

    return result


def build_work_queue(vault):
    priorities = vault.get("priorities", {})
    ownership = vault.get("ownership", {})
    findings = vault.get("findings", [])
    objectives = vault.get("objectives", {})
    projects = vault.get("projects", {})
    reasoning = vault.get("executive_reasoning", {})
    risk = vault.get("risk", {})
    resolution = vault.get("resolution", {})

    actions = []

    #
    # Executive priorities
    #

    for item in priorities.get("top_priorities", []):

        recommendation = (
            item.get("recommended_actions", ["Review executive treatment"])[0]
        )

        actions.append({
            "title": item["title"],
            "category": item["type"].title(),
            "priority": item["priority"],
            "score": _priority_weight(item["priority"]) + item["priority_score"],
            "action": recommendation,
            "reason": "; ".join(item.get("reasons", [])[:3]),
        })

    #
    # Missing project owners
    #

    for item in ownership.get("projects", []):

        if item["owner"] is not None:
            continue

        actions.append({
            "title": item["project"],
            "category": "Ownership",
            "priority": "HIGH",
            "score": 140,
            "action": "Assign an accountable owner",
            "reason": "Project has no inferred owner.",
        })

    #
    # Objective intelligence
    #

    for obj in objectives.get("insights", []):

        if getattr(obj, "status", "") != "AT RISK":
            continue

        actions.append({
            "title": obj.title,
            "category": "Objective",
            "priority": "CRITICAL",
            "score": 175,
            "action": "Reconnect objective to active delivery work",
            "reason": "Objective has insufficient supporting evidence.",
        })

    #
    # Project intelligence
    #

    for project in projects.get("insights", []):

        status = getattr(project, "status", "")

        if status == "AT RISK":

            actions.append({
                "title": project.title,
                "category": "Project",
                "priority": "HIGH",
                "score": 130,
                "action": "Review project governance",
                "reason": "Project lacks sufficient graph support.",
            })

        elif status == "WATCH":

            actions.append({
                "title": project.title,
                "category": "Project",
                "priority": "MEDIUM",
                "score": 80,
                "action": "Review supporting evidence",
                "reason": "Project has limited supporting relationships.",
            })

    #
    # Knowledge findings
    #

    for finding in findings:

        score = {
            "HIGH": 150,
            "MEDIUM": 100,
            "LOW": 50,
        }.get(finding.severity, 50)

        actions.append({
            "title": finding.title,
            "category": finding.category,
            "priority": finding.severity,
            "score": score,
            "action": finding.recommendation,
            "reason": finding.evidence,
        })

    #
    # Entity resolution
    #

    ambiguous = resolution.get("ambiguous_key_count", 0)

    if ambiguous:

        actions.append({
            "title": "Resolve ambiguous entities",
            "category": "Knowledge Graph",
            "priority": "HIGH",
            "score": min(200, ambiguous // 4),
            "action": "Continue canonical entity consolidation",
            "reason": f"{ambiguous} ambiguous entity keys remain.",
        })

    #
    # High risk count
    #

    if risk.get("high_risk"):

        actions.append({
            "title": "Reduce executive risk exposure",
            "category": "Executive Risk",
            "priority": "CRITICAL",
            "score": 190,
            "action": "Address highest-risk projects first",
            "reason": f"{len(risk['high_risk'])} high-risk entities remain.",
        })

    #
    # Executive reasoning recommendations
    #

    for conclusion in reasoning.get("conclusions", []):

        actions.append({
            "title": conclusion["headline"],
            "category": conclusion["theme"],
            "priority": "HIGH",
            "score": 120,
            "action": conclusion["recommendation"],
            "reason": conclusion["detail"],
        })

    #
    # Final ordering
    #

    actions = _dedupe(actions)

    actions.sort(
        key=lambda x: (
            -x["score"],
            x["title"].lower(),
        )
    )

    summary = defaultdict(int)

    for action in actions:

        summary[action["priority"]] += 1

    return {
        "total_actions": len(actions),
        "critical": summary["CRITICAL"],
        "high": summary["HIGH"],
        "medium": summary["MEDIUM"],
        "low": summary["LOW"],
        "top_actions": actions[:25],
        "all_actions": actions,
    }
