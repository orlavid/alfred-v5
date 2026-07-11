from pathlib import Path

from src.operations.semantic_equivalence_validation import build_semantic_equivalence_validation


def test_semantic_equivalence_validation_passes_for_legacy_style_objectives(tmp_path: Path):
    vault = _build_vault(tmp_path / "vault")

    report = build_semantic_equivalence_validation(
        evidence_root=Path("evidence/alfred-inventory"),
        vault_root=vault,
    )

    assert report.overall_status == "PASS"
    assert report.mode == "live_vault"
    assert report.objectives.legacy_count == 6
    assert report.objectives.new_count == 6
    assert report.objectives.matched == (
        "Cost Management",
        "Data and AI Strategies",
        "Employee Development",
        "Operational Governance",
        "Performance and Value Realisation",
        "Risk Management",
    )
    assert report.objectives.missing == ()
    assert report.objectives.false_positives == ()
    assert report.objectives.false_negatives == ()
    assert report.objectives.current_heuristic_count == 4
    assert "2026-05-28 Open Loop - platform_resilience" in report.objectives.current_heuristic_false_positives
    assert "2026-05-29 Watchlist - strategic_drift" in report.objectives.current_heuristic_false_positives
    assert "Strategic Memory Synthesis" in report.objectives.current_heuristic_false_positives
    assert all(".md#objective-" in path for path in report.objectives.source_notes_used)


def test_semantic_equivalence_validation_falls_back_to_representative_fixture_when_vault_missing(tmp_path: Path):
    report = build_semantic_equivalence_validation(
        evidence_root=Path("evidence/alfred-inventory"),
        vault_root=tmp_path / "missing-vault",
    )

    assert report.overall_status == "PASS"
    assert report.mode == "representative_fixture"
    assert report.objectives.legacy_count == 6
    assert report.objectives.false_positives == ()


def _build_vault(vault: Path) -> Path:
    for folder in (
        "01 Daily Logs",
        "02 People",
        "03 Projects",
        "04 Companies",
        "04 Decisions",
        "05 Meetings",
        "06 Risks",
        "07 Open Loops",
        "08 Follow Ups",
        "09 Objectives",
        "10 Briefings",
    ):
        (vault / folder).mkdir(parents=True)
    (vault / "09 Governance" / "Watchlists").mkdir(parents=True)
    (vault / "07 AI Memory" / "Strategic Synthesis").mkdir(parents=True)
    (vault / "09 Governance" / "Objectives").mkdir(parents=True)

    (vault / "09 Governance" / "Objectives" / "2026 Executive Objectives.md").write_text(
        "# 2026 Executive Objectives\n\n"
        "## Objectives\n\n"
        "1. Operational Governance\n"
        "2. Data and AI Strategies\n"
        "3. Risk Management\n"
        "4. Employee Development\n"
        "5. Cost Management\n"
        "6. Performance and Value Realisation\n"
    )
    (vault / "09 Governance" / "Objectives" / "2026-05-28 Open Loop - platform_resilience.md").write_text(
        "# 2026-05-28 Open Loop - platform_resilience\nObjective: unblock platform resilience work.\n"
    )
    (vault / "09 Governance" / "Watchlists" / "2026-05-29 Watchlist - strategic_drift.md").write_text(
        "# 2026-05-29 Watchlist - strategic_drift\nObjective: monitor strategic drift.\n"
    )
    (vault / "07 AI Memory" / "Strategic Synthesis" / "Strategic Memory Synthesis.md").write_text(
        "# Strategic Memory Synthesis\nObjective: summarise the historical record.\n"
    )
    (vault / "03 Projects" / "Project Phoenix.md").write_text("# Project Phoenix\nOperational governance programme.\n")
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\nOwner.\n")
    (vault / "04 Companies" / "Acme Capital.md").write_text("# Acme Capital\nSupplier.\n")
    (vault / "04 Decisions" / "Decision 1.md").write_text("# Decision 1\nApprove.\n")
    (vault / "05 Meetings" / "Project Phoenix Review.md").write_text("# Project Phoenix Review\nAgenda.\n")
    (vault / "06 Risks" / "Risk Register.md").write_text("# Risk Register\nEscalation.\n")
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text(
        "## LOOP-1\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\nIssue: Await approval.\n"
    )
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text(
        "## Follow-Up Actions\n- Follow up with Acme Capital today.\n"
    )
    (vault / "01 Daily Logs" / "2026-07-04 Daily.md").write_text(
        "# 2026-07-04 Daily\nReviewed [[Project Phoenix]].\n"
    )
    return vault
