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
from executive.knowledge.entity_quality import build_executive_entity_quality
from src.obsidian.live_vault import resolve_live_vault_path

VAULT_ROOT = resolve_live_vault_path()


def analyze(evidence_root, vault_root=None):
    effective_vault_root = resolve_live_vault_path(vault_root) if vault_root is not None else VAULT_ROOT
    entities = extract_entities(effective_vault_root)
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
    entity_quality = build_executive_entity_quality(
        entities,
        resolution_model,
        graph=graph,
        objective_analysis=objective_analysis,
        project_analysis=project_analysis,
        company_analysis=company_analysis,
        people_analysis=people_analysis,
        decision_analysis=decision_analysis,
        risk_analysis=risk_analysis,
        ownership=ownership,
    )

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
        lambda: build_priorities(
            priority_input,
            entities,
            graph,
            canonical_entities=entity_quality.canonical_entities,
        ),
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
            "entity_quality": {
                "canonical_count": len(entity_quality.canonical_entities),
                "rejected_count": len(entity_quality.rejected_entities),
                "canonical_examples": [
                    {
                        "entity_id": item.entity_id,
                        "entity_type": item.entity_type,
                        "canonical_name": item.canonical_name,
                        "owner": item.owner,
                        "status": item.status,
                        "risk_level": item.risk_level,
                        "evidence_paths": list(item.evidence_paths),
                        "missing_fields": list(item.missing_fields),
                    }
                    for item in entity_quality.canonical_entities[:20]
                ],
                "rejected_examples": [
                    {
                        "title": item.title,
                        "entity_type": item.entity_type,
                        "path": item.path,
                        "reasons": list(item.reasons),
                    }
                    for item in entity_quality.rejected_entities[:20]
                ],
            },
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
