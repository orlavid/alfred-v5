from pathlib import Path
import subprocess
import sys

from src.executive.executive_intelligence import ExecutiveIntelligence, ExecutiveLineItem
from src.executive.executive_reasoning import _build_actions
from src.followups.followup_intelligence import FollowupIntelligence
from src.openloops.open_loop_intelligence import OpenLoopIntelligence

from src.executive.executive_reasoning import SECTION_HEADINGS
from executive.intelligence.prioritisation import build_priorities
from executive.knowledge.entity import VaultEntity


def test_build_executive_reasoning_generates_report():
    output = Path("output/Executive_Reasoning.md")
    if output.exists():
        output.unlink()

    exit_code = subprocess.run(
        [sys.executable, "build_executive_reasoning.py"],
        check=False,
    ).returncode

    assert exit_code == 0
    assert output.exists()

    content = output.read_text()
    assert "# Executive Reasoning" in content
    for heading in SECTION_HEADINGS:
        assert f"## {heading}" in content
    assert "## Top 10 Executive Actions" in content
    assert "- Priority:" in content or "_None found._" in content
    assert "- Action:" in content or "_None found._" in content
    assert "- Why it matters:" in content
    assert "- Supporting evidence:" in content
    assert "- Expected impact:" in content
    assert "- Confidence:" in content


def test_priority_builder_demotes_historical_capture_artifacts():
    entities = [
        VaultEntity(
            id="capture-1",
            type="project",
            title="Historical Capture - Signing Authorities - 20260526-141436",
            path="00 Inbox/Captures/Historical Capture - Signing Authorities - 20260526-141436.md",
        ),
        VaultEntity(
            id="project-1",
            type="project",
            title="Cash Management",
            path="03 Projects/Cash Management.md",
        ),
    ]
    graph = {"edges": [], "entities_by_type": {"project": 2}}
    vault = {
        "impact": [
            {"title": "Historical Capture - Signing Authorities - 20260526-141436", "impact": 1000},
            {"title": "Cash Management", "impact": 900},
        ],
        "dependency_analysis": {"top_dependencies": []},
        "risk": {
            "all": [
                {"title": "Historical Capture - Signing Authorities - 20260526-141436", "risk_score": 80, "reasons": ["Weak graph connectivity"]},
                {"title": "Cash Management", "risk_score": 75, "reasons": ["Weak graph connectivity"]},
            ]
        },
        "ownership": {
            "projects": [
                {"project": "Historical Capture - Signing Authorities - 20260526-141436", "owner": None, "confidence": 0.1},
                {"project": "Cash Management", "owner": None, "confidence": 0.1},
            ]
        },
        "projects": {
            "insights": [
                type("ProjectInsight", (), {"title": "Historical Capture - Signing Authorities - 20260526-141436", "status": "AT RISK"})(),
                type("ProjectInsight", (), {"title": "Cash Management", "status": "AT RISK"})(),
            ]
        },
        "companies": {"insights": []},
        "people": {"insights": []},
        "decisions": {"top_decisions": []},
    }

    priorities = build_priorities(vault, entities, graph)["top_priorities"]
    titles = [item["title"] for item in priorities]

    assert titles[0] == "Cash Management"
    capture = next(item for item in priorities if item["title"].startswith("Historical Capture"))
    current = next(item for item in priorities if item["title"] == "Cash Management")
    assert capture["priority_score"] < current["priority_score"]


def test_build_actions_does_not_let_low_priority_capture_outrank_live_work():
    intelligence = ExecutiveIntelligence(
        executive_health=[],
        top_priorities=[
            ExecutiveLineItem(
                "Historical Capture - Signing Authorities - 20260526-141436",
                "LOW score 22. Review and confirm executive treatment",
            ),
            ExecutiveLineItem(
                "Cash Management",
                "HIGH score 82. Assign an accountable owner",
            ),
        ],
        objectives_requiring_attention=[],
        critical_meetings=[],
        projects_at_risk=[],
        followups_requiring_action=[
            ExecutiveLineItem("Follow Up Actions", "Follow up with Acme Capital today. Due: 2026-07-04; Priority: HIGH.")
        ],
        open_loops=[
            ExecutiveLineItem("LOOP-1", "Waiting for approval. Status: OPEN; Owner: Jane Smith.")
        ],
        key_people=[],
        supplier_risks=[],
        decisions_awaiting_attention=[],
        recommended_actions_today=["Escalate overdue follow-ups."],
        executive_summary=[],
    )
    followups = FollowupIntelligence(
        generated_at="2026-07-07T00:00:00+00:00",
        followup_count=1,
        overdue=[],
        due_today=[],
        due_this_week=[],
        waiting_on_others=[],
        high_priority=[],
        recommendations=["Escalate overdue follow-ups."],
        executive_summary=[],
    )
    open_loops = OpenLoopIntelligence(
        generated_at="2026-07-07T00:00:00+00:00",
        open_loop_count=1,
        critical_open_loops=[],
        waiting_for=[],
        stalled_projects=[],
        missing_decisions=[],
        missing_owners=[],
        recommended_actions=["Assign owner to LOOP-1."],
        executive_summary=[],
    )

    actions = _build_actions(intelligence, None, followups, open_loops)
    action_titles = [action.action for action in actions[:3]]

    assert all("Historical Capture" not in action for action in action_titles)
    assert any("Follow Up Actions" in action or "LOOP-1" in action or "Cash Management" in action for action in action_titles)


def test_priority_action_synthesis_is_specific_and_evidence_backed():
    intelligence = ExecutiveIntelligence(
        executive_health=[],
        top_priorities=[
            ExecutiveLineItem(
                "Cash Management",
                "CRITICAL score 82. Assign an accountable owner; Status: AT RISK; Owner: Jane Smith; Evidence: 03 Projects/Cash Management.md",
                context={
                    "priority": "CRITICAL",
                    "priority_score": 82,
                    "next_step": "Assign an accountable owner",
                    "status": "AT RISK",
                    "owner": "Jane Smith",
                    "deadline_or_recency": "dated evidence signal: 2026-07-04",
                    "evidence_paths": ["03 Projects/Cash Management.md"],
                    "why_now": ["Risk score 75", "No objective relationship detected"],
                    "confidence": "HIGH",
                },
            ),
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
    action = actions[0]
    assert action.action == (
        "Assign an accountable owner for Cash Management "
        "(AT RISK; owner Jane Smith; dated evidence signal: 2026-07-04)"
    )
    assert "Risk score 75" in action.why_it_matters
    assert "03 Projects/Cash Management.md" in action.supporting_evidence
    assert "Jane Smith" in action.expected_impact
