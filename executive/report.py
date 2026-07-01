def render(health, risks):
    lines = []

    score = health["score"]

    if score >= 95:
        status = "🟢 GREEN"
    elif score >= 80:
        status = "🟠 AMBER"
    else:
        status = "🔴 RED"

    lines.append("# Executive Review")
    lines.append("")
    lines.append("## Executive Health")
    lines.append("")
    lines.append(f"Overall Score: **{score} / 100**")
    lines.append(f"Overall Status: **{status}**")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|-------|------:|")
    lines.append(f"| Running Services | {health['running']} |")
    lines.append(f"| Failed Services | {health['failed']} |")
    lines.append("")

    lines.append("## Executive Priorities")
    lines.append("")

    if risks:
        for i, risk in enumerate(risks, start=1):
            lines.append(f"{i}. {risk}")
    else:
        lines.append("No immediate platform risks detected.")

    lines.append("")
    lines.append("## Executive Assessment")
    lines.append("")

    if health["failed"] == 0:
        lines.append(
            "Platform is healthy with no failed services detected."
        )
    else:
        lines.append(
            f"{health['failed']} failed services require investigation before production deployment."
        )

    return "\n".join(lines)
