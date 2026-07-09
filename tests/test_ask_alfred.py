from pathlib import Path
import subprocess
import sys

from src.alfred.ask import ask_alfred_from_state
from src.executive.intent_contract import CanonicalExecutiveIntent
from src.executive.executive_reasoning import ExecutiveAction, ExecutiveReasoning
from src.executive.executive_state import ExecutiveState


def test_build_ask_alfred_outputs_response():
    output = Path("output/Ask_Alfred.md")
    if output.exists():
        output.unlink()

    result = subprocess.run(
        [sys.executable, "build_ask_alfred.py", "What should I do today?"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Executive Answer" in result.stdout
    assert "Supporting Evidence" in result.stdout
    assert "Confidence" in result.stdout
    assert "Recommended Next Actions" in result.stdout
    assert output.exists()

    content = output.read_text()
    assert "Executive Answer" in content
    assert "Supporting Evidence" in content
    assert "Confidence" in content
    assert "Recommended Next Actions" in content


def test_ask_alfred_uses_action_evidence_for_general_priority_answers(monkeypatch):
    state = ExecutiveState()
    reasoning = ExecutiveReasoning(
        overall_health="AMBER (80 / 100)",
        confidence="HIGH",
        key_themes=["1 top priority needs active triage."],
        top_actions=[
            ExecutiveAction(
                priority="CRITICAL",
                action="Assign an accountable owner for Cash Management (AT RISK; owner Jane Smith; dated evidence signal: 2026-07-04)",
                why_it_matters="Cash Management matters now because Risk score 75; No objective relationship detected.",
                supporting_evidence="Cash Management is evidenced by 03 Projects/Cash Management.md. CRITICAL score 82. Assign an accountable owner; Status: AT RISK.",
                expected_impact="Reduces at risk exposure for Cash Management and clarifies accountability with Jane Smith.",
                confidence="HIGH",
                score=82,
            )
        ],
        risks_requiring_immediate_attention=[],
        opportunities=[],
        decisions_required=[],
        recommended_agenda_for_today=[],
        executive_conclusion=[],
    )

    class IntelligenceStub:
        top_priorities = []
        recommended_actions_today = []
        supplier_risks = []
        followups_requiring_action = []
        open_loops = []

    monkeypatch.setattr("src.alfred.ask.build_executive_reasoning_from_state", lambda _: reasoning)
    monkeypatch.setattr("src.alfred.ask.build_executive_intelligence_from_state", lambda _: IntelligenceStub())

    response = ask_alfred_from_state("What should I do today?", state)

    assert response.executive_answer[1].startswith("Assign an accountable owner for Cash Management")
    assert any("03 Projects/Cash Management.md" in item for item in response.supporting_evidence)


def test_ask_alfred_supplier_answers_use_supplier_intent(monkeypatch):
    state = ExecutiveState()
    reasoning = ExecutiveReasoning(
        overall_health="AMBER (80 / 100)",
        confidence="HIGH",
        key_themes=["1 supplier relationship needs active triage."],
        top_actions=[],
        risks_requiring_immediate_attention=[],
        opportunities=[],
        decisions_required=[],
        recommended_agenda_for_today=[],
        executive_conclusion=[],
        intents=(
            CanonicalExecutiveIntent(
                intent_id="intent::supplier::acme-capital",
                intent_type="supplier",
                recommended_action="Validate ownership, dependency and supplier governance for Acme Capital (ACTIVE)",
                why_now="Acme Capital is elevated because ACTIVE; links 2; projects 1; people 0.",
                source_entities=("company::acme-capital",),
                source_work_items=(),
                priority="MEDIUM",
                urgency=None,
                confidence="MEDIUM",
                owner=None,
                blockers=(),
                dependencies=(),
                evidence_paths=("04 Companies/Acme Capital.md",),
                expiry=None,
                provenance={"evidence_paths": ("04 Companies/Acme Capital.md",)},
            ),
        ),
    )

    class IntelligenceStub:
        top_priorities = []
        recommended_actions_today = []
        followups_requiring_action = []
        open_loops = []
        supplier_risks = [type("Item", (), {"title": "Acme Capital", "detail": "ACTIVE; links 2; projects 1; people 0."})()]

    monkeypatch.setattr("src.alfred.ask.build_executive_reasoning_from_state", lambda _: reasoning)
    monkeypatch.setattr("src.alfred.ask.build_executive_intelligence_from_state", lambda _: IntelligenceStub())

    response = ask_alfred_from_state("Which suppliers require attention?", state)

    assert "Acme Capital" in response.executive_answer[1]
    assert "Acme Capital" in response.executive_answer[2]
