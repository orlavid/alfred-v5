from pathlib import Path
import yaml

RULES = Path(__file__).resolve().parent / "rules" / "systemd_recommendations.yml"

def load_rules():
    return yaml.safe_load(RULES.read_text()) or {}

def build_recommendations(risks):
    mapping = load_rules()
    recommendations = []

    for risk in risks:
        service = risk.replace("FAILED: ", "")

        if service in mapping:
            recommendations.append(mapping[service])
        else:
            recommendations.append({
                "priority": 99,
                "severity": "MEDIUM",
                "owner": "Platform Engineering",
                "action": f"Investigate failed service: {service}",
                "impact": "A failed service may reduce platform reliability."
            })

    recommendations.sort(key=lambda r: r["priority"])
    return recommendations
