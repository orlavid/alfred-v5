def build_risks(services):
    risks = []
    for s in services:
        if (
            s["active"] == "failed"
            or s["state"] == "failed"
            or s["load"] == "failed"
        ):
            risks.append(f"FAILED: {s['name']}")
    return risks