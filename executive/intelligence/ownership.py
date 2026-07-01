from collections import defaultdict

def infer_ownership(graph, entities):
    lookup = {e.id: e for e in entities}

    neighbours = defaultdict(set)

    for edge in graph["edges"]:
        neighbours[edge["source"]].add(edge["target"])
        neighbours[edge["target"]].add(edge["source"])

    owners = []

    for entity in entities:
        if entity.type != "project":
            continue

        linked = [
            lookup[n]
            for n in neighbours.get(entity.id, set())
            if n in lookup
        ]

        people = [x for x in linked if x.type == "person"]

        if people:
            owners.append({
                "project": entity.title,
                "owner": people[0].title,
                "confidence": 1.0,
                "source": "graph",
            })
            continue

        company_counts = defaultdict(int)

        for x in linked:
            if x.type == "company":
                company_counts[x.title] += 1

        if company_counts:
            company = max(company_counts, key=company_counts.get)
            owners.append({
                "project": entity.title,
                "owner": f"(unknown owner via {company})",
                "confidence": 0.35,
                "source": "company inference",
            })
            continue

        owners.append({
            "project": entity.title,
            "owner": None,
            "confidence": 0.0,
            "source": "none",
        })

    return {
        "projects": owners,
        "owned_projects": sum(1 for x in owners if x["owner"]),
        "missing_owners": sum(1 for x in owners if not x["owner"]),
    }
