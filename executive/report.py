from executive.recommendations import build_recommendations

def render(health, risks):
    recommendations = build_recommendations(risks)

    score = health["score"]

    if score >= 95:
        status = "🟢 GREEN"
    elif score >= 80:
        status = "🟠 AMBER"
    else:
        status = "🔴 RED"

    lines = [
        "# Executive Review",
        "",
        "## Executive Health",
        "",
        f"Overall Score: **{score} / 100**",
        f"Overall Status: **{status}**",
        "",
        "| Metric | Value |",
        "|-------|------:|",
        f"| Running Services | {health['running']} |",
        f"| Failed Services | {health['failed']} |",
        "",
        "## Executive Priorities",
        ""
    ]

    if recommendations:
        for r in recommendations:
            lines.extend([
                f"### Priority {r['priority']}",
                f"**Action:** {r['action']}",
                f"**Impact:** {r['impact']}",
                ""
            ])
    else:
        lines.append("No immediate platform risks detected.")

    return "\n".join(lines)
