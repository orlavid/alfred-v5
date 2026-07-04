from pathlib import Path
import subprocess
import sys

from src.pipeline import executive_pipeline
from src.pipeline.executive_pipeline import build_executive_pipeline


def test_build_executive_pipeline_runs_all_stages(tmp_path):
    report = build_executive_pipeline(
        Path("evidence/alfred-inventory"),
        refresh_state_path=tmp_path / "refresh.json",
    )

    assert len(report.stages) == 8
    assert report.stages[0].stage == "Vault Scan"
    assert report.stages[-1].stage == "Dashboard API Refresh"
    assert report.overall_health in {"GREEN", "AMBER", "RED"}
    assert any(stage.stage == "ExecutiveState" and stage.status == "PASS" for stage in report.stages)
    assert any(stage.stage == "Daily Brief" and stage.status == "PASS" for stage in report.stages)


def test_pipeline_continues_after_recoverable_entity_resolution_failure(monkeypatch, tmp_path):
    def broken_resolution(_entities):
        raise RuntimeError("resolution failed")

    monkeypatch.setattr(executive_pipeline, "build_entity_resolution", broken_resolution)

    report = build_executive_pipeline(
        Path("evidence/alfred-inventory"),
        refresh_state_path=tmp_path / "refresh.json",
    )
    stages = {stage.stage: stage for stage in report.stages}

    assert stages["Entity Resolution"].status == "FAIL"
    assert stages["Executive Knowledge Builder"].status == "PASS"


def test_build_executive_pipeline_generates_report():
    output = Path("output/Executive_Pipeline_Report.md")
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [sys.executable, "build_executive_pipeline.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output.exists()

    content = output.read_text()
    assert "# Executive Pipeline" in content
    assert "| Stage | Status | Duration | Records Processed | Warnings | Errors |" in content
    assert "## Summary" in content
    assert "## Overall Health" in content
