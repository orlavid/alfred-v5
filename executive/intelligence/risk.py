from collections import defaultdict

def analyse_risk(graph, entities):
    lookup = {e.id: e for e in entities}

    neighbours = defaultdict(set)

    for edge in graph["edges"]:
        neighbours[edge["source"]].add(edge["target"])
        neighbours[edge["target"]].add(edge["source"])

    risks = []

    for entity in entities:
        if entity.type not in ("project", "objective", "company"):
            continue

        linked = [
            lookup[n]
            for n in neighbours.get(entity.id, set())
            if n in lookup
        ]

        linked_types = {x.type for x in linked}

        score = 0
        reasons = []

        if entity.type == "project":
            if "person" not in linked_types:
                score += 30
                reasons.append("No owner or person linked")
            if "objective" not in linked_types:
                score += 25
                reasons.append("No objective linked")
            if "company" not in linked_types:
                score += 20
                reasons.append("No supplier/company linked")
            if len(linked) < 3:
                score += 25
                reasons.append("Weak graph connectivity")

        elif entity.type == "objective":
            if "project" not in linked_types:
                score += 50
                reasons.append("No supporting project linked")
            if len(linked) < 3:
                score += 25
                reasons.append("Weak graph connectivity")

        elif entity.type == "company":
            if len(linked) >= 10 and "person" not in linked_types:
                score += 40
                reasons.append("Important company has no linked owner/person")
            if len(linked) >= 10 and "project" not in linked_types:
                score += 20
                reasons.append("Important company has no linked project")
            if len(linked) < 2:
                score += 15
                reasons.append("Low evidence company record")

        if score > 0:
            risks.append({
                "title": entity.title,
                "type": entity.type,
                "risk_score": score,
                "reasons": reasons,
                "connections": len(linked),
            })

    risks.sort(key=lambda r: r["risk_score"], reverse=True)

    return {
        "high_risk": [r for r in risks if r["risk_score"] >= 50],
        "all": risks,
    }
