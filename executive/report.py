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
    recommendations = build_recommendations(risks)

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
        "",
        "## Executive Priorities",
        "",
    ]

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
