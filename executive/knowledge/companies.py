from dataclasses import dataclass
from collections import defaultdict

@dataclass
class CompanyInsight:
    title: str
    path: str
    links: int
    people: int
    projects: int
    objectives: int
    score: int
    status: str
    is_supplier: bool = False

def analyze_companies(entities, graph):
    entity_lookup = {e.id: e for e in entities}

    connected = defaultdict(set)

    for edge in graph["edges"]:
        connected[edge["source"]].add(edge["target"])
        connected[edge["target"]].add(edge["source"])

    insights = []

    for entity in entities:
        if entity.type != "company":
            continue

        neighbours = [
            entity_lookup[n]
            for n in connected.get(entity.id, set())
            if n in entity_lookup
        ]

        people = sum(1 for n in neighbours if n.type == "person")
        projects = sum(1 for n in neighbours if n.type == "project")
        objectives = sum(1 for n in neighbours if n.type == "objective")

        score = (
            len(neighbours)
            + (projects * 5)
            + (objectives * 10)
            + (people * 2)
        )

        if score >= 30:
            status = "CRITICAL"
        elif score >= 15:
            status = "IMPORTANT"
        elif score >= 5:
            status = "ACTIVE"
        else:
            status = "LOW"

        insights.append(
            CompanyInsight(
                title=entity.title,
                path=entity.path,
                links=len(neighbours),
                people=people,
                projects=projects,
                objectives=objectives,
                score=score,
                status=status,
            )
        )

    insights.sort(key=lambda c: c.score, reverse=True)

    return {
        "company_count": len(insights),
        "critical": sum(c.status == "CRITICAL" for c in insights),
        "important": sum(c.status == "IMPORTANT" for c in insights),
        "active": sum(c.status == "ACTIVE" for c in insights),
        "low": sum(c.status == "LOW" for c in insights),
        "insights": insights,
    }
