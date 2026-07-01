from pathlib import Path
from executive.knowledge.extractor import extract_entities
from executive.knowledge.resolver import build_resolution_index
from executive.knowledge.graph import build_graph
from executive.knowledge.canonical_resolution import canonicalise_resolution_index

VAULT_ROOT = Path.home() / "Documents" / "My Vault" / "My Vault"

def test_canonical_preview_preserves_edge_count():
    entities = extract_entities(VAULT_ROOT)
    resolution_index = build_resolution_index(entities)
    canonical_index, _ = canonicalise_resolution_index(resolution_index)
    canonical_index_for_graph = {k: [v] for k, v in canonical_index.items() if v is not None}

    current_graph = build_graph(entities, resolution_index)
    preview_graph = build_graph(entities, canonical_index_for_graph)

    assert current_graph["edge_count"] == preview_graph["edge_count"]
