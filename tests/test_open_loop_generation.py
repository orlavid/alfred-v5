from pathlib import Path
import subprocess
import sys

from src.openloops import open_loop_intelligence as open_loop_module
from src.openloops.open_loop_intelligence import SECTION_HEADINGS, build_open_loop_intelligence


def test_build_open_loops_generates_report():
    output = Path("output/Open_Loop_Intelligence.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_open_loops.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Open Loop Intelligence" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content


def test_open_loops_prefer_daily_governance_index_records(tmp_path, monkeypatch):
    index = tmp_path / "daily_governance_index.json"
    index.write_text(
        """{
  "records": [
    {
      "id": "DG-20260710-OPEN_LOOP-1",
      "date": "2026-07-10",
      "type": "open_loop",
      "text": "Awaiting a formal recovery plan from Decision Focus that restores confidence in delivery against the agreed end-of-July target.",
      "status": "open",
      "source": "/docker/obsidian-vault/01 Daily Logs/2026-07-10.md"
    },
    {
      "id": "DG-20260709-OPEN_LOOP-2",
      "date": "2026-07-09",
      "type": "open_loop",
      "text": "What was on my follow up and open loops today",
      "status": "open",
      "source": "/docker/obsidian-vault/01 Daily Logs/2026-07-09.md"
    }
  ]
}"""
    )
    monkeypatch.setattr(open_loop_module, "DAILY_GOVERNANCE_INDEX", index)

    report = build_open_loop_intelligence(vault_root=tmp_path / "missing-vault")

    assert report.open_loop_count == 1
    assert report.critical_open_loops
    assert report.critical_open_loops[0].path == "01 Daily Logs/2026-07-10.md"
    assert "What was on my follow up and open loops today" not in [item.summary for item in report.critical_open_loops]
