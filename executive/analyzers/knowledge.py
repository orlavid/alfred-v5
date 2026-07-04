from pathlib import Path
from dataclasses import asdict

from executive.knowledge.extractor import extract_entities
from executive.knowledge.graph import build_graph
from executive.knowledge.resolver import (
    build_entity_resolution,
    build_resolution_index,
    unresolved_links_with_index,
    resolution_summary_from_index,
)
from executive.knowledge.objectives import analyze_objectives
from executive.knowledge.projects import analyze_projects
from executive.knowledge.companies import analyze_companies
from executive.intelligence.people import analyse_people
from executive.intelligence.relationships import analyse_relationships
from executive.intelligence.dependencies import analyse_dependencies
from executive.intelligence.decisions import analyse_decisions
from executive.intelligence.risk import analyse_risk
from executive.intelligence.reasoning import build_executive_reasoning
from executive.intelligence.ownership import infer_ownership
from executive.intelligence.prioritisation import build_priorities
from executive.intelligence.safety import safe_execute
from executive.intelligence.work_queue import build_work_queue
from executive.intelligence.do_next import build_do_next
from executive.knowledge.relationship_strength import score_relationships
from executive.knowledge.executive_briefing import build_briefing
from executive.intelligence.impact import calculate
from executive.intelligence.entity_consolidation import consolidate, rewrite_graph
from executive.knowledge.findings import Finding

VAULT_ROOT = Path.home() / "Documents" / "My Vault" / "My Vault"


def analyze(evidence_root):
    entities = extract_entities(VAULT_ROOT)
    resolution_model = build_entity_resolution(entities)
    resolution_index = resolution_model.index
    graph = build_graph(entities, resolution_index)

    consolidation = consolidate(entities)

    rewrite_graph(graph, consolidation["entity_map"])

    unresolved = unresolved_links_with_index(entities, resolution_index)
    objective_analysis = analyze_objectives(entities, graph)
    project_analysis = analyze_projects(entities, graph)
    company_analysis = analyze_companies(entities, graph)
    people_analysis = analyse_people(entities, graph)
    relationship_analysis = analyse_relationships(graph, entities)
    dependency_analysis = analyse_dependencies(graph, entities)
    decision_analysis = analyse_decisions(graph, entities)
    risk_analysis = analyse_risk(graph, entities)
    ownership = infer_ownership(graph, entities)
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

    priority_input = {
        "objectives": objective_analysis,
        "projects": project_analysis,
        "companies": company_analysis,
        "people": people_analysis,
        "decisions": decision_analysis,
        "dependency_analysis": dependency_analysis,
        "impact": impact,
        "risk": risk_analysis,
        "ownership": ownership,
        "resolution": resolution,
        "findings": findings,
    }

    priority_analysis = safe_execute(
        lambda: build_priorities(priority_input, entities, graph),
        fallback={"priority_count": 0, "top_priorities": []},
        label="prioritisation"
    )

    work_queue = build_work_queue(priority_input)

    do_next = build_do_next(priority_input)

    reasoning_input = {
        "objectives": objective_analysis,
        "projects": project_analysis,
        "companies": company_analysis,
        "people": people_analysis,
        "decisions": decision_analysis,
        "dependency_analysis": dependency_analysis,
        "impact": impact,
        "risk": risk_analysis,
        "resolution": resolution,
        "findings": findings,
    }

    executive_reasoning = build_executive_reasoning(reasoning_input)

    briefing = build_briefing({
        "objectives": objective_analysis,
        "projects": project_analysis,
        "findings": findings,
    })

    return {
        "vault": {
            "entities": entities,
            "note_count": graph["entity_count"],
            "kind_counts": graph["entities_by_type"],
            "graph": graph,
            "unresolved_links": unresolved[:50],
            "unresolved_link_count": len(unresolved),
            "resolution": resolution,
            "canonical_entities": [asdict(entity) for entity in resolution_model.canonical_entities],
            "aliases": [asdict(alias) for alias in resolution_model.aliases],
            "relationships": list(resolution_model.relationships),
            "objectives": objective_analysis,
            "projects": project_analysis,
            "companies": company_analysis,
            "people": people_analysis,
            "relationship_analysis": relationship_analysis,
            "dependency_analysis": dependency_analysis,
            "decisions": decision_analysis,
            "risk": risk_analysis,
            "ownership": ownership,
            "priorities": priority_analysis,
            "work_queue": work_queue,
            "do_next": do_next,
            "executive_reasoning": executive_reasoning,
            "relationships": relationships,
            "impact": impact,
            "consolidation": consolidation,
            "briefing": briefing,
            "findings": findings,
        }
    }
