"""Canonical executive runtime state for Alfred."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.board.board_registry import BoardGovernance, build_board_governance
from src.followups.followup_intelligence import FollowupIntelligence
from src.knowledge.executive_knowledge_builder import ExecutiveKnowledgeModel
from src.knowledge.knowledge_graph import KnowledgeGraphModel
from src.knowledge.providers.legacy_adapter import LegacyKnowledgeAdapter, build_legacy_knowledge_adapter
from src.meeting.meeting_intelligence import MeetingBrief, build_meeting_brief
from src.openloops.open_loop_intelligence import OpenLoopIntelligence
from src.operations.config_registry import build_configuration_registry


@dataclass(frozen=True)
class ExecutiveState:
    adapter: LegacyKnowledgeAdapter | None = None
    board: BoardGovernance | None = None
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
    meeting_subject: str | None = None,
    vault_root: Path | None = None,
    knowledge_provider: str | None = None,
) -> ExecutiveState:
    provider = _resolve_knowledge_provider(knowledge_provider, vault_root)
    adapter = build_legacy_knowledge_adapter(evidence_root, vault_root=vault_root)
    engine_result = adapter.engine_result
    vault = adapter.vault
    knowledge_model = adapter.knowledge_model
    relationship_graph = adapter.relationship_graph
    board = build_board_governance()
    meetings = _build_meetings(meeting_subject, vault_root, adapter)
    followups = adapter.get_followups()
    open_loops = adapter.get_open_loops()

    objectives = adapter.get_objectives()
    projects = adapter.get_projects()
    companies = adapter.get_companies()
    people = adapter.get_people()
    policies = adapter.get_policies()
    decisions = adapter.get_decisions()
    risks = adapter.get_risks()
    priorities = adapter.get_priorities()
    suppliers = tuple(_filter_suppliers(companies))
    entities = adapter.entities
    neighbours = adapter.get_neighbours()

    objective_health = _build_objective_health(objectives, vault)
    project_health = _build_project_health(projects, vault)
    recommendations = (
        _dedupe(
            priorities[:3],
            [meetings[0].recommended_discussion[0]] if meetings and meetings[0].recommended_discussion else [],
            followups.recommendations[:2],
            open_loops.recommended_actions[:2],
            knowledge_model.recommended_actions[:2],
        )
        if knowledge_model.entities and knowledge_model.source_mode == "live_vault"
        else ()
    )
    confidence = _derive_confidence(engine_result, followups, open_loops, relationship_graph)
    summary = _build_summary(
        board=board,
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
        adapter=adapter,
        board=board,
        objectives=objectives,
        projects=projects,
        companies=companies,
        people=people,
        meetings=meetings,
        decisions=decisions,
        risks=risks,
        policies=policies,
        followups=followups,
        open_loops=open_loops,
        executive_health=engine_result["health"],
        objective_health=objective_health,
        project_health=project_health,
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


def _resolve_knowledge_provider(knowledge_provider: str | None, vault_root: Path | None) -> str:
    provider = knowledge_provider or build_configuration_registry(vault_path=vault_root).default_knowledge_provider
    if provider != "legacy_adapter":
        raise ValueError(f"Unsupported knowledge provider: {provider}")
    return provider


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
        f"Canonical graph covers {relationship_graph.statistics['node_count']} nodes and {relationship_graph.statistics['edge_count']} edges.",
        f"Runtime state includes {len(objectives)} objectives, {len(projects)} projects, {len(companies)} companies, {len(people)} people, {len(decisions)} decisions, and {len(policies)} policies.",
        f"Operational pressure includes {len(followups.overdue)} overdue follow-ups and {len(open_loops.critical_open_loops)} critical open loops.",
        f"Entity resolution currently exposes {len(knowledge_model.aliases)} aliases across {len(knowledge_model.canonical_entities)} canonical entities.",
        f"Runtime confidence is {confidence}.",
    )


def _build_meetings(
    meeting_subject: str | None,
    vault_root: Path | None,
    adapter: LegacyKnowledgeAdapter,
) -> tuple[MeetingBrief, ...]:
    subject = (meeting_subject or "").strip()
    if subject:
        brief = build_meeting_brief(subject, vault_root=vault_root)
        return (brief,) if _meeting_has_evidence(brief) else ()

    candidate = next((entity.title for entity in adapter.knowledge_model.entities if entity.entity_type == "meeting"), None)
    if candidate:
        brief = build_meeting_brief(candidate, vault_root=vault_root)
        return (brief,) if _meeting_has_evidence(brief) else ()
    return ()


def _meeting_has_evidence(brief: MeetingBrief) -> bool:
    return bool(
        brief.matched_entities
        or brief.evidence_note_count
        or brief.related_people
        or brief.related_projects
        or brief.related_companies
        or brief.related_objectives
        or brief.related_decisions
        or brief.open_loops
        or brief.follow_ups
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
