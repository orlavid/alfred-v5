from pathlib import Path

from src.meeting.meeting_intelligence import MeetingIntelligence


def test_meeting_intelligence_finds_matching_evidence(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    (evidence / "barclays.md").write_text(
        "Barclays meeting evidence. Follow up on virtual cards and AP analysis."
    )

    brief = MeetingIntelligence(evidence).build("Barclays")

    assert brief.hits
    assert brief.hits[0].path == "barclays.md"
    assert "Barclays" in brief.query


def test_meeting_intelligence_handles_no_evidence(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    evidence.mkdir()

    brief = MeetingIntelligence(evidence).build("No Such Meeting")

    assert not brief.hits
    assert "No evidence found" in brief.risks[0]


def test_meeting_intelligence_renders_markdown(tmp_path: Path) -> None:
    evidence = tmp_path / "evidence"
    evidence.mkdir()
    (evidence / "note.md").write_text("Graham Dawe and Barclays discussion.")

