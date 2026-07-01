from executive.parser import parse_services
from executive.health import platform_health
from executive.risks import build_risks

def analyze(evidence_root):
    services = parse_services(evidence_root)

    return {
        "health": platform_health(services),
        "risks": build_risks(services),
    }
