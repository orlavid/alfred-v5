def build_recommendations(risks):
    mapping = {
        "alfred-retrieval-daily.service": {
            "priority": 1,
            "action": "Restore daily retrieval validation",
            "impact": "Daily retrieval quality is not being verified."
        },
        "alfred-retrieval-weekly.service": {
            "priority": 2,
            "action": "Restore weekly retrieval regression testing",
            "impact": "Long-term retrieval regressions may go undetected."
        },
        "alfred-v3-harness.service": {
            "priority": 3,
            "action": "Repair Alfred V3 retrieval harness",
            "impact": "V3 validation is unavailable."
        },
        "hermes-5am-check.service": {
            "priority": 4,
            "action": "Restore Hermes 5am self-check",
            "impact": "Morning platform health checks are not executing."
        },
    }

    recommendations = []

    for risk in risks:
        service = risk.replace("FAILED: ", "")
        if service in mapping:
            recommendations.append(mapping[service])

    recommendations.sort(key=lambda r: r["priority"])
    return recommendations
