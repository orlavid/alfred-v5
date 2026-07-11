from pathlib import Path
from datetime import date
import subprocess
import sys

from src.followups import followup_intelligence as followup_module
from src.followups.followup_intelligence import SECTION_HEADINGS, build_followup_intelligence


def test_build_followups_generates_report():
    output = Path("output/Followup_Intelligence.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_followups.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Follow-up Intelligence" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content


def test_followups_prefer_daily_governance_index_records(tmp_path, monkeypatch):
    index = tmp_path / "daily_governance_index.json"
    index.write_text(
        """{
  "records": [
    {
      "id": "DG-20260710-FOLLOW_UP_ACTION-1",
      "date": "2026-07-10",
      "type": "follow_up_action",
      "text": "Review and respond to Decision Focus once their revised remediation plan is received.",
      "status": "open",
      "source": "/docker/obsidian-vault/01 Daily Logs/2026-07-10.md"
    },
    {
      "id": "DG-20260709-FOLLOW_UP_ACTION-2",
      "date": "2026-07-09",
      "type": "follow_up_action",
      "text": "Complete any required Procurement KPI input ahead of the Mancom material deadline of 13 July.",
      "status": "open",
      "source": "/docker/obsidian-vault/01 Daily Logs/2026-07-09.md"
    }
  ]
}"""
    )
    monkeypatch.setattr(followup_module, "DAILY_GOVERNANCE_INDEX", index)

    report = build_followup_intelligence(vault_root=tmp_path / "missing-vault", today=date(2026, 7, 14))

    assert report.followup_count == 2
    assert any(item.path == "01 Daily Logs/2026-07-09.md" for item in report.high_priority)
    assert report.executive_summary[0].startswith("Analysed 2 inferred follow-ups")
