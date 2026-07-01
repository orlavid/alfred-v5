from collections import defaultdict
from executive.knowledge.resolver import normalise_name
from dataclasses import dataclass

@dataclass
class PersonInsight:
    title: str
    path: str
    projects: int
    companies: int
    objectives: int
    decisions: int
    total_links: int
    influence: int
    risk: str

def analyse_people(entities, graph):
    lookup = {e.id: e for e in entities}

    connected = defaultdict(set)

    for edge in graph["edges"]:
        connected[edge["source"]].add(edge["target"])
        connected[edge["target"]].add(edge["source"])

    insights = []

    for entity in entities:
        if entity.type != "person":
            continue

        neighbours = [
            lookup[n]
            for n in connected.get(entity.id, set())
            if n in lookup
        ]

        projects = sum(1 for n in neighbours if n.type == "project")
        companies = sum(1 for n in neighbours if n.type == "company")
        objectives = sum(1 for n in neighbours if n.type == "objective")
        decisions = sum(1 for n in neighbours if n.type == "decision")

        influence = (
            projects * 20 +
            companies * 10 +
            objectives * 40 +
            decisions * 15 +
            len(neighbours)
        )

        if influence >= 500:
            risk = "CRITICAL"
        elif influence >= 250:
            risk = "HIGH"
        elif influence >= 100:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        insights.append(
            PersonInsight(
                title=entity.title,
                path=entity.path,
                projects=projects,
                companies=companies,
                objectives=objectives,
                decisions=decisions,
                total_links=len(neighbours),
                influence=influence,
                risk=risk,
            )
        )

    insights.sort(key=lambda p: p.influence, reverse=True)

    duplicate_groups = defaultdict(list)
    for person in insights:
        duplicate_groups[normalise_name(person.title)].append(person.title)

    duplicates = {
        key: sorted(set(values))
        for key, values in duplicate_groups.items()
        if len(set(values)) > 1
    }

    return {
        "people_count": len(insights),
        "duplicate_people": len(duplicates),
        "duplicate_examples": dict(list(duplicates.items())[:10]),
        "critical": sum(p.risk == "CRITICAL" for p in insights),
        "high": sum(p.risk == "HIGH" for p in insights),
        "medium": sum(p.risk == "MEDIUM" for p in insights),
        "low": sum(p.risk == "LOW" for p in insights),
        "insights": insights,
    }
