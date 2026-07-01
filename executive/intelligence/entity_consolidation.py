from collections import defaultdict

from executive.knowledge.resolver import (
    build_resolution_index,
    choose_canonical,
)

def consolidate(entities):
    index = build_resolution_index(entities)

    canonical = {}
    merged = defaultdict(list)

    for _, candidates in index.items():
        winner = choose_canonical(candidates)

        canonical[winner.id] = winner

        for candidate in candidates:
            merged[winner.id].append(candidate.id)

    entity_map = {}

    for canonical_id, members in merged.items():
        for member in members:
            entity_map[member] = canonical_id

    return {
        "entity_map": entity_map,
        "canonical_entities": canonical,
        "merged_groups": merged,
        "merged_count": sum(len(v)-1 for v in merged.values()),
    }

def rewrite_graph(graph, entity_map):
    rewritten = []

    seen = set()

    for edge in graph["edges"]:
        source = entity_map.get(edge["source"], edge["source"])
        target = entity_map.get(edge["target"], edge["target"])

        if source == target:
            continue

        key = (
            source,
            target,
            edge.get("raw_link",""),
        )

        if key in seen:
            continue

        seen.add(key)

        rewritten.append({
            **edge,
            "source": source,
            "target": target,
        })

    graph["edges"] = rewritten

    return graph
