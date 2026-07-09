from executive.intelligence.prioritisation import build_priorities
from executive.knowledge.entity import VaultEntity
from executive.knowledge.entity_quality import build_executive_entity_quality
from executive.knowledge.resolver import build_entity_resolution


def test_entity_quality_rejects_low_information_entities():
    entities = [
        VaultEntity(id="year", type="project", title="2026", path="03 Projects/2026.md"),
        VaultEntity(
            id="historical",
            type="project",
            title="Historical Capture - Signing Authorities - 20260526-141436",
            path="00 Inbox/Captures/Historical Capture - Signing Authorities - 20260526-141436.md",
        ),
        VaultEntity(
            id="capture",
            type="project",
            title="Capture - Legacy Notes",
            path="00 Inbox/Captures/Capture - Legacy Notes.md",
        ),
        VaultEntity(
            id="memory",
            type="project",
            title="po-consilio",
            path="07 AI Memory/Entities/po-consilio.md",
        ),
        VaultEntity(
            id="weak-file",
            type="project",
            title="tmp-import-042",
            path="03 Projects/tmp-import-042.md",
        ),
        VaultEntity(
            id="objective",
            type="objective",
            title="Treasury Operating Model",
            path="09 Objectives/Treasury Operating Model.md",
            aliases=["TOM"],
        ),
        VaultEntity(
            id="project",
            type="project",
            title="Cash Management",
            path="03 Projects/Cash Management.md",
        ),
        VaultEntity(
            id="decision",
            type="decision",
            title="Approve Barclays Mandate",
            path="04 Decisions/Approve Barclays Mandate.md",
        ),
    ]

    quality = build_executive_entity_quality(entities, build_entity_resolution(entities))

    canonical_titles = {entity.title for entity in quality.canonical_entities}
    rejected_titles = {entity.title for entity in quality.rejected_entities}

    assert canonical_titles == {
        "Treasury Operating Model",
        "Cash Management",
        "Approve Barclays Mandate",
    }
    assert rejected_titles == {
        "2026",
        "Historical Capture - Signing Authorities - 20260526-141436",
        "Capture - Legacy Notes",
        "po-consilio",
        "tmp-import-042",
    }


def test_entity_quality_merges_aliases_into_canonical_entity():
    entities = [
        VaultEntity(
            id="microsoft",
            type="company",
            title="Microsoft",
            path="04 Companies/Microsoft.md",
            aliases=["MSFT"],
        ),
        VaultEntity(
            id="msft",
            type="company",
            title="MSFT",
            path="04 Companies/MSFT.md",
        ),
    ]

    quality = build_executive_entity_quality(entities, build_entity_resolution(entities))

    assert len(quality.canonical_entities) == 1
    canonical = quality.canonical_entities[0]
    assert canonical.title == "Microsoft"
    assert "MSFT" in canonical.aliases
    assert canonical.evidence_paths == ("04 Companies/MSFT.md", "04 Companies/Microsoft.md")


def test_priorities_only_consume_canonical_executive_entities():
    entities = [
        VaultEntity(id="year", type="project", title="2026", path="03 Projects/2026.md"),
        VaultEntity(
            id="historical",
            type="project",
            title="Historical Capture - Signing Authorities - 20260526-141436",
            path="00 Inbox/Captures/Historical Capture - Signing Authorities - 20260526-141436.md",
        ),
        VaultEntity(
            id="memory",
            type="project",
            title="po-consilio",
            path="07 AI Memory/Entities/po-consilio.md",
        ),
        VaultEntity(
            id="weak-file",
            type="project",
            title="tmp-import-042",
            path="03 Projects/tmp-import-042.md",
        ),
        VaultEntity(
            id="project",
            type="project",
            title="Cash Management",
            path="03 Projects/Cash Management.md",
        ),
    ]
    graph = {"edges": [], "entities_by_type": {"project": len(entities)}}
    vault = {
        "impact": [
            {"title": "2026", "impact": 2000},
            {"title": "Historical Capture - Signing Authorities - 20260526-141436", "impact": 1800},
            {"title": "po-consilio", "impact": 1600},
            {"title": "tmp-import-042", "impact": 1400},
            {"title": "Cash Management", "impact": 900},
        ],
        "dependency_analysis": {"top_dependencies": []},
        "risk": {
            "all": [
                {"title": "2026", "risk_score": 90, "reasons": ["Weak graph connectivity"]},
                {"title": "Historical Capture - Signing Authorities - 20260526-141436", "risk_score": 90, "reasons": ["Weak graph connectivity"]},
                {"title": "po-consilio", "risk_score": 90, "reasons": ["Weak graph connectivity"]},
                {"title": "tmp-import-042", "risk_score": 90, "reasons": ["Weak graph connectivity"]},
                {"title": "Cash Management", "risk_score": 75, "reasons": ["Weak graph connectivity"]},
            ]
        },
        "ownership": {
            "projects": [
                {"project": "2026", "owner": None, "confidence": 0.1},
                {"project": "Historical Capture - Signing Authorities - 20260526-141436", "owner": None, "confidence": 0.1},
                {"project": "po-consilio", "owner": None, "confidence": 0.1},
                {"project": "tmp-import-042", "owner": None, "confidence": 0.1},
                {"project": "Cash Management", "owner": None, "confidence": 0.1},
            ]
        },
        "projects": {
            "insights": [
                type("ProjectInsight", (), {"title": "2026", "status": "AT RISK"})(),
                type("ProjectInsight", (), {"title": "Historical Capture - Signing Authorities - 20260526-141436", "status": "AT RISK"})(),
                type("ProjectInsight", (), {"title": "po-consilio", "status": "AT RISK"})(),
                type("ProjectInsight", (), {"title": "tmp-import-042", "status": "AT RISK"})(),
                type("ProjectInsight", (), {"title": "Cash Management", "status": "AT RISK"})(),
            ]
        },
        "companies": {"insights": []},
        "people": {"insights": []},
        "decisions": {"top_decisions": []},
    }

    quality = build_executive_entity_quality(entities, build_entity_resolution(entities))
    priorities = build_priorities(
        vault,
        entities,
        graph,
        canonical_entities=quality.canonical_entities,
    )["top_priorities"]

    titles = [item["title"] for item in priorities]

    assert titles == ["Cash Management"]
    assert "2026" not in titles
    assert "Historical Capture - Signing Authorities - 20260526-141436" not in titles
    assert "po-consilio" not in titles
    assert "tmp-import-042" not in titles
