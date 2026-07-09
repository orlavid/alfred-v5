from executive.intelligence.prioritisation import build_priorities
from executive.knowledge.entity import VaultEntity
from executive.knowledge.entity_quality import build_executive_entity_quality
from executive.knowledge.resolver import build_entity_resolution
from src.executive.executive_intelligence import ExecutiveIntelligence, ExecutiveLineItem
from src.executive.executive_reasoning import _build_actions
from src.followups.followup_intelligence import FollowupIntelligence
from src.openloops.open_loop_intelligence import OpenLoopIntelligence


def test_entity_contract_stable_ids_survive_rebuilds_and_aliases_resolve():
    entities = [
        VaultEntity(
            id="04 Companies/Microsoft.md",
            type="company",
            title="Microsoft",
            path="04 Companies/Microsoft.md",
            aliases=["MSFT"],
            source_text="Status: IMPORTANT\nOwner: Jane Smith\n",
        ),
        VaultEntity(
            id="04 Companies/MSFT.md",
            type="company",
            title="MSFT",
            path="04 Companies/MSFT.md",
        ),
    ]
    resolution = build_entity_resolution(entities)

    first = build_executive_entity_quality(entities, resolution)
    second = build_executive_entity_quality(list(reversed(entities)), resolution)

    assert len(first.canonical_entities) == 1
    assert len(second.canonical_entities) == 1
    assert first.canonical_entities[0].entity_id == second.canonical_entities[0].entity_id
    assert first.canonical_entities[0].canonical_name == "Microsoft"
    assert "MSFT" in first.canonical_entities[0].aliases


def test_entity_contract_preserves_known_metadata_and_provenance():
    entities = [
        VaultEntity(
            id="03 Projects/Cash Management.md",
            type="project",
            title="Cash Management",
            path="03 Projects/Cash Management.md",
            links=["Treasury Objective", "Jane Smith"],
            source_text=(
                "Owner: Jane Smith\n"
                "Status: AT RISK\n"
                "Priority: HIGH\n"
                "Due: 2026-07-15\n"
                "Review Date: 2026-07-20\n"
                "Created: 2026-07-01\n"
                "Last Activity: 2026-07-14\n"
            ),
        ),
        VaultEntity(
            id="09 Objectives/Treasury Objective.md",
            type="objective",
            title="Treasury Objective",
            path="09 Objectives/Treasury Objective.md",
        ),
        VaultEntity(
            id="02 People/Jane Smith.md",
            type="person",
            title="Jane Smith",
            path="02 People/Jane Smith.md",
        ),
    ]
    graph = {
        "edges": [
            {"source": "03 Projects/Cash Management.md", "target": "09 Objectives/Treasury Objective.md"},
            {"source": "03 Projects/Cash Management.md", "target": "02 People/Jane Smith.md"},
        ]
    }
    resolution = build_entity_resolution(entities)
    quality = build_executive_entity_quality(
        entities,
        resolution,
        graph=graph,
        project_analysis={
            "insights": [
                type("ProjectInsight", (), {
                    "title": "Cash Management",
                    "path": "03 Projects/Cash Management.md",
                    "status": "AT RISK",
                    "recommendation": "Review project governance and linkage",
                })()
            ]
        },
        people_analysis={
            "insights": [
                type("PersonInsight", (), {
                    "title": "Jane Smith",
                    "path": "02 People/Jane Smith.md",
                    "risk": "LOW",
                })()
            ]
        },
        ownership={
            "projects": [
                {
                    "project": "Cash Management",
                    "owner": "Jane Smith",
                    "confidence": 1.0,
                    "source": "graph",
                }
            ]
        },
    )

    contract = next(item for item in quality.canonical_entities if item.canonical_name == "Cash Management")
    assert contract.owner == "Jane Smith"
    assert contract.status == "AT RISK"
    assert contract.priority == "HIGH"
    assert contract.due_date == "2026-07-15"
    assert contract.review_date == "2026-07-20"
    assert contract.created == "2026-07-01"
    assert contract.last_activity == "2026-07-14"
    assert contract.related_objectives == ("Treasury Objective",)
    assert contract.related_people == ("Jane Smith",)
    assert contract.provenance["owner"] == ("03 Projects/Cash Management.md",)
    assert contract.provenance["due_date"] == ("03 Projects/Cash Management.md",)
    assert contract.evidence_paths == ("03 Projects/Cash Management.md",)


