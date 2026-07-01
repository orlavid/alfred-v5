from collections import defaultdict

def score_relationships(entities, graph):
    scores = defaultdict(int)
    seen_edges = set()

    entity_lookup = {e.id: e for e in entities}

    for edge in graph["edges"]:
        pair = tuple(sorted((edge["source"], edge["target"])))
        raw_link = edge.get("raw_link", "")

        edge_key = (pair, raw_link)
        if edge_key in seen_edges:
            continue
        seen_edges.add(edge_key)

        scores[pair] += 10

    relationships = []

    for (source, target), score in scores.items():
        relationships.append({
            "source": source,
            "target": target,
            "score": score,
            "source_title": entity_lookup[source].title,
            "target_title": entity_lookup[target].title,
        })

    relationships.sort(key=lambda r: r["score"], reverse=True)

    return {
        "relationship_count": len(relationships),
        "top_relationships": relationships[:100],
    }
