from datetime import date
from pathlib import Path
import subprocess
import sys

from src.curation.knowledge_curator import SECTION_HEADINGS, build_knowledge_housekeeping


def test_knowledge_curator_classifies_records_from_outputs(tmp_path: Path):
    output = tmp_path / "output"
    output.mkdir()

    (output / "Knowledge_Mining_Report.md").write_text(
        "\n".join(
            [
                "# Executive Knowledge Inventory",
                "",
                "## Projects",
                "",
                "- Project Atlas | Type: project | Source: legacy/projects/atlas.md | Confidence: HIGH | Import: IMPORT | ExecutiveState: projects",
                "",
                "## Recommended Imports",
                "",
                "- Project Atlas | Type: project | Source: legacy/projects/atlas.md | Confidence: HIGH | Import: IMPORT | ExecutiveState: projects",
                "",
                "## Discarded Technical Debt",
                "",
                "- legacy/logs/runtime.log",
            ]
        )
    )
    (output / "Executive_Intelligence.md").write_text(
        "\n".join(
            [
                "# Executive Intelligence",
                "",
                "## Projects At Risk",
                "",
                "- Project Atlas: AT RISK. Project has no graph linkage; review whether it is current, duplicated, or missing relationships.",
                "- Dormant Programme: WATCH. Last reviewed 2026-01-01 with limited supporting evidence.",
                "",
                "## Open Loops",
                "",
                "- Supplier Renewal: Waiting for supplier response. Status: OPEN; Owner: Unknown.",
                "",
                "## Supplier Risks",
                "",
                "- SoftCat: CRITICAL; links 255; projects 4; people 5.",
                "",
                "## Objectives Requiring Attention",
                "",
                "- Compliance Uplift: WATCH. Review whether supporting evidence is still complete.",
                "",
                "## Decisions Awaiting Attention",
                "",
                "- Financial Decision: Importance 34; projects 0; objectives 0.",
            ]
        )
    )
    (output / "Executive_Reasoning.md").write_text(
        "\n".join(
            [
                "# Executive Reasoning",
                "",
                "## Top 10 Executive Actions",
                "",
                "### Project Atlas",
                "- Priority: HIGH",
                "- Action: Review recovery path for project Atlas",
                "- Why it matters: Project has no graph linkage.",
                "",
                "## Recommended Agenda For Today",
                "",
                "- Review recovery path for project Atlas",
            ]
        )
    )

    report = build_knowledge_housekeeping(output, today=date(2026, 7, 3))

    assert any(record.title == "SoftCat" for record in report.active_records)
    assert any(record.title == "Dormant Programme" for record in report.dormant_records)
    assert any(record.title == "legacy/logs/runtime.log" for record in report.archived_candidates)
    assert any(record.title == "Supplier Renewal" for record in report.orphaned_records)
    assert any(record.title == "Project Atlas" for record in report.duplicate_candidates)
    assert any(record.title == "Compliance Uplift" for record in report.review_required)


def test_build_knowledge_housekeeping_generates_output():
    output = Path("output/Knowledge_Housekeeping_Report.md")
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [sys.executable, "build_knowledge_housekeeping.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output.exists()
    content = output.read_text()
    assert "# Knowledge Housekeeping" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