def test_entity_contract_marks_unknown_metadata_explicitly():
    entities = [
        VaultEntity(
            id="03 Projects/Operations Refresh.md",
            type="project",
            title="Operations Refresh",
            path="03 Projects/Operations Refresh.md",
            source_text="No structured metadata here.\n",
        )
    ]
    resolution = build_entity_resolution(entities)
    quality = build_executive_entity_quality(entities, resolution)

    contract = next(item for item in quality.canonical_entities if item.canonical_name == "Operations Refresh")
    assert contract.owner is None
    assert contract.due_date is None
    assert "owner" in contract.missing_fields
    assert "due_date" in contract.missing_fields
    assert "status" in contract.missing_fields


def test_prioritisation_and_reasoning_continue_to_consume_contract():
    entities = [
        VaultEntity(
            id="03 Projects/Cash Management.md",
            type="project",
            title="Cash Management",
            path="03 Projects/Cash Management.md",
            source_text="Owner: Jane Smith\nStatus: AT RISK\nDue: 2026-07-15\n",
        ),
        VaultEntity(
            id="09 Objectives/Treasury Objective.md",
            type="objective",
            title="Treasury Objective",
            path="09 Objectives/Treasury Objective.md",
        ),
        VaultEntity(
            id="02 People/Jane Smith.md",
            type="person",
            title="Jane Smith",
            path="02 People/Jane Smith.md",
        ),
    ]
    graph = {
        "edges": [
            {"source": "03 Projects/Cash Management.md", "target": "09 Objectives/Treasury Objective.md"},
            {"source": "03 Projects/Cash Management.md", "target": "02 People/Jane Smith.md"},
        ],
        "entities_by_type": {"project": 1, "objective": 1, "person": 1},
    }
    vault = {
        "impact": [{"title": "Cash Management", "impact": 900}],
        "dependency_analysis": {"top_dependencies": []},
        "risk": {"all": [{"title": "Cash Management", "risk_score": 75, "reasons": ["Weak graph connectivity"]}]},
        "ownership": {"projects": [{"project": "Cash Management", "owner": "Jane Smith", "confidence": 1.0}]},
        "projects": {"insights": [type("ProjectInsight", (), {"title": "Cash Management", "status": "AT RISK"})()]},
        "companies": {"insights": []},
        "people": {"insights": []},
        "decisions": {"top_decisions": []},
    }
    resolution = build_entity_resolution(entities)
    quality = build_executive_entity_quality(
        entities,
        resolution,
        graph=graph,
        project_analysis={"insights": [type("ProjectInsight", (), {"title": "Cash Management", "path": "03 Projects/Cash Management.md", "status": "AT RISK", "recommendation": "Review project governance and linkage"})()]},
        ownership={"projects": [{"project": "Cash Management", "owner": "Jane Smith", "confidence": 1.0}]},
        risk_analysis={"all": [{"title": "Cash Management", "risk_score": 75, "reasons": ["Weak graph connectivity"]}]},
    )

    priorities = build_priorities(vault, entities, graph, canonical_entities=quality.canonical_entities)["top_priorities"]
    priority = priorities[0]

    assert priority["owner"] == "Jane Smith"
    assert priority["status"] == "AT RISK"
    assert priority["deadline_or_recency"] == "2026-07-15"
    assert priority["evidence_paths"] == ["03 Projects/Cash Management.md"]

    intelligence = ExecutiveIntelligence(
        executive_health=[],
        top_priorities=[
            ExecutiveLineItem(
                priority["title"],
                f"{priority['priority']} score {priority['priority_score']}. {priority['next_step']}",
                context=dict(priority),
            )
        ],
        objectives_requiring_attention=[],
        critical_meetings=[],
        projects_at_risk=[],
        followups_requiring_action=[],
        open_loops=[],
        key_people=[],
        supplier_risks=[],
        decisions_awaiting_attention=[],
        recommended_actions_today=[],
        executive_summary=[],
    )
    followups = FollowupIntelligence(
        generated_at="2026-07-07T00:00:00+00:00",
        followup_count=0,
        overdue=[],
        due_today=[],
        due_this_week=[],
        waiting_on_others=[],
        high_priority=[],
        recommendations=[],
        executive_summary=[],
    )
    open_loops = OpenLoopIntelligence(
        generated_at="2026-07-07T00:00:00+00:00",
        open_loop_count=0,
        critical_open_loops=[],
        waiting_for=[],
        stalled_projects=[],
        missing_decisions=[],
        missing_owners=[],
        recommended_actions=[],
        executive_summary=[],
    )

    actions = _build_actions(intelligence, None, followups, open_loops)

    assert len(actions) == 1
    assert "Jane Smith" in actions[0].action
    assert "2026-07-15" in actions[0].action
    assert "03 Projects/Cash Management.md" in actions[0].supporting_evidence
