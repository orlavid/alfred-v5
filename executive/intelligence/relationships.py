from collections import defaultdict

def analyse_relationships(graph, entities):
    lookup = {e.id: e for e in entities}

    neighbours = defaultdict(set)

    for edge in graph["edges"]:
        neighbours[edge["source"]].add(edge["target"])
        neighbours[edge["target"]].add(edge["source"])

    ranked = []

    for entity in entities:
        links = neighbours.get(entity.id, set())

        linked_types = defaultdict(int)

        for other in links:
            if other not in lookup:
                continue
            linked_types[lookup[other].type] += 1

        ranked.append({
            "title": entity.title,
            "type": entity.type,
            "connections": len(links),
            "linked_types": dict(linked_types),
        })

    ranked.sort(key=lambda x: x["connections"], reverse=True)

    return {
        "top_connected": ranked[:100],
        "max_connections": ranked[0]["connections"] if ranked else 0,
    }
