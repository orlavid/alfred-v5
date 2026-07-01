from pathlib import Path

from executive.parser import parse_services
from executive.health import platform_health
from executive.risks import build_risks
from executive.recommendations import build_recommendations

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "alfred-inventory"

services = parse_services(EVIDENCE)
health = platform_health(services)
risks = build_risks(services)
recommendations = build_recommendations(risks)

assert health["failed"] == 4
assert health["score"] == 80
assert health["status"] == "AMBER"

assert "FAILED: alfred-retrieval-daily.service" in risks
assert "FAILED: hermes-5am-check.service" in risks

assert len(recommendations) == 4

fallback = build_recommendations(["FAILED: unknown-test.service"])
assert fallback[0]["priority"] == 99
assert fallback[0]["action"] == "Investigate failed service: unknown-test.service"

print("PASS: Executive Review pipeline")
