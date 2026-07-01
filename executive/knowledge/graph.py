from collections import defaultdict

def build_graph(entities):
    by_title = {e.title: e for e in entities}
    edges = []

    for entity in entities:
        for link in entity.links:
            target = by_title.get(link)
            if target:
                edges.append({
                    "source": entity.id,
                    "target": target.id,
                    "type": "links_to",
                })

    return {
        "entity_count": len(entities),
        "edge_count": len(edges),
        "entities_by_type": dict(_count_by_type(entities)),
        "edges": edges,
    }

def _count_by_type(entities):
    counts = defaultdict(int)
    for entity in entities:
        counts[entity.type] += 1
    return counts
