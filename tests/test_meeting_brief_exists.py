from pathlib import Path

def test_meeting_builder_exists():
    assert Path("build_meeting_brief.py").exists()

def test_meeting_module_exists():
    assert Path("src/meeting/meeting_intelligence.py").exists()
