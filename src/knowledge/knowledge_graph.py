"""Canonical executive knowledge graph for Alfred."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from src.knowledge.executive_knowledge_builder import (
    DEFAULT_EVIDENCE_ROOT,
    ExecutiveKnowledgeModel,
    build_executive_knowledge,
)

NODE_TYPE_LABELS = {
    "objective": "Objective",
    "project": "Project",
    "company": "Company",
    "person": "Person",
    "meeting": "Meeting",
    "decision": "Decision",
    "risk": "Risk",
    "policy": "Policy",
    "daily_log": "Daily Log",
    "executive_briefing": "Executive Briefing",
}

RELATIONSHIP_TYPES = {
    "SUPPORTS",
    "OWNS",
    "ATTENDS",
    "RELATES_TO",
    "BLOCKS",
    "DEPENDS_ON",
    "DECIDES",
    "MENTIONS",
    "LINKS_TO",
}


@dataclass(frozen=True)
class GraphNode:
    id: str
    label: str
    node_type: str
    source_path: str
    confidence: str


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relationship_type: str


@dataclass(frozen=True)
class KnowledgeGraphModel:
    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]
    statistics: dict[str, dict[str, int] | int]
    orphans: tuple[GraphNode, ...]
    highest_connectivity: tuple[GraphNode, ...]
    suggested_missing_links: tuple[str, ...]


def build_knowledge_graph(
    evidence_root: Path | None = None,
) -> KnowledgeGraphModel:
    knowledge = build_executive_knowledge(evidence_root or DEFAULT_EVIDENCE_ROOT)
    return build_knowledge_graph_from_model(knowledge)


def build_knowledge_graph_from_model(model: ExecutiveKnowledgeModel) -> KnowledgeGraphModel:
    nodes = _build_nodes(model)
    node_lookup = {node.id: node for node in nodes}
    edges = _build_edges(model, node_lookup)
    statistics = _build_statistics(nodes, edges)
    connectivity = _connectivity(nodes, edges)
    orphans = tuple(node for node in nodes if connectivity.get(node.id, 0) == 0)
    highest = tuple(sorted(nodes, key=lambda node: (-connectivity.get(node.id, 0), node.label.lower(), node.id))[:10])
    suggestions = _suggest_missing_links(model, nodes, connectivity)
    return KnowledgeGraphModel(
        nodes=nodes,
        edges=edges,
        statistics=statistics,
        orphans=orphans,
        highest_connectivity=highest,
        suggested_missing_links=suggestions,
    )


def render_knowledge_graph(report: KnowledgeGraphModel) -> str:
    parts = ["# Knowledge Graph", ""]
    parts.extend(["## Summary", ""])
    parts.extend(_render_bullets(
        [
            f"Nodes: {len(report.nodes)}.",
            f"Edges: {len(report.edges)}.",
            f"Orphans: {len(report.orphans)}.",
            f"Highest-connectivity nodes listed: {len(report.highest_connectivity)}.",
        ]
    ))
    parts.extend(["", "## Node Counts", ""])
    parts.extend(_render_bullets([f"{key}: {value}" for key, value in sorted(report.statistics["node_counts"].items())]))
    parts.extend(["", "## Relationship Counts", ""])
    parts.extend(_render_bullets([f"{key}: {value}" for key, value in sorted(report.statistics["relationship_counts"].items())]))
    parts.extend(["", "## Orphans", ""])
    parts.extend(_render_nodes(report.orphans))
    parts.extend(["", "## Highest Connectivity", ""])
    parts.extend(_render_nodes(report.highest_connectivity))
    parts.extend(["", "## Suggested Missing Links", ""])
    parts.extend(_render_bullets(list(report.suggested_missing_links)))
    parts.append("")
    return "\n".join(parts)


def render_knowledge_graph_json(report: KnowledgeGraphModel) -> str:
    payload = {
        "nodes": [asdict(node) for node in report.nodes],
        "edges": [asdict(edge) for edge in report.edges],
        "statistics": report.statistics,
    }
    return __import__("json").dumps(payload, indent=2, sort_keys=True)


def _build_nodes(model: ExecutiveKnowledgeModel) -> tuple[GraphNode, ...]:
    nodes = []
    for item in model.canonical_entities:
        node_type = item["entity_type"]
        nodes.append(
            GraphNode(
                id=item["canonical_id"],
                label=item["canonical_name"],
                node_type=NODE_TYPE_LABELS.get(node_type, node_type.title()),
                source_path=item["source_path"],
                confidence=item["confidence"],
            )
        )
    return tuple(sorted(nodes, key=lambda node: (node.node_type, node.label.lower(), node.id)))


def _build_edges(model: ExecutiveKnowledgeModel, node_lookup: dict[str, GraphNode]) -> tuple[GraphEdge, ...]:
    alias_to_canonical = {alias["canonical_id"]: alias["canonical_name"] for alias in model.aliases}
    source_to_canonical = {item["source_path"]: item["canonical_id"] for item in model.canonical_entities}
    edges = []
    seen = set()

    for relationship in model.relationship_graph:
        source_id = _canonicalise_endpoint(relationship.source, source_to_canonical)
        target_id = _canonicalise_endpoint(relationship.target, source_to_canonical)
        if source_id not in node_lookup or target_id not in node_lookup or source_id == target_id:
            continue
        relationship_type = _map_relationship_type(node_lookup[source_id], node_lookup[target_id], relationship.relationship_type)
        key = (source_id, target_id, relationship_type)
        if key in seen:
            continue
        seen.add(key)
        edges.append(GraphEdge(source_id, target_id, relationship_type))

    for alias_edge in model.aliases:
        canonical_id = alias_edge["canonical_id"]
        if canonical_id not in node_lookup:
            continue
        alias_name = alias_edge["alias"]
        if alias_name == alias_to_canonical.get(canonical_id):
            continue

    return tuple(sorted(edges, key=lambda edge: (edge.relationship_type, edge.source, edge.target)))


def _canonicalise_endpoint(value: str, source_to_canonical: dict[str, str]) -> str:
    return source_to_canonical.get(value, value)


def _map_relationship_type(source: GraphNode, target: GraphNode, raw_type: str) -> str:
    if raw_type == "links_to":
        if source.node_type == "Project" and target.node_type == "Objective":
            return "SUPPORTS"
        if source.node_type == "Decision":
            return "DECIDES"
        if source.node_type == "Risk" and target.node_type in {"Project", "Objective"}:
            return "BLOCKS"
        if source.node_type == "Policy" and target.node_type in {"Project", "Objective", "Risk"}:
            return "RELATES_TO"
        return "LINKS_TO"
    if raw_type == "mentions":
        if source.node_type == "Person" and target.node_type in {"Project", "Objective", "Meeting"}:
            return "OWNS"
        if source.node_type == "Meeting" and target.node_type == "Person":
            return "ATTENDS"
        if source.node_type == "Project" and target.node_type == "Project":
            return "DEPENDS_ON"
        return "MENTIONS"
    return "RELATES_TO"


def _build_statistics(nodes: tuple[GraphNode, ...], edges: tuple[GraphEdge, ...]) -> dict[str, dict[str, int] | int]:
    node_counts: dict[str, int] = {}
    relationship_counts: dict[str, int] = {}
    for node in nodes:
        node_counts[node.node_type] = node_counts.get(node.node_type, 0) + 1
    for edge in edges:
        relationship_counts[edge.relationship_type] = relationship_counts.get(edge.relationship_type, 0) + 1
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "node_counts": dict(sorted(node_counts.items())),
        "relationship_counts": dict(sorted(relationship_counts.items())),
    }


def _connectivity(nodes: tuple[GraphNode, ...], edges: tuple[GraphEdge, ...]) -> dict[str, int]:
    counts = {node.id: 0 for node in nodes}
    for edge in edges:
        counts[edge.source] = counts.get(edge.source, 0) + 1
        counts[edge.target] = counts.get(edge.target, 0) + 1
    return counts


def _suggest_missing_links(
    model: ExecutiveKnowledgeModel,
    nodes: tuple[GraphNode, ...],
    connectivity: dict[str, int],
) -> tuple[str, ...]:
    node_lookup = {node.id: node for node in nodes}
    suggestions = []
    for orphan in model.orphans[:10]:
        node = node_lookup.get(orphan.id)
        if node is None:
            continue
        if node.node_type == "Project":
            suggestions.append(f"Link project {node.label} to an objective, owner, or decision.")
        elif node.node_type == "Objective":
            suggestions.append(f"Link objective {node.label} to supporting projects or decisions.")
        elif node.node_type == "Meeting":
            suggestions.append(f"Link meeting {node.label} to attendees, actions, or related decisions.")
        else:
            suggestions.append(f"Add at least one canonical relationship for {node.node_type.lower()} {node.label}.")
    if not suggestions and not any(connectivity.values()):
        suggestions.append("Add wikilinks between executive entities in Obsidian so the canonical graph has usable structure.")
    return tuple(sorted(dict.fromkeys(suggestions)))


def _render_bullets(values: Iterable[str]) -> list[str]:
    rendered = [f"- {value}" for value in values if value]
    return rendered or ["_None found._"]


def _render_nodes(values: Iterable[GraphNode]) -> list[str]:
    nodes = list(values)
    if not nodes:
        return ["_None found._"]
    return [
        f"- {node.label} | Type: {node.node_type} | Confidence: {node.confidence} | Source: {node.source_path}"
        for node in nodes
    ]
