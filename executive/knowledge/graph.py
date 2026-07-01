from collections import defaultdict

from executive.knowledge.resolver import resolve_link_with_index

def build_graph(entities, resolution_index):
    edges = []

    for entity in entities:
        for link in entity.links:
            target = resolve_link_with_index(link, resolution_index)
            if target:
                edges.append({
                    "source": entity.id,
                    "target": target.id,
                    "type": "links_to",
                    "raw_link": link,
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
