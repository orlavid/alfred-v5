from collections import defaultdict

EXECUTIVE_TYPES = {
    "objective",
    "project",
    "company",
    "person",
}

def analyse_dependencies(graph, entities):
    lookup = {e.id: e for e in entities}

    depends_on = defaultdict(set)
    depended_on_by = defaultdict(set)

    for edge in graph["edges"]:
        depends_on[edge["source"]].add(edge["target"])
        depended_on_by[edge["target"]].add(edge["source"])

    results = []

    for entity in entities:
        if entity.type not in EXECUTIVE_TYPES:
            continue

        incoming = len(depended_on_by.get(entity.id, set()))
        outgoing = len(depends_on.get(entity.id, set()))

        bottleneck = incoming * 2 + outgoing

        results.append({
            "title": entity.title,
            "type": entity.type,
            "incoming": incoming,
            "outgoing": outgoing,
            "bottleneck": bottleneck,
        })

    results.sort(key=lambda x: x["bottleneck"], reverse=True)

    return {
        "top_dependencies": results[:100]
    }
