from pathlib import Path

from executive.knowledge.extractor import extract_entities
from executive.knowledge.graph import build_graph
from executive.knowledge.resolver import (
    build_resolution_index,
    unresolved_links_with_index,
    resolution_summary_from_index,
)
from executive.knowledge.objectives import analyze_objectives
from executive.knowledge.projects import analyze_projects
from executive.knowledge.companies import analyze_companies
from executive.intelligence.people import analyse_people
from executive.knowledge.relationship_strength import score_relationships
from executive.knowledge.executive_briefing import build_briefing
from executive.intelligence.impact import calculate
from executive.knowledge.findings import Finding

VAULT_ROOT = Path.home() / "Documents" / "My Vault" / "My Vault"

def analyze(evidence_root):
    entities = extract_entities(VAULT_ROOT)
    resolution_index = build_resolution_index(entities)
    graph = build_graph(entities, resolution_index)
    unresolved = unresolved_links_with_index(entities, resolution_index)
    objective_analysis = analyze_objectives(entities, graph)
    project_analysis = analyze_projects(entities, graph)
    company_analysis = analyze_companies(entities, graph)
    people_analysis = analyse_people(entities, graph)
    relationships = score_relationships(entities, graph)
    impact = calculate(graph, entities)
    resolution = resolution_summary_from_index(resolution_index)

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

    briefing = build_briefing({
        "objectives": objective_analysis,
        "projects": project_analysis,
            "companies": company_analysis,
            "people": people_analysis,
        "findings": findings,
    })

    return {
        "vault": {
            "note_count": graph["entity_count"],
            "kind_counts": graph["entities_by_type"],
            "graph": graph,
            "unresolved_links": unresolved[:50],
            "unresolved_link_count": len(unresolved),
            "resolution": resolution,
            "objectives": objective_analysis,
            "projects": project_analysis,
            "companies": company_analysis,
            "people": people_analysis,
            "relationships": relationships,
            "impact": impact,
            "briefing": briefing,
            "findings": findings,
        }
    }
