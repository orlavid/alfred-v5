from pathlib import Path

from executive.parser import parse_services
from executive.health import platform_health
from executive.risks import build_risks
from executive.recommendations import build_recommendations
from executive.engine import execute
from executive.report import render

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

engine_result = execute(EVIDENCE)
assert engine_result["health"]["failed"] == 4
assert engine_result["timers"]["timer_count"] == 25
assert engine_result["docker"]["container_count"] == 2
assert engine_result["docker"]["running"] == 1
assert engine_result["docker"]["exited"] == 1
assert "FAILED: hermes-5am-check.service" in engine_result["risks"]

report = render(engine_result)
assert "Timers Detected | 25" in report
assert "Docker Containers | 2" in report
assert "Knowledge Graph Edges | 21310" in report
assert "Unresolved Links | 4890" in report
assert "Objectives Analysed | 35" in report
assert "Objective Intelligence" in report

print("PASS: Executive Review pipeline")
