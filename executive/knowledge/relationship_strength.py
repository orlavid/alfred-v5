from collections import defaultdict

def score_relationships(entities, graph):
    entity_lookup = {e.id: e for e in entities}

    relationships = []
    seen = set()

    for edge in graph.get("edges", []):
        source = edge.get("source")
        target = edge.get("target")

        src = entity_lookup.get(source)
        tgt = entity_lookup.get(target)

        if not src or not tgt:
            continue

        key = tuple(sorted((source, target)))
        if key in seen:
            continue
        seen.add(key)

        relationships.append({
            "source": source,
            "target": target,
            "score": 10,
            "source_title": src.title,
            "target_title": tgt.title,
        })

    return {
        "relationship_count": len(relationships),
        "top_relationships": relationships[:100],
    }
