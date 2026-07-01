from collections import defaultdict

def analyse_decisions(graph, entities):
    lookup = {e.id: e for e in entities}

    neighbours = defaultdict(set)

    for edge in graph["edges"]:
        neighbours[edge["source"]].add(edge["target"])
        neighbours[edge["target"]].add(edge["source"])

    results = []

    for entity in entities:
        if entity.type != "decision":
            continue

        linked = [lookup[n] for n in neighbours.get(entity.id, set()) if n in lookup]

        projects = sum(1 for x in linked if x.type == "project")
        objectives = sum(1 for x in linked if x.type == "objective")
        companies = sum(1 for x in linked if x.type == "company")
        people = sum(1 for x in linked if x.type == "person")

        importance = (
            objectives * 100 +
            projects * 40 +
            companies * 20 +
            people * 10 +
            len(linked)
        )

        results.append({
            "title": entity.title,
            "projects": projects,
            "objectives": objectives,
            "companies": companies,
            "people": people,
            "importance": importance,
        })

    results.sort(key=lambda x: x["importance"], reverse=True)

    return {
        "decision_count": len(results),
        "top_decisions": results[:100],
    }
