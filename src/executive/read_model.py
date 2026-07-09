"""Unified executive read-model adapter for downstream consumers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from executive.knowledge.entity_contract import CanonicalExecutiveEntityContract
from src.executive.work_item_contract import ExecutiveWorkItemContract

if TYPE_CHECKING:
    from src.executive.executive_state import ExecutiveState
    from src.followups.followup_intelligence import FollowupIntelligence
    from src.openloops.open_loop_intelligence import OpenLoopIntelligence
    from src.meeting.meeting_intelligence import MeetingBrief
    from src.knowledge.knowledge_graph import KnowledgeGraphModel


@dataclass(frozen=True)
class ExecutiveReadModelEvidenceSummary:
    subject_id: str
    subject_type: str
    title: str
    evidence_paths: tuple[str, ...]
    evidence_count: int
    provenance: dict[str, tuple[str, ...]]
    confidence: str
    last_verified: str | None


@dataclass(frozen=True)
class ExecutiveReadModelCompatibility:
    objectives: tuple[Any, ...]
    projects: tuple[Any, ...]
    companies: tuple[Any, ...]
    people: tuple[Any, ...]
    meetings: tuple["MeetingBrief", ...]
    decisions: tuple[dict[str, Any], ...]
    followups: "FollowupIntelligence"
    open_loops: "OpenLoopIntelligence"
    suppliers: tuple[Any, ...]


@dataclass(frozen=True)
class UnifiedExecutiveReadModel:
    entities: tuple[CanonicalExecutiveEntityContract, ...]
    work_items: tuple[ExecutiveWorkItemContract, ...]
    actions: tuple[str, ...]
    relationships: "KnowledgeGraphModel | None"
    evidence_summaries: dict[str, ExecutiveReadModelEvidenceSummary]
    recency_signals: dict[str, str | None]
    priority_signals: dict[str, str | None]
    risk_signals: dict[str, str | None]
    priorities: tuple[dict[str, Any], ...]
    compatibility: ExecutiveReadModelCompatibility

    @property
    def meetings(self) -> tuple["MeetingBrief", ...]:
        return self.compatibility.meetings

    @property
    def followups(self) -> "FollowupIntelligence":
        return self.compatibility.followups

    @property
    def open_loops(self) -> "OpenLoopIntelligence":
        return self.compatibility.open_loops

    @property
    def projects(self) -> tuple[Any, ...]:
        return self.compatibility.projects

    @property
    def objectives(self) -> tuple[Any, ...]:
        return self.compatibility.objectives

    @property
    def companies(self) -> tuple[Any, ...]:
        return self.compatibility.companies

    @property
    def people(self) -> tuple[Any, ...]:
        return self.compatibility.people

    @property
    def decisions(self) -> tuple[dict[str, Any], ...]:
        return self.compatibility.decisions

    @property
    def suppliers(self) -> tuple[Any, ...]:
        return self.compatibility.suppliers


def build_unified_executive_read_model(state: "ExecutiveState") -> UnifiedExecutiveReadModel:
    evidence_summaries: dict[str, ExecutiveReadModelEvidenceSummary] = {}
    recency_signals: dict[str, str | None] = {}
    priority_signals: dict[str, str | None] = {}
    risk_signals: dict[str, str | None] = {}

    for entity in state.canonical_entities:
        evidence_summaries[entity.entity_id] = ExecutiveReadModelEvidenceSummary(
            subject_id=entity.entity_id,
            subject_type=entity.entity_type,
            title=entity.canonical_name,
            evidence_paths=entity.evidence_paths,
            evidence_count=entity.evidence_count,
            provenance=dict(entity.provenance),
            confidence=entity.confidence,
            last_verified=entity.last_verified,
        )
        recency_signals[entity.entity_id] = entity.due_date or entity.last_activity or entity.review_date
        priority_signals[entity.entity_id] = entity.priority
        risk_signals[entity.entity_id] = entity.risk_level

    for item in state.work_items:
        evidence_summaries[item.work_item_id] = ExecutiveReadModelEvidenceSummary(
            subject_id=item.work_item_id,
            subject_type=item.work_item_type,
            title=item.title,
            evidence_paths=item.evidence_paths,
            evidence_count=item.evidence_count,
            provenance=dict(item.provenance),
            confidence=item.confidence,
            last_verified=item.last_verified,
        )
        recency_signals[item.work_item_id] = item.due_date or item.last_activity
        priority_signals[item.work_item_id] = item.priority
        risk_signals[item.work_item_id] = item.risk_level

    return UnifiedExecutiveReadModel(
        entities=state.canonical_entities,
        work_items=state.work_items,
        actions=tuple(state.recommendations),
        relationships=state.relationship_graph,
        evidence_summaries=evidence_summaries,
        recency_signals=recency_signals,
        priority_signals=priority_signals,
        risk_signals=risk_signals,
        priorities=state.priorities,
        compatibility=ExecutiveReadModelCompatibility(
            objectives=state.objectives,
            projects=state.projects,
            companies=state.companies,
            people=state.people,
            meetings=state.meetings,
            decisions=state.decisions,
            followups=state.followups,
            open_loops=state.open_loops,
            suppliers=state.suppliers,
        ),
    )
