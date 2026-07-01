from pathlib import Path

from executive.knowledge.extractor import extract_entities
from executive.knowledge.graph import build_graph
from executive.knowledge.resolver import unresolved_links
from executive.knowledge.objectives import analyze_objectives
from executive.knowledge.findings import Finding

VAULT_ROOT = Path.home() / "Documents" / "My Vault" / "My Vault"

def analyze(evidence_root):
    entities = extract_entities(VAULT_ROOT)
    graph = build_graph(entities)
    unresolved = unresolved_links(entities)
    objective_analysis = analyze_objectives(entities, graph)

    findings = []

    if graph["entities_by_type"].get("project", 0) == 0:
        findings.append(Finding(
            category="Knowledge",
            severity="HIGH",
            title="No projects detected in vault",
            evidence="The vault scan did not classify any project entities.",
            recommendation="Review project folder naming or classification rules.",
        ))

    if graph["entities_by_type"].get("objective", 0) == 0:
        findings.append(Finding(
            category="Knowledge",
            severity="HIGH",
            title="No objectives detected in vault",
            evidence="The vault scan did not classify any objective entities.",
            recommendation="Create or tag objective notes so Alfred can track strategic drift.",
        ))

    if len(unresolved) > 1000:
        findings.append(Finding(
            category="Knowledge Graph",
            severity="MEDIUM",
            title="High unresolved link count",
            evidence=f"{len(unresolved)} wikilinks do not currently resolve to known vault entities.",
            recommendation="Prioritise entity resolution and alias handling so Alfred can reason more accurately across people, projects, suppliers and objectives.",
        ))

    return {
        "vault": {
            "note_count": graph["entity_count"],
            "kind_counts": graph["entities_by_type"],
            "graph": graph,
            "unresolved_links": unresolved[:50],
            "unresolved_link_count": len(unresolved),
            "objectives": objective_analysis,
            "findings": findings,
        }
    }
