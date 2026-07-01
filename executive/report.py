from executive.recommendations import build_recommendations

STATUS_ICON = {
    "GREEN": "🟢",
    "AMBER": "🟠",
    "RED": "🔴",
}

def render(result):
    health = result["health"]
    risks = result["risks"]
    timers = result.get("timers", {})
    docker = result.get("docker", {})
    vault = result.get("knowledge", {}).get("vault", {})
    objectives = vault.get("objectives", {})
    projects = vault.get("projects", {})
    companies = vault.get("companies", {})
    people = vault.get("people", {})
    impact = vault.get("impact", [])
    dependencies = vault.get("dependency_analysis", {})
    decisions = vault.get("decisions", {})
    risk = vault.get("risk", {})
    reasoning = vault.get("executive_reasoning", {})
    ownership = vault.get("ownership", {})
    resolution = vault.get("resolution", {})
    recommendations = build_recommendations(risks)
    knowledge_findings = vault.get("findings", [])
    briefing = vault.get("briefing", [])

    lines = [
        "# Executive Review",
        "",
        "## Executive Health",
        "",
        f"Overall Score: **{health['score']} / 100**",
        f"Overall Status: **{STATUS_ICON[health['status']]} {health['status']}**",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Running Services | {health['running']} |",
        f"| Failed Services | {health['failed']} |",
        f"| Timers Detected | {timers.get('timer_count', 0)} |",
        f"| Docker Containers | {docker.get('container_count', 0)} |",
        f"| Running Containers | {docker.get('running', 0)} |",
        f"| Exited Containers | {docker.get('exited', 0)} |",
        f"| Vault Notes | {vault.get('note_count', 0)} |",
        f"| Projects | {vault.get('kind_counts', {}).get('project', 0)} |",
        f"| Objectives | {vault.get('kind_counts', {}).get('objective', 0)} |",
        f"| Companies | {vault.get('kind_counts', {}).get('company', 0)} |",
        f"| People | {vault.get('kind_counts', {}).get('person', 0)} |",
        f"| Open Loops | {vault.get('kind_counts', {}).get('open_loop', 0)} |",
        f"| Knowledge Graph Edges | {vault.get('graph', {}).get('edge_count', 0)} |",
        f"| Unresolved Links | {vault.get('unresolved_link_count', 0)} |",
        f"| Objectives Analysed | {objectives.get('objective_count', 0)} |",
        f"| Objectives At Risk | {objectives.get('at_risk', 0)} |",
        f"| Objectives On Watch | {objectives.get('watch', 0)} |",
        f"| Objectives Supported | {objectives.get('supported', 0)} |",
        f"| Projects Analysed | {projects.get('project_count', 0)} |",
        f"| Projects At Risk | {projects.get('at_risk', 0)} |",
        f"| Projects On Watch | {projects.get('watch', 0)} |",
        f"| Projects Supported | {projects.get('supported', 0)} |",
        f"| Companies Analysed | {companies.get('company_count', 0)} |",
        f"| Critical Companies | {companies.get('critical', 0)} |",
        f"| Important Companies | {companies.get('important', 0)} |",
        f"| People Analysed | {people.get('people_count', 0)} |",
        f"| High Influence People | {people.get('high', 0)} |",
        f"| Duplicate People Groups | {people.get('duplicate_people', 0)} |",
        f"| Resolution Keys | {resolution.get('resolution_keys', 0)} |",
        f"| Ambiguous Entity Keys | {resolution.get('ambiguous_keys', 0)} |",
        "",
    ]


    if briefing:
        lines.extend([
            "## Executive Briefing",
            "",
        ])

        for item in briefing:
            lines.extend([
                f"### {item['headline']}",
                f"**Category:** {item['category']}",
                f"{item['detail']}",
                "",
            ])

    if knowledge_findings:
        lines.extend([
            "## Knowledge Findings",
            "",
        ])
        for f in knowledge_findings:
            lines.extend([
                f"### {f.severity}: {f.title}",
                f"**Category:** {f.category}",
                f"**Evidence:** {f.evidence}",
                f"**Recommendation:** {f.recommendation}",
                "",
            ])

    if objectives.get("insights"):
        lines.extend([
            "## Objective Intelligence",
            "",
            f"Objectives analysed: **{objectives.get('objective_count', 0)}**",
            f"At risk: **{objectives.get('at_risk', 0)}**",
            f"Watch: **{objectives.get('watch', 0)}**",
            f"Supported: **{objectives.get('supported', 0)}**",
            "",
        ])

        notable_objectives = [
            objective
            for objective in objectives.get("insights", [])
            if objective.status in ("AT RISK", "WATCH")
        ][:10]

        for objective in notable_objectives:
                lines.extend([
                    f"### {objective.status}: {objective.title}",
                    f"**Linked entities:** {objective.linked_entities}",
                    f"**Recommendation:** {objective.recommendation}",
                    "",
                ])

    if projects.get("insights"):
        notable_projects = [
            project
            for project in projects.get("insights", [])
            if project.status in ("AT RISK", "WATCH")
        ][:10]

        lines.extend([
            "## Project Intelligence",
            "",
            f"Projects analysed: **{projects.get('project_count', 0)}**",
            f"At risk: **{projects.get('at_risk', 0)}**",
            f"Watch: **{projects.get('watch', 0)}**",
            f"Supported: **{projects.get('supported', 0)}**",
            "",
        ])

        for project in notable_projects:
            lines.extend([
                f"### {project.status}: {project.title}",
                f"**Linked entities:** {project.linked_entities}",
                f"**Recommendation:** {project.recommendation}",
                "",
            ])

    if people.get("insights"):
        lines.extend([
            "## People Intelligence",
            "",
            f"People analysed: **{people.get('people_count', 0)}**",
            f"High influence: **{people.get('high', 0)}**",
            f"Medium influence: **{people.get('medium', 0)}**",
            f"Duplicate people groups: **{people.get('duplicate_people', 0)}**",
            "",
        ])

        if people.get("duplicate_examples"):
            lines.extend([
                "### Duplicate people detected",
                "",
            ])
            for key, variants in list(people.get("duplicate_examples", {}).items())[:10]:
                lines.append(f"- **{key}**: {', '.join(variants)}")
            lines.append("")

        for person in people.get("insights", [])[:10]:
            lines.extend([
                f"### {person.risk}: {person.title}",
                f"**Influence:** {person.influence}",
                f"**Projects:** {person.projects}",
                f"**Companies:** {person.companies}",
                f"**Decisions:** {person.decisions}",
                "",
            ])

    if reasoning.get("conclusions"):
        lines.extend([
            "## Ownership Intelligence

Projects with inferred owner: **{ownership.get('owned_projects',0)}**
Projects missing owner: **{ownership.get('missing_owners',0)}**

## Executive Reasoning",
            "",
            f"Conclusions: **{reasoning.get('conclusion_count', 0)}**",
            "",
        ])

        for item in reasoning.get("conclusions", [])[:10]:
            lines.extend([
                f"### {item['headline']}",
                f"**Theme:** {item['theme']}",
                f"**Detail:** {item['detail']}",
                f"**Recommendation:** {item['recommendation']}",
                "",
            ])

    if risk.get("high_risk"):
        lines.extend([
            "## Executive Risk Intelligence",
            "",
            f"High risk items: **{len(risk.get('high_risk', []))}**",
            "",
        ])

        for item in risk.get("high_risk", [])[:10]:
            lines.extend([
                f"### {item['risk_score']}: {item['title']}",
                f"**Type:** {item['type']}",
                f"**Connections:** {item['connections']}",
                "**Drivers:**",
            ])
            for reason in item.get("reasons", []):
                lines.append(f"- {reason}")
            lines.append("")

    if decisions.get("top_decisions"):
        lines.extend([
            "## Decision Intelligence",
            "",
            f"Decisions analysed: **{decisions.get('decision_count', 0)}**",
            "",
        ])

        for decision in decisions.get("top_decisions", [])[:10]:
            lines.extend([
                f"### {decision['title']}",
                f"**Importance:** {decision['importance']}",
                f"**Projects:** {decision['projects']}",
                f"**Objectives:** {decision['objectives']}",
                f"**Companies:** {decision['companies']}",
                f"**People:** {decision['people']}",
                "",
            ])

    if dependencies.get("top_dependencies"):
        lines.extend([
            "## Dependency Intelligence",
            "",
        ])

        for item in dependencies.get("top_dependencies", [])[:10]:
            lines.extend([
                f"### {item['title']}",
                f"**Type:** {item['type']}",
                f"**Bottleneck score:** {item['bottleneck']}",
                f"**Incoming references:** {item['incoming']}",
                f"**Outgoing dependencies:** {item['outgoing']}",
                "",
            ])

    if impact:
        lines.extend([
            "## Top Executive Impact",
            "",
        ])

        for item in impact[:10]:
            lines.extend([
                f"### {item['title']}",
                f"**Type:** {item['type']}",
                f"**Impact score:** {item['impact']}",
                "",
            ])

    if companies.get("insights"):
        lines.extend([
            "## Company Intelligence",
            "",
            f"Companies analysed: **{companies.get('company_count', 0)}**",
            f"Critical: **{companies.get('critical', 0)}**",
            f"Important: **{companies.get('important', 0)}**",
            "",
        ])

        for company in companies.get("insights", [])[:10]:
            lines.extend([
                f"### {company.status}: {company.title}",
                f"**Score:** {company.score}",
                f"**Projects:** {company.projects}",
                f"**People:** {company.people}",
                "",
            ])

    lines.extend([
        "## Platform Priorities",
        "",
    ])

    if recommendations:
        for r in recommendations:
            lines.extend([
                f"### Priority {r['priority']} — {r['severity']}",
                f"**Owner:** {r['owner']}",
                f"**Action:** {r['action']}",
                f"**Impact:** {r['impact']}",
                "",
            ])
    else:
        lines.append("No immediate platform risks detected.")

    return "\n".join(lines)
