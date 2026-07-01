def render(health, risks):
    lines = []

    lines.append("# Executive Review")
    lines.append("")
    lines.append("## Executive Health")
    lines.append("")
    lines.append(f"Overall Score: **{health['score']} / 100**")
    lines.append("")
    lines.append(f"Running Services: {health['running']}")
    lines.append(f"Failed Services: {health['failed']}")
    lines.append("")
    lines.append("## Executive Risks")
    lines.append("")

    if risks:
        for r in risks:
            lines.append(f"- {r}")
    else:
        lines.append("- No risks detected.")

    return "\n".join(lines)
