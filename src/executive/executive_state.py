"""Canonical executive runtime state for Alfred."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from executive.engine import execute
from src.board.board_intelligence import BoardIntelligence, build_board_intelligence_from_state
from src.board.board_registry import BoardGovernance, build_board_governance
from src.followups.followup_intelligence import FollowupIntelligence, build_followup_intelligence
from src.knowledge.executive_knowledge_builder import ExecutiveKnowledgeModel, build_executive_knowledge
from src.knowledge.knowledge_graph import KnowledgeGraphModel, build_knowledge_graph_from_model
from src.meeting.meeting_intelligence import MeetingBrief, build_meeting_brief
from src.openloops.open_loop_intelligence import OpenLoopIntelligence, build_open_loop_intelligence
from src.planning.executive_planner import ExecutivePlan, build_executive_plans_from_inputs

DEFAULT_MEETING_SUBJECT = "Barclays"


@dataclass(frozen=True)
class ExecutiveState:
    board: BoardGovernance | None = None
    board_intelligence: BoardIntelligence | None = None
    objectives: tuple[Any, ...] = ()
    projects: tuple[Any, ...] = ()
    companies: tuple[Any, ...] = ()
    people: tuple[Any, ...] = ()
    meetings: tuple[MeetingBrief, ...] = ()
    decisions: tuple[dict[str, Any], ...] = ()
    risks: tuple[Any, ...] = ()
    policies: tuple[Any, ...] = ()
    followups: FollowupIntelligence | None = None
    open_loops: OpenLoopIntelligence | None = None
    executive_health: dict[str, Any] = field(default_factory=dict)
    objective_health: dict[str, Any] = field(default_factory=dict)
    project_health: dict[str, Any] = field(default_factory=dict)
    executive_plans: tuple[ExecutivePlan, ...] = ()
    recommendations: tuple[str, ...] = ()
    relationship_graph: KnowledgeGraphModel | None = None
    confidence: str = "LOW"
    summary: tuple[str, ...] = ()
    priorities: tuple[dict[str, Any], ...] = ()
    suppliers: tuple[Any, ...] = ()
    engine_result: dict[str, Any] = field(default_factory=dict)
    vault: dict[str, Any] = field(default_factory=dict)
    entities: tuple[Any, ...] = ()
    neighbours: dict[str, tuple[str, ...]] = field(default_factory=dict)
    knowledge_model: ExecutiveKnowledgeModel | None = None


def build_executive_state(
    evidence_root: Path,
    *,
    meeting_subject: str = DEFAULT_MEETING_SUBJECT,
) -> ExecutiveState:
    engine_result = execute(evidence_root)
    vault = engine_result["knowledge"]["vault"]
    knowledge_model = build_executive_knowledge(evidence_root)
    relationship_graph = build_knowledge_graph_from_model(knowledge_model)
    board = build_board_governance()
    meeting = build_meeting_brief(meeting_subject)
    followups = build_followup_intelligence()
    open_loops = build_open_loop_intelligence()

    objectives = tuple(sorted(vault.get("objectives", {}).get("insights", []), key=_title_key))
    projects = tuple(sorted(vault.get("projects", {}).get("insights", []), key=_title_key))
    companies = tuple(sorted(vault.get("companies", {}).get("insights", []), key=_title_key))
    people = tuple(sorted(vault.get("people", {}).get("insights", []), key=_title_key))
    policies = tuple(
        sorted(
            (entity for entity in knowledge_model.entities if entity.entity_type == "policy"),
            key=lambda entity: (entity.title.lower(), entity.path),
        )
    )
    decisions = tuple(
        sorted(
            vault.get("decisions", {}).get("top_decisions", []),
            key=lambda item: (-item.get("importance", 0), item.get("title", "").lower()),
        )
    )
    risks = tuple(vault.get("risk", {}).get("high_risk", []))
    priorities = tuple(vault.get("priorities", {}).get("top_priorities", []))
    suppliers = tuple(_filter_suppliers(companies))
    entities = tuple(vault.get("entities", []))
    neighbours = _build_neighbours(vault.get("graph", {}).get("edges", []))

    objective_health = _build_objective_health(objectives, vault)
    project_health = _build_project_health(projects, vault)
    executive_plans = build_executive_plans_from_inputs(
        projects=projects,
        people=people,
        entities=entities,
        neighbours=neighbours,
        project_health=project_health,
    ).plans
    draft_state = ExecutiveState(
        board=board,
        board_intelligence=None,
        objectives=objectives,
        projects=projects,
        companies=companies,
        people=people,
        meetings=(meeting,),
        decisions=decisions,
        risks=risks,
        policies=policies,
        followups=followups,
        open_loops=open_loops,
        executive_health=engine_result["health"],
        objective_health=objective_health,
        project_health=project_health,
        executive_plans=executive_plans,
        recommendations=(),
        relationship_graph=relationship_graph,
        confidence="LOW",
        summary=(),
        priorities=priorities,
        suppliers=suppliers,
        engine_result=engine_result,
        vault=vault,
        entities=entities,
        neighbours=neighbours,
        knowledge_model=knowledge_model,
    )
    board_intelligence = build_board_intelligence_from_state(draft_state)
    recommendations = _dedupe(
        priorities[:3],
        [meeting.recommended_discussion[0]] if meeting.recommended_discussion else [],
        followups.recommendations[:2],
        open_loops.recommended_actions[:2],
        knowledge_model.recommended_actions[:2],
    )
    confidence = _derive_confidence(engine_result, followups, open_loops, relationship_graph)
    summary = _build_summary(
        board=board,
        board_intelligence=board_intelligence,
        objectives=objectives,
        projects=projects,
        companies=companies,
        people=people,
        decisions=decisions,
        policies=policies,
        followups=followups,
        open_loops=open_loops,
        relationship_graph=relationship_graph,
        knowledge_model=knowledge_model,
        executive_health=engine_result["health"],
        confidence=confidence,
    )

    return ExecutiveState(
        board=board,
        board_intelligence=board_intelligence,
        objectives=objectives,
        projects=projects,
        companies=companies,
        people=people,
        meetings=(meeting,),
        decisions=decisions,
        risks=risks,
        policies=policies,
        followups=followups,
        open_loops=open_loops,
        executive_health=engine_result["health"],
        objective_health=objective_health,
        project_health=project_health,
        executive_plans=executive_plans,
        recommendations=recommendations,
        relationship_graph=relationship_graph,
        confidence=confidence,
        summary=summary,
        priorities=priorities,
        suppliers=suppliers,
        engine_result=engine_result,
        vault=vault,
        entities=entities,
        neighbours=neighbours,
        knowledge_model=knowledge_model,
    )


def render_executive_state_summary(state: ExecutiveState) -> str:
    relationship_graph = state.relationship_graph
    graph_stats = relationship_graph.statistics if relationship_graph is not None else {}
    node_counts = graph_stats.get("node_counts", {})
    relationship_counts = graph_stats.get("relationship_counts", {})
    parts = [
        "# ExecutiveState Summary",
        "",
        "## Summary",
        "",
    ]
    parts.extend(_render_bullets(state.summary))
    parts.extend(["", "## Board", ""])
    parts.extend(_render_bullets([
        f"Board members: {len(state.board.board_members) if state.board else 0}.",
        f"Weekly board agenda items: {len(state.board.standing_agenda) if state.board else 0}.",
        f"Board proposed updates: {len(state.board_intelligence.monthly_review.proposed_executive_updates) if state.board_intelligence else 0}.",
    ]))
    parts.extend(["", "## Entity Coverage", ""])
    parts.extend(_render_bullets([
        f"Objectives: {len(state.objectives)}.",
        f"Projects: {len(state.projects)}.",
        f"Companies: {len(state.companies)}.",
        f"People: {len(state.people)}.",
        f"Decisions: {len(state.decisions)}.",
        f"Policies: {len(state.policies)}.",
        f"Canonical nodes: {graph_stats.get('node_count', 0)}.",
        f"Canonical edges: {graph_stats.get('edge_count', 0)}.",
    ]))
    parts.extend(["", "## Health", ""])
    parts.extend(_render_bullets([
        f"Executive health: {state.executive_health.get('status', 'UNKNOWN')} ({state.executive_health.get('score', 0)} / 100).",
        f"Objective health: supported {state.objective_health.get('supported', 0)}, at risk {state.objective_health.get('at_risk', 0)}, watch {state.objective_health.get('watch', 0)}.",
        f"Project health: supported {state.project_health.get('supported', 0)}, at risk {state.project_health.get('at_risk', 0)}, watch {state.project_health.get('watch', 0)}.",
        f"Draft executive plans: {len(state.executive_plans)}.",
    ]))
    parts.extend(["", "## Graph Detail", ""])
    parts.extend(_render_bullets([
        f"{key}: {value}" for key, value in sorted(node_counts.items())
    ] + [
        f"{key}: {value}" for key, value in sorted(relationship_counts.items())
    ]))
    parts.extend(["", "## Recommendations", ""])
    parts.extend(_render_bullets(state.recommendations))
    parts.extend(["", "## Confidence", "", f"- {state.confidence}", ""])
    return "\n".join(parts)


def _build_objective_health(objectives: tuple[Any, ...], vault: dict[str, Any]) -> dict[str, Any]:
    objective_vault = vault.get("objectives", {})
    return {
        "total": len(objectives),
        "supported": objective_vault.get("supported", 0),
        "at_risk": objective_vault.get("at_risk", _status_count(objectives, "AT RISK")),
        "watch": _status_count(objectives, "WATCH"),
    }


def _build_project_health(projects: tuple[Any, ...], vault: dict[str, Any]) -> dict[str, Any]:
    project_vault = vault.get("projects", {})
    return {
        "total": len(projects),
        "supported": project_vault.get("supported", _status_count(projects, "SUPPORTED")),
        "at_risk": project_vault.get("at_risk", _status_count(projects, "AT RISK")),
        "watch": _status_count(projects, "WATCH"),
    }


def _status_count(items: tuple[Any, ...], target: str) -> int:
    return sum(1 for item in items if getattr(item, "status", None) == target)


def _build_summary(
    *,
    board: BoardGovernance,
    board_intelligence: BoardIntelligence,
    objectives: tuple[Any, ...],
    projects: tuple[Any, ...],
    companies: tuple[Any, ...],
    people: tuple[Any, ...],
    decisions: tuple[dict[str, Any], ...],
    policies: tuple[Any, ...],
    followups: FollowupIntelligence,
    open_loops: OpenLoopIntelligence,
    relationship_graph: KnowledgeGraphModel,
    knowledge_model: ExecutiveKnowledgeModel,
    executive_health: dict[str, Any],
    confidence: str,
) -> tuple[str, ...]:
    return (
        f"Executive health is {executive_health['status']} with score {executive_health['score']} / 100.",
        f"Board registry contains {len(board.board_members)} members and {len(board.decision_rights)} explicit decision rights.",
        f"Board intelligence currently proposes {len(board_intelligence.monthly_review.proposed_executive_updates)} approval-gated executive updates.",
        f"Canonical graph covers {relationship_graph.statistics['node_count']} nodes and {relationship_graph.statistics['edge_count']} edges.",
        f"Runtime state includes {len(objectives)} objectives, {len(projects)} projects, {len(companies)} companies, {len(people)} people, {len(decisions)} decisions, and {len(policies)} policies.",
        f"Operational pressure includes {len(followups.overdue)} overdue follow-ups and {len(open_loops.critical_open_loops)} critical open loops.",
        f"Entity resolution currently exposes {len(knowledge_model.aliases)} aliases across {len(knowledge_model.canonical_entities)} canonical entities.",
        f"Runtime confidence is {confidence}.",
    )


def _filter_suppliers(companies: tuple[Any, ...]) -> list[Any]:
    return [
        company
        for company in companies
        if getattr(company, "status", None) in {"CRITICAL", "IMPORTANT"}
        and getattr(company, "path", "").startswith("04 Companies/")
    ]


def _derive_confidence(
    engine_result: dict[str, Any],
    followups: FollowupIntelligence,
    open_loops: OpenLoopIntelligence,
    relationship_graph: KnowledgeGraphModel,
) -> str:
    if (
        engine_result["health"]["status"] == "AMBER"
        and len(followups.high_priority) >= 5
        and len(open_loops.critical_open_loops) >= 5
        and relationship_graph.statistics["node_count"] >= 10
    ):
        return "HIGH"
    if len(followups.overdue) >= 1 or len(open_loops.critical_open_loops) >= 1:
        return "MEDIUM"
    return "LOW"


def _dedupe(*groups: Any) -> tuple[str, ...]:
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
    return tuple(deduped[:10])


def _build_neighbours(edges: list[dict[str, Any]]) -> dict[str, tuple[str, ...]]:
    neighbours: dict[str, set[str]] = {}
    for edge in edges:
        source = edge["source"]
        target = edge["target"]
        neighbours.setdefault(source, set()).add(target)
        neighbours.setdefault(target, set()).add(source)
    return {
        entity_id: tuple(sorted(linked))
        for entity_id, linked in sorted(neighbours.items())
    }


def _title_key(item: Any) -> tuple[str, str]:
    return (getattr(item, "title", "").lower(), getattr(item, "path", ""))


def _render_bullets(values: tuple[str, ...] | list[str]) -> list[str]:
    rendered = [f"- {value}" for value in values if value]
    return rendered or ["_None found._"]
