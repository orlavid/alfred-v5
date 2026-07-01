from executive.recommendations import build_recommendations

STATUS_ICON = {
    "GREEN": "🟢",
    "AMBER": "🟠",
    "RED": "🔴",
}

def render(health, risks):
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
