from pathlib import Path
import json
import subprocess
import sys

from src.knowledge.executive_knowledge_builder import ExecutiveKnowledgeModel, KnowledgeEntity, KnowledgeRelationship
from src.knowledge.knowledge_graph import build_knowledge_graph_from_model


def test_build_knowledge_graph_from_model_uses_canonical_nodes():
    model = ExecutiveKnowledgeModel(
        source_mode="evidence_inventory",
        source_root="evidence/alfred-inventory",
        entity_inventory={"objective": 1, "project": 1},
        entities=(
            KnowledgeEntity(
                id="03 Projects/Project A.md",
                entity_type="project",
                title="Project A",
                path="03 Projects/Project A.md",
                source_reference="03 Projects/Project A.md",
                confidence="HIGH",
                relationships=("09 Governance/Objectives/Objective A.md",),
                orphan=False,
                stale_evidence=False,
                last_evidence_date=None,
            ),
            KnowledgeEntity(
                id="09 Governance/Objectives/Objective A.md",
                entity_type="objective",
                title="Objective A",
                path="09 Governance/Objectives/Objective A.md",
                source_reference="09 Governance/Objectives/Objective A.md",
                confidence="HIGH",
                relationships=("03 Projects/Project A.md",),
                orphan=False,
                stale_evidence=False,
                last_evidence_date=None,
            ),
        ),
        raw_entities=(),
        canonical_entities=(
            {
                "canonical_id": "03 Projects/Project A.md",
                "canonical_name": "Project A",
                "entity_type": "project",
                "source_path": "03 Projects/Project A.md",
                "aliases": ["Project A"],
                "confidence": "LOW",
            },
            {
                "canonical_id": "09 Governance/Objectives/Objective A.md",
                "canonical_name": "Objective A",
                "entity_type": "objective",
                "source_path": "09 Governance/Objectives/Objective A.md",
                "aliases": ["Objective A"],
                "confidence": "LOW",
            },
        ),
        aliases=(),
        relationship_graph=(
            KnowledgeRelationship(
                source="03 Projects/Project A.md",
                target="09 Governance/Objectives/Objective A.md",
                relationship_type="links_to",
            ),
        ),
        orphans=(),
        stale_evidence=(),
        executive_summary=[],
        recommended_actions=[],
    )

    report = build_knowledge_graph_from_model(model)

    assert len(report.nodes) == 2
    assert any(edge.relationship_type == "SUPPORTS" for edge in report.edges)
    assert report.statistics["node_counts"]["Objective"] == 1
    assert report.statistics["relationship_counts"]["SUPPORTS"] == 1


def test_build_knowledge_graph_generates_outputs():
    markdown_output = Path("output/Knowledge_Graph.md")
    json_output = Path("output/Knowledge_Graph.json")
    if markdown_output.exists():
        markdown_output.unlink()
    if json_output.exists():
        json_output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_knowledge_graph.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert markdown_output.exists()
    assert json_output.exists()

    content = markdown_output.read_text()
    assert "# Knowledge Graph" in content
    assert "## Node Counts" in content
    payload = json.loads(json_output.read_text())
    assert "nodes" in payload
    assert "edges" in payload
    assert "statistics" in payload
