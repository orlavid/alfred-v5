"""Shared executive knowledge engine for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from executive.engine import execute
from src.followups.followup_intelligence import FollowupIntelligence, build_followup_intelligence
from src.meeting.meeting_intelligence import MeetingBrief, build_meeting_brief
from src.openloops.open_loop_intelligence import OpenLoopIntelligence, build_open_loop_intelligence

DEFAULT_MEETING_SUBJECT = "Barclays"


@dataclass(frozen=True)
class ExecutiveState:
    executive_health: dict
    priorities: list[dict]
    objectives: list
    meetings: list[MeetingBrief]
    followups: FollowupIntelligence
    open_loops: OpenLoopIntelligence
    projects: list
    suppliers: list
    people: list
    risks: list[dict] | list[str]
    recommendations: list[str]
    confidence: str
    engine_result: dict
    vault: dict


def build_executive_state(
    evidence_root: Path,
    *,
    meeting_subject: str = DEFAULT_MEETING_SUBJECT,
) -> ExecutiveState:
    engine_result = execute(evidence_root)
    vault = engine_result["knowledge"]["vault"]
    meeting = build_meeting_brief(meeting_subject)
    followups = build_followup_intelligence()
    open_loops = build_open_loop_intelligence()

    recommendations = _dedupe(
        vault.get("do_next", {}).get("top_10", [])[:3],
        [meeting.recommended_discussion[0]] if meeting.recommended_discussion else [],
        followups.recommendations[:2],
        open_loops.recommended_actions[:2],
    )

    confidence = _derive_confidence(engine_result, followups, open_loops)

    return ExecutiveState(
        executive_health=engine_result["health"],
        priorities=vault.get("priorities", {}).get("top_priorities", []),
        objectives=vault.get("objectives", {}).get("insights", []),
        meetings=[meeting],
        followups=followups,
        open_loops=open_loops,
        projects=vault.get("projects", {}).get("insights", []),
        suppliers=_filter_suppliers(vault.get("companies", {}).get("insights", [])),
        people=vault.get("people", {}).get("insights", []),
        risks=vault.get("risk", {}).get("high_risk", []),
        recommendations=recommendations,
        confidence=confidence,
        engine_result=engine_result,
        vault=vault,
    )


def _filter_suppliers(companies: list) -> list:
    return [
        company
        for company in companies
        if company.status in {"CRITICAL", "IMPORTANT"} and company.path.startswith("04 Companies/")
    ]


def _derive_confidence(engine_result: dict, followups: FollowupIntelligence, open_loops: OpenLoopIntelligence) -> str:
    if (
        engine_result["health"]["status"] == "AMBER"
        and len(followups.high_priority) >= 5
        and len(open_loops.critical_open_loops) >= 5
    ):
        return "HIGH"
    if len(followups.overdue) >= 1 or len(open_loops.critical_open_loops) >= 1:
        return "MEDIUM"
    return "LOW"


def _dedupe(*groups) -> list[str]:
    values: list[str] = []
    for group in groups:
        for item in group:
            if isinstance(item, dict) and "action" in item:
                values.append(item["action"])
            elif isinstance(item, str):
                values.append(item)

    deduped: list[str] = []
    seen = set()
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped[:10]
