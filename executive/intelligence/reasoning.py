def build_executive_reasoning(vault):
    conclusions = []

    objectives = vault.get("objectives", {})
    projects = vault.get("projects", {})
    companies = vault.get("companies", {})
    people = vault.get("people", {})
    decisions = vault.get("decisions", {})
    dependencies = vault.get("dependency_analysis", {})
    impact = vault.get("impact", [])
    risk = vault.get("risk", {})
    resolution = vault.get("resolution", {})

    if risk.get("high_risk"):
        top = risk["high_risk"][0]
        conclusions.append({
            "priority": 1,
            "theme": "Executive Risk",
            "headline": f"{len(risk['high_risk'])} high-risk entities require attention",
            "detail": f"Highest risk item is {top['title']} with risk score {top['risk_score']}.",
            "recommendation": "Review the highest-risk projects and resolve ownership, objective linkage and supplier linkage gaps.",
        })

    if projects.get("at_risk", 0):
        conclusions.append({
            "priority": 2,
            "theme": "Project Governance",
            "headline": f"{projects['at_risk']} projects are at risk",
            "detail": "Projects are flagged where graph evidence shows missing owners, objectives, suppliers or weak connectivity.",
            "recommendation": "Prioritise remediation of projects with no linked owner, objective or supplier.",
        })

    if objectives.get("at_risk", 0):
        conclusions.append({
            "priority": 3,
            "theme": "Strategic Alignment",
            "headline": f"{objectives['at_risk']} strategic objective is unsupported",
            "detail": "At least one objective has insufficient supporting evidence in the knowledge graph.",
            "recommendation": "Review objective-to-project traceability and link active initiatives to the objective register.",
        })

    if dependencies.get("top_dependencies"):
        top = dependencies["top_dependencies"][0]
        conclusions.append({
            "priority": 4,
            "theme": "Dependency Concentration",
            "headline": f"{top['title']} is the largest dependency bottleneck",
            "detail": f"{top['title']} has bottleneck score {top['bottleneck']} with {top['incoming']} incoming references.",
            "recommendation": "Assess whether this concentration creates operational, supplier or knowledge dependency risk.",
        })

    if impact:
        top = impact[0]
        conclusions.append({
            "priority": 5,
            "theme": "Executive Impact",
            "headline": f"{top['title']} has the highest executive impact",
            "detail": f"{top['title']} is ranked highest by graph impact score ({top['impact']}).",
            "recommendation": "Validate whether this entity should be treated as a strategic priority in executive briefings.",
        })

    if people.get("duplicate_people", 0):
        conclusions.append({
            "priority": 6,
            "theme": "Entity Quality",
            "headline": f"{people['duplicate_people']} duplicate people groups remain",
            "detail": "Duplicate people records are still distorting influence, ownership and relationship analysis.",
            "recommendation": "Continue canonical entity consolidation and alias learning.",
        })

    if resolution.get("ambiguous_keys", 0):
        conclusions.append({
            "priority": 7,
            "theme": "Knowledge Graph Quality",
            "headline": f"{resolution['ambiguous_keys']} ambiguous entity keys remain",
            "detail": "Ambiguous entity keys reduce confidence in relationship and dependency analysis.",
            "recommendation": "Prioritise high-impact ambiguous entities first: people, suppliers, projects and objectives.",
        })

    if decisions.get("decision_count", 0) and not any(d.get("projects", 0) or d.get("objectives", 0) for d in decisions.get("top_decisions", [])):
        conclusions.append({
            "priority": 8,
            "theme": "Decision Traceability",
            "headline": "Decisions are weakly linked to projects and objectives",
            "detail": "Current decision records show limited graph linkage to strategic delivery evidence.",
            "recommendation": "Improve decision note structure so decisions link to affected projects, suppliers, owners and objectives.",
        })

    conclusions.sort(key=lambda x: x["priority"])

    return {
        "conclusion_count": len(conclusions),
        "conclusions": conclusions,
    }
