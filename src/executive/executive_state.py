"""Canonical executive runtime state for Alfred."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any

from src.board.board_registry import BoardGovernance, build_board_governance
from executive.intelligence.ownership import infer_ownership
from executive.knowledge.companies import CompanyInsight
from executive.knowledge.entity_contract import CanonicalExecutiveEntityContract
from executive.knowledge.entity_quality import build_executive_entity_quality
from executive.knowledge.objectives import ObjectiveInsight
from executive.knowledge.projects import ProjectInsight
from executive.intelligence.people import PersonInsight
from executive.knowledge.resolver import build_entity_resolution
from src.followups.followup_intelligence import FollowupIntelligence
from src.knowledge.executive_knowledge_builder import ExecutiveKnowledgeModel
from src.knowledge.knowledge_graph import KnowledgeGraphModel
from src.knowledge.providers.legacy_adapter import LegacyKnowledgeAdapter, build_legacy_knowledge_adapter
from src.meeting.meeting_intelligence import MeetingBrief, build_meeting_brief
from src.openloops.open_loop_intelligence import OpenLoopIntelligence
from src.operations.config_registry import build_configuration_registry
from src.executive.work_item_contract import (
    ExecutiveWorkItemContract,
    build_executive_work_items,
    project_followups_from_work_items,
    project_open_loops_from_work_items,
)


@dataclass(frozen=True)
class ExecutiveAssemblyStage:
    name: str
    duration_ms: float
    dependencies: tuple[str, ...] = ()
    produces: tuple[str, ...] = ()
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutiveAssemblyPipelineResult:
    state: "ExecutiveState"
    stages: tuple[ExecutiveAssemblyStage, ...]
    diagnostics: dict[str, dict[str, Any]] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutiveAssemblyRequest:
    evidence_root: Path
    meeting_subject: str | None = None
    requested_vault_root: Path | None = None
    requested_knowledge_provider: str | None = None


@dataclass(frozen=True)
class KnowledgeAcquisitionOutput:
    effective_vault_root: Path
    provider: str
    adapter: LegacyKnowledgeAdapter
    engine_result: dict[str, Any]
    vault: dict[str, Any]
    knowledge_model: ExecutiveKnowledgeModel
    relationship_graph: KnowledgeGraphModel
    board: BoardGovernance
    meetings: tuple[MeetingBrief, ...]
    source_followups: FollowupIntelligence
    source_open_loops: OpenLoopIntelligence
    entities: tuple[Any, ...]
    neighbours: dict[str, tuple[str, ...]]
    policies: tuple[Any, ...]
    risks: tuple[Any, ...]
    priorities: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class EntityProjectionOutput:
    resolution_model: Any
    canonical_entities: tuple[CanonicalExecutiveEntityContract, ...]
    projection_context: dict[str, Any]
    objectives: tuple[Any, ...]
    projects: tuple[Any, ...]
    companies: tuple[Any, ...]
    people: tuple[Any, ...]
    decisions: tuple[dict[str, Any], ...]
    suppliers: tuple[Any, ...]


@dataclass(frozen=True)
class WorkItemProjectionOutput:
    work_items: tuple[ExecutiveWorkItemContract, ...]
    followups: FollowupIntelligence
    open_loops: OpenLoopIntelligence
    objective_health: dict[str, Any]
    project_health: dict[str, Any]
    recommendations: tuple[str, ...]
    confidence: str


@dataclass(frozen=True)
class ReadModelAssemblyOutput:
    state_seed: "ExecutiveState"
    read_model: Any


@dataclass(frozen=True)
class IntentGenerationOutput:
    reasoning: Any


@dataclass(frozen=True)
class PresentationGenerationOutput:
    presentation: Any


@dataclass(frozen=True)
class FinalisationOutput:
    state: "ExecutiveState"


@dataclass(frozen=True)
class ExecutiveState:
    adapter: LegacyKnowledgeAdapter | None = None
    board: BoardGovernance | None = None
    canonical_entities: tuple[CanonicalExecutiveEntityContract, ...] = ()
    work_items: tuple[ExecutiveWorkItemContract, ...] = ()
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
    return run_executive_assembly_pipeline(
        evidence_root,
        meeting_subject=meeting_subject,
        vault_root=vault_root,
        knowledge_provider=knowledge_provider,
    ).state


def run_executive_assembly_pipeline(
    evidence_root: Path,
    *,
    meeting_subject: str | None = None,
    vault_root: Path | None = None,
    knowledge_provider: str | None = None,
) -> ExecutiveAssemblyPipelineResult:
    request = ExecutiveAssemblyRequest(
        evidence_root=evidence_root,
        meeting_subject=meeting_subject,
        requested_vault_root=vault_root,
        requested_knowledge_provider=knowledge_provider,
    )
    stages: list[ExecutiveAssemblyStage] = []
    knowledge = _run_stage(
        stages,
        "knowledge_acquisition",
        ("request",),
        ("knowledge",),
        lambda: run_knowledge_acquisition_stage(request),
    )
    entity_projection = _run_stage(
        stages,
        "entity_projection",
        ("knowledge",),
        ("entity_projection",),
        lambda: run_entity_projection_stage(knowledge),
    )
    work_item_projection = _run_stage(
        stages,
        "work_item_projection",
        ("knowledge", "entity_projection"),
        ("work_item_projection",),
        lambda: run_work_item_projection_stage(knowledge, entity_projection),
    )
    read_model_assembly = _run_stage(
        stages,
        "read_model_assembly",
        ("knowledge", "entity_projection", "work_item_projection"),
        ("read_model_assembly",),
        lambda: run_read_model_assembly_stage(knowledge, entity_projection, work_item_projection),
    )
    intent_generation = _run_stage(
        stages,
        "intent_generation",
        ("read_model_assembly",),
        ("intent_generation",),
        lambda: run_intent_generation_stage(read_model_assembly),
    )
    presentation_generation = _run_stage(
        stages,
        "presentation_generation",
        ("read_model_assembly", "intent_generation"),
        ("presentation_generation",),
        lambda: run_presentation_generation_stage(read_model_assembly, intent_generation),
    )
    finalisation = _run_stage(
        stages,
        "executive_state_finalisation",
        ("knowledge", "entity_projection", "work_item_projection", "presentation_generation"),
        ("state",),
        lambda: run_executive_state_finalisation_stage(
            knowledge,
            entity_projection,
            work_item_projection,
            presentation_generation,
        ),
    )

    diagnostics = {stage.name: dict(stage.diagnostics) for stage in stages}
    return ExecutiveAssemblyPipelineResult(
        state=finalisation.state,
        stages=tuple(stages),
        diagnostics=diagnostics,
    )


def _run_stage(
    stages: list[ExecutiveAssemblyStage],
    name: str,
    dependencies: tuple[str, ...],
    produces: tuple[str, ...],
    stage_fn,
):
    started = perf_counter()
    output, diagnostics = stage_fn()
    stages.append(
        ExecutiveAssemblyStage(
            name=name,
            duration_ms=round((perf_counter() - started) * 1000, 3),
            dependencies=dependencies,
            produces=produces,
            diagnostics=diagnostics,
        )
    )
    return output


def run_knowledge_acquisition_stage(request: ExecutiveAssemblyRequest) -> tuple[KnowledgeAcquisitionOutput, dict[str, Any]]:
    effective_vault_root = _resolve_vault_root(request.requested_vault_root)
    provider = _resolve_knowledge_provider(request.requested_knowledge_provider, effective_vault_root)
    adapter = build_legacy_knowledge_adapter(request.evidence_root, vault_root=effective_vault_root)
    engine_result = adapter.engine_result
    vault = adapter.vault
    knowledge_model = adapter.knowledge_model
    relationship_graph = adapter.relationship_graph
    board = build_board_governance()
    meetings = _build_meetings(request.meeting_subject, effective_vault_root, adapter)
    source_followups = adapter.get_followups()
    source_open_loops = adapter.get_open_loops()
    entities = adapter.entities
    neighbours = adapter.get_neighbours()
    output = KnowledgeAcquisitionOutput(
        effective_vault_root=effective_vault_root,
        provider=provider,
        adapter=adapter,
        engine_result=engine_result,
        vault=vault,
        knowledge_model=knowledge_model,
        relationship_graph=relationship_graph,
        board=board,
        meetings=meetings,
        source_followups=source_followups,
        source_open_loops=source_open_loops,
        entities=entities,
        neighbours=neighbours,
        policies=adapter.get_policies(),
        risks=adapter.get_risks(),
        priorities=adapter.get_priorities(),
    )
    return output, {
        "provider": provider,
        "vault_root": str(effective_vault_root),
        "entity_count": len(entities),
        "meeting_count": len(meetings),
        "followup_count": source_followups.followup_count,
        "open_loop_count": source_open_loops.open_loop_count,
    }


def run_entity_projection_stage(knowledge: KnowledgeAcquisitionOutput) -> tuple[EntityProjectionOutput, dict[str, Any]]:
    entities = knowledge.entities
    vault = knowledge.vault
    neighbours = knowledge.neighbours
    resolution_model = build_entity_resolution(entities)
    canonical_entities = build_executive_entity_quality(
        entities,
        resolution_model,
        graph=vault.get("graph", {}),
        objective_analysis=vault.get("objectives", {}),
        project_analysis=vault.get("projects", {}),
        company_analysis=vault.get("companies", {}),
        people_analysis=vault.get("people", {}),
        decision_analysis=vault.get("decisions", {}),
        risk_analysis=vault.get("risk", {}),
        ownership=vault.get("ownership", {}),
    ).canonical_entities
    projection_context = _build_projection_context(canonical_entities, entities, neighbours)

    objectives = _project_objectives(canonical_entities, projection_context)
    projects = _project_projects(canonical_entities, projection_context)
    companies = _project_companies(canonical_entities, projection_context)
    people = _project_people(canonical_entities, projection_context)
    decisions = _project_decisions(canonical_entities, projection_context)
    suppliers = tuple(_filter_suppliers(companies))
    output = EntityProjectionOutput(
        resolution_model=resolution_model,
        canonical_entities=canonical_entities,
        projection_context=projection_context,
        objectives=objectives,
        projects=projects,
        companies=companies,
        people=people,
        decisions=decisions,
        suppliers=suppliers,
    )
    return output, {
        "canonical_entity_count": len(canonical_entities),
        "objective_count": len(objectives),
        "project_count": len(projects),
        "company_count": len(companies),
        "people_count": len(people),
        "decision_count": len(decisions),
    }


def run_work_item_projection_stage(
    knowledge: KnowledgeAcquisitionOutput,
    entity_projection: EntityProjectionOutput,
) -> tuple[WorkItemProjectionOutput, dict[str, Any]]:
    work_items = build_executive_work_items(
        followups=knowledge.source_followups,
        open_loops=knowledge.source_open_loops,
        meetings=knowledge.meetings,
    )
    followups = project_followups_from_work_items(work_items, knowledge.source_followups)
    open_loops = project_open_loops_from_work_items(work_items, knowledge.source_open_loops)
    objective_health = _build_objective_health(entity_projection.objectives, knowledge.vault)
    project_health = _build_project_health(entity_projection.projects, knowledge.vault)
    knowledge_model = knowledge.knowledge_model
    meetings = knowledge.meetings
    recommendations = (
        _dedupe(
            knowledge.priorities[:3],
            [meetings[0].recommended_discussion[0]] if meetings and meetings[0].recommended_discussion else [],
            followups.recommendations[:2],
            open_loops.recommended_actions[:2],
            knowledge_model.recommended_actions[:2],
        )
        if knowledge_model.entities and knowledge_model.source_mode == "live_vault"
        else ()
    )
    confidence = _derive_confidence(knowledge.engine_result, followups, open_loops, knowledge.relationship_graph)
    output = WorkItemProjectionOutput(
        work_items=work_items,
        followups=followups,
        open_loops=open_loops,
        objective_health=objective_health,
        project_health=project_health,
        recommendations=recommendations,
        confidence=confidence,
    )
    return output, {
        "work_item_count": len(work_items),
        "followup_projection_count": followups.followup_count,
        "open_loop_projection_count": open_loops.open_loop_count,
        "recommendation_count": len(recommendations),
        "confidence": confidence,
    }


def run_read_model_assembly_stage(
    knowledge: KnowledgeAcquisitionOutput,
    entity_projection: EntityProjectionOutput,
    work_item_projection: WorkItemProjectionOutput,
) -> tuple[ReadModelAssemblyOutput, dict[str, Any]]:
    state = _assemble_executive_state(knowledge, entity_projection, work_item_projection)
    from src.executive.read_model import build_unified_executive_read_model

    read_model = build_unified_executive_read_model(state)
    output = ReadModelAssemblyOutput(
        state_seed=state,
        read_model=read_model,
    )
    return output, {
        "entity_count": len(read_model.entities),
        "work_item_count": len(read_model.work_items),
        "action_count": len(read_model.actions),
        "relationship_nodes": knowledge.relationship_graph.statistics["node_count"],
    }


def run_intent_generation_stage(
    read_model_assembly: ReadModelAssemblyOutput,
) -> tuple[IntentGenerationOutput, dict[str, Any]]:
    from src.executive.executive_reasoning import build_executive_reasoning_from_state

    reasoning = build_executive_reasoning_from_state(read_model_assembly.state_seed)
    output = IntentGenerationOutput(reasoning=reasoning)
    return output, {
        "intent_count": len(reasoning.intents),
        "top_action_count": len(reasoning.top_actions),
        "confidence": reasoning.confidence,
    }


def run_presentation_generation_stage(
    read_model_assembly: ReadModelAssemblyOutput,
    intent_generation: IntentGenerationOutput,
) -> tuple[PresentationGenerationOutput, dict[str, Any]]:
    from src.executive.presentation_contract import build_executive_presentation_from_state

    presentation = build_executive_presentation_from_state(
        read_model_assembly.state_seed,
        reasoning=intent_generation.reasoning,
        read_model=read_model_assembly.read_model,
    )
    output = PresentationGenerationOutput(presentation=presentation)
    return output, {
        "section_count": len(presentation.sections),
        "ordered_sections": list(presentation.ordered_sections),
        "presentation_confidence": presentation.confidence,
    }


def run_executive_state_finalisation_stage(
    knowledge: KnowledgeAcquisitionOutput,
    entity_projection: EntityProjectionOutput,
    work_item_projection: WorkItemProjectionOutput,
    presentation_generation: PresentationGenerationOutput,
) -> tuple[FinalisationOutput, dict[str, Any]]:
    state = _assemble_executive_state(knowledge, entity_projection, work_item_projection)
    output = FinalisationOutput(state=state)
    return output, {
        "summary_line_count": len(state.summary),
        "recommendation_count": len(state.recommendations),
        "state_confidence": state.confidence,
        "presentation_sections": list(presentation_generation.presentation.ordered_sections),
    }


def _assemble_executive_state(
    knowledge: KnowledgeAcquisitionOutput,
    entity_projection: EntityProjectionOutput,
    work_item_projection: WorkItemProjectionOutput,
) -> ExecutiveState:
    summary = _build_summary(
        board=knowledge.board,
        objectives=entity_projection.objectives,
        projects=entity_projection.projects,
        companies=entity_projection.companies,
        people=entity_projection.people,
        decisions=entity_projection.decisions,
        policies=knowledge.policies,
        followups=work_item_projection.followups,
        open_loops=work_item_projection.open_loops,
        relationship_graph=knowledge.relationship_graph,
        knowledge_model=knowledge.knowledge_model,
        executive_health=knowledge.engine_result["health"],
        confidence=work_item_projection.confidence,
    )

    return ExecutiveState(
        adapter=knowledge.adapter,
        board=knowledge.board,
        canonical_entities=entity_projection.canonical_entities,
        work_items=work_item_projection.work_items,
        objectives=entity_projection.objectives,
        projects=entity_projection.projects,
        companies=entity_projection.companies,
        people=entity_projection.people,
        meetings=knowledge.meetings,
        decisions=entity_projection.decisions,
        risks=knowledge.risks,
        policies=knowledge.policies,
        followups=work_item_projection.followups,
        open_loops=work_item_projection.open_loops,
        executive_health=knowledge.engine_result["health"],
        objective_health=work_item_projection.objective_health,
        project_health=work_item_projection.project_health,
        recommendations=work_item_projection.recommendations,
        relationship_graph=knowledge.relationship_graph,
        confidence=work_item_projection.confidence,
        summary=summary,
        priorities=knowledge.priorities,
        suppliers=entity_projection.suppliers,
        engine_result=knowledge.engine_result,
        vault=knowledge.vault,
        entities=knowledge.entities,
        neighbours=knowledge.neighbours,
        knowledge_model=knowledge.knowledge_model,
    )


def _resolve_knowledge_provider(knowledge_provider: str | None, vault_root: Path | None) -> str:
    provider = knowledge_provider or build_configuration_registry(vault_path=vault_root).default_knowledge_provider
    if provider != "legacy_adapter":
        raise ValueError(f"Unsupported knowledge provider: {provider}")
    return provider


def _resolve_vault_root(vault_root: Path | None) -> Path:
    if vault_root is not None:
        return vault_root.expanduser()
    registry = build_configuration_registry()
    return Path(registry.configured_vault_path).expanduser()


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
        f"Canonical executive entities: {len(state.canonical_entities)}.",
        f"Canonical work items: {len(state.work_items)}.",
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
        f"ExecutiveState projects {len(objectives) + len(projects) + len(companies) + len(people)} domain views from {len(knowledge_model.canonical_entities)} canonical executive entities.",
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
        if getattr(company, "path", "").startswith("04 Companies/")
        and (
            getattr(company, "is_supplier", False)
            or getattr(company, "status", None) in {"CRITICAL", "IMPORTANT"}
        )
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


def _build_projection_context(
    canonical_entities: tuple[CanonicalExecutiveEntityContract, ...],
    raw_entities: tuple[Any, ...],
    neighbours: dict[str, tuple[str, ...]],
) -> dict[str, Any]:
    raw_lookup = {entity.id: entity for entity in raw_entities}
    name_to_contract = {entity.canonical_name: entity for entity in canonical_entities}
    counts: dict[str, dict[str, Any]] = {}

    for contract in canonical_entities:
        source_ids = set(contract.extensions.get("source_entity_ids", (contract.entity_id,)))
        linked_raw_ids = {
            linked_id
            for source_id in source_ids
            for linked_id in neighbours.get(source_id, ())
            if linked_id not in source_ids and linked_id in raw_lookup
        }
        linked_titles: dict[str, set[str]] = {}
        for linked_id in linked_raw_ids:
            entity = raw_lookup[linked_id]
            linked_titles.setdefault(entity.type, set()).add(entity.title)
        counts[contract.entity_id] = {
            "total": len(linked_raw_ids),
            "titles_by_type": {
                entity_type: tuple(sorted(values))
                for entity_type, values in sorted(linked_titles.items())
            },
        }

    return {
        "counts": counts,
        "name_to_contract": name_to_contract,
        "supplier_like": {
            contract.entity_id: any(
                any(token in f"{raw_lookup[source_id].path} {raw_lookup[source_id].title} {getattr(raw_lookup[source_id], 'source_text', '')}".lower() for token in ("supplier", "vendor"))
                for source_id in contract.extensions.get("source_entity_ids", (contract.entity_id,))
                if source_id in raw_lookup
            )
            for contract in canonical_entities
        },
    }


def _project_objectives(
    canonical_entities: tuple[CanonicalExecutiveEntityContract, ...],
    context: dict[str, Any],
) -> tuple[ObjectiveInsight, ...]:
    projected = []
    for contract in canonical_entities:
        if contract.entity_type != "objective":
            continue
        linked = context["counts"].get(contract.entity_id, {}).get("total", 0)
        status = contract.status or _project_status_from_links(linked)
        projected.append(
            ObjectiveInsight(
                title=contract.canonical_name,
                path=contract.primary_path,
                linked_entities=linked,
                status=status,
                recommendation=_objective_recommendation(status),
            )
        )
    return tuple(sorted(projected, key=_title_key))


def _project_projects(
    canonical_entities: tuple[CanonicalExecutiveEntityContract, ...],
    context: dict[str, Any],
) -> tuple[ProjectInsight, ...]:
    projected = []
    for contract in canonical_entities:
        if contract.entity_type != "project":
            continue
        linked = context["counts"].get(contract.entity_id, {}).get("total", 0)
        status = contract.status or _project_status_from_links(linked)
        projected.append(
            ProjectInsight(
                title=contract.canonical_name,
                path=contract.primary_path,
                linked_entities=linked,
                status=status,
                recommendation=_project_recommendation(status),
            )
        )
    return tuple(sorted(projected, key=_title_key))


def _project_companies(
    canonical_entities: tuple[CanonicalExecutiveEntityContract, ...],
    context: dict[str, Any],
) -> tuple[CompanyInsight, ...]:
    projected = []
    for contract in canonical_entities:
        if contract.entity_type != "company":
            continue
        titles_by_type = context["counts"].get(contract.entity_id, {}).get("titles_by_type", {})
        people = len(titles_by_type.get("person", ()))
        projects = len(titles_by_type.get("project", ()))
        objectives = len(titles_by_type.get("objective", ()))
        links = context["counts"].get(contract.entity_id, {}).get("total", 0)
        score = links + (projects * 5) + (objectives * 10) + (people * 2)
        status = contract.status or _company_status_from_score(score)
        is_supplier = context.get("supplier_like", {}).get(contract.entity_id, False)
        projected.append(
            CompanyInsight(
                title=contract.canonical_name,
                path=contract.primary_path,
                links=links,
                people=people,
                projects=projects,
                objectives=objectives,
                score=score,
                status=status,
                is_supplier=is_supplier,
            )
        )
    return tuple(sorted(projected, key=lambda item: (-item.score, item.title.lower(), item.path)))


def _project_people(
    canonical_entities: tuple[CanonicalExecutiveEntityContract, ...],
    context: dict[str, Any],
) -> tuple[PersonInsight, ...]:
    projected = []
    for contract in canonical_entities:
        if contract.entity_type != "person":
            continue
        titles_by_type = context["counts"].get(contract.entity_id, {}).get("titles_by_type", {})
        projects = len(titles_by_type.get("project", ()))
        companies = len(titles_by_type.get("company", ()))
        objectives = len(titles_by_type.get("objective", ()))
        decisions = len(titles_by_type.get("decision", ()))
        total_links = context["counts"].get(contract.entity_id, {}).get("total", 0)
        influence = projects * 20 + companies * 10 + objectives * 40 + decisions * 15 + total_links
        risk = contract.risk_level or _person_risk_from_influence(influence)
        projected.append(
            PersonInsight(
                title=contract.canonical_name,
                path=contract.primary_path,
                projects=projects,
                companies=companies,
                objectives=objectives,
                decisions=decisions,
                total_links=total_links,
                influence=influence,
                risk=risk,
            )
        )
    return tuple(sorted(projected, key=lambda item: (-item.influence, item.title.lower(), item.path)))


def _project_decisions(
    canonical_entities: tuple[CanonicalExecutiveEntityContract, ...],
    context: dict[str, Any],
) -> tuple[dict[str, Any], ...]:
    projected = []
    for contract in canonical_entities:
        if contract.entity_type != "decision":
            continue
        titles_by_type = context["counts"].get(contract.entity_id, {}).get("titles_by_type", {})
        projects = len(titles_by_type.get("project", ()))
        objectives = len(titles_by_type.get("objective", ()))
        companies = len(titles_by_type.get("company", ()))
        people = len(titles_by_type.get("person", ()))
        importance = objectives * 100 + projects * 40 + companies * 20 + people * 10 + context["counts"].get(contract.entity_id, {}).get("total", 0)
        projected.append(
            {
                "title": contract.canonical_name,
                "projects": projects,
                "objectives": objectives,
                "companies": companies,
                "people": people,
                "importance": importance,
                "path": contract.primary_path,
                "owner": contract.owner,
                "confidence": contract.confidence,
                "evidence_paths": list(contract.evidence_paths),
            }
        )
    projected.sort(key=lambda item: (-item["importance"], item["title"].lower()))
    return tuple(projected)


def _project_status_from_links(linked: int) -> str:
    if linked == 0:
        return "AT RISK"
    if linked < 3:
        return "WATCH"
    return "SUPPORTED"


def _project_recommendation(status: str) -> str:
    if status == "AT RISK":
        return "Project has no graph linkage; review whether it is current, duplicated, or missing relationships."
    if status == "WATCH":
        return "Project has limited supporting evidence; review owner, objective, decisions and dependencies."
    return "Project has supporting vault evidence."


def _objective_recommendation(status: str) -> str:
    if status == "AT RISK":
        return "Review objective linkage; no supporting projects, decisions, people or evidence are connected."
    if status == "WATCH":
        return "Objective has limited supporting evidence; review whether it is actively managed."
    return "Objective has supporting vault evidence."


def _company_status_from_score(score: int) -> str:
    if score >= 30:
        return "CRITICAL"
    if score >= 15:
        return "IMPORTANT"
    if score >= 5:
        return "ACTIVE"
    return "LOW"


def _person_risk_from_influence(influence: int) -> str:
    if influence >= 500:
        return "CRITICAL"
    if influence >= 250:
        return "HIGH"
    if influence >= 100:
        return "MEDIUM"
    return "LOW"


def _render_bullets(values: tuple[str, ...] | list[str]) -> list[str]:
    rendered = [f"- {value}" for value in values if value]
    return rendered or ["_None found._"]
