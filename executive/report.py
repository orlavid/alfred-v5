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
    resolution = vault.get("resolution", {})
    recommendations = build_recommendations(risks)
    knowledge_findings = vault.get("findings", [])

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
        f"| Resolution Keys | {resolution.get('resolution_keys', 0)} |",
        f"| Ambiguous Entity Keys | {resolution.get('ambiguous_keys', 0)} |",
        "",
    ]

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

    lines.extend([
        "## Executive Priorities",
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
