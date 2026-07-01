from collections import defaultdict

WEIGHTS = {
    "objective": 100,
    "project": 40,
    "company": 25,
    "person": 10,
    "decision": 15,
    "open_loop": 20,
    "note": 1,
}

EXECUTIVE_TYPES = {
    "objective",
    "project",
    "company",
    "person",
    "decision",
    "open_loop",
}

def calculate(graph, entities):
    lookup = {e.id: e for e in entities}

    score = defaultdict(int)

    for edge in graph["edges"]:
        source = lookup.get(edge["source"])
        target = lookup.get(edge["target"])

        if source and target:
            score[source.id] += WEIGHTS.get(target.type, 5)
            score[target.id] += WEIGHTS.get(source.type, 5)

    ranked = []

    for entity in entities:
        if entity.type not in EXECUTIVE_TYPES:
            continue

        ranked.append({
            "id": entity.id,
            "title": entity.title,
            "type": entity.type,
            "impact": score[entity.id],
        })

    ranked.sort(key=lambda x: x["impact"], reverse=True)

    return ranked
