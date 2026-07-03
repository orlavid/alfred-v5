"""Structured board governance registry for Alfred."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json

SECTION_HEADINGS = [
    "Executive Summary",
    "Board Purpose",
    "Organisation Chart",
    "Board Members",
    "Weekly Board Meeting",
    "Monthly Board Meeting",
    "Decision Rights",
    "Standing Agenda",
    "Board Packs",
    "Minutes and Actions",
    "Registry Summary",
]


@dataclass(frozen=True)
class BoardMember:
    name: str
    role: str
    purpose: str
    responsibilities: tuple[str, ...]
    authority: str
    meeting_role: str
    weekly_board_contribution: str
    monthly_board_contribution: str
    prompt_profile: str
    communication_style: str
    portrait_placeholder: str
    status: str


@dataclass(frozen=True)
class BoardGovernance:
    board_purpose: list[str]
    organisation_chart: list[str]
    board_members: tuple[BoardMember, ...]
    weekly_board_meeting: list[str]
    monthly_board_meeting: list[str]
    decision_rights: list[str]
    standing_agenda: list[str]
    board_packs: list[str]
    minutes_and_actions: list[str]
    registry_summary: list[str]


def build_board_governance() -> BoardGovernance:
    members = tuple(_build_members())
    return BoardGovernance(
        board_purpose=[
            "Provide a first-class executive committee domain for direction, control, and operating cadence.",
            "Separate board governance from generic agents so decision rights and meeting behaviours stay explicit.",
            "Create a reusable machine-readable registry for weekly and monthly board operations.",
        ],
        organisation_chart=[
            "Chairman: Phillip.",
            "Executive Oracle: Alfred.",
            "Chief of Staff: Hermes Prime.",
            "Functional board members: Athena, Titan, Echo, Sterling, Sentinel, Vector.",
            "Execution and governance roles: Nigel and Victoria.",
        ],
        board_members=members,
        weekly_board_meeting=[
            "Purpose: run the weekly executive operating review.",
            "Cadence: weekly, fixed agenda, action-first decisions.",
            "Primary outputs: priorities, risks, ownership changes, and dated follow-through actions.",
        ],
        monthly_board_meeting=[
            "Purpose: run the monthly strategic and governance review.",
            "Cadence: monthly, focused on objectives, capital, control environment, and board-level decisions.",
            "Primary outputs: strategic decisions, budget calls, governance resets, and archived minutes.",
        ],
        decision_rights=[
            "Phillip holds final chair authority on direction, prioritisation, and escalation.",
            "Alfred frames evidence, options, and reasoning but does not replace the Chairman's final call.",
            "Hermes Prime coordinates board flow, decision capture, and operating follow-through.",
            "Functional members own recommendations inside their remit: strategy, operations, communications, finance, risk, and technology.",
            "Victoria governs minutes, resolution records, and board pack completeness.",
        ],
        standing_agenda=[
            "Executive health and material changes.",
            "Objectives and project progress.",
            "Financial posture and capital calls.",
            "Risk, controls, and governance matters.",
            "Open loops, actions, and decision log review.",
        ],
        board_packs=[
            "Weekly pack: executive summary, top priorities, risks, action register, and unresolved decisions.",
            "Monthly pack: strategy review, board scorecard, financial summary, governance exceptions, and archived minutes extract.",
            "Registry extract: current board members, roles, prompt profiles, and communication guidance.",
        ],
        minutes_and_actions=[
            "Minutes capture decisions, rationale, owners, and due dates.",
            "Actions are tracked separately from narrative minutes and reviewed at the next meeting.",
            "Board Secretary maintains the canonical record and closure status.",
        ],
        registry_summary=[
            f"Board members registered: {len(members)}.",
            "Registry is deterministic, machine-readable, and uses portrait placeholders until image assets exist.",
            "Status model is explicit per member to support future activation, delegation, or retirement workflows.",
        ],
    )


def render_board_governance(report: BoardGovernance) -> str:
    parts = ["# Board Governance", ""]
    parts.extend(["## Executive Summary", ""])
    parts.extend(_render_bullets(report.registry_summary[:2] + ["Board governance registry is active and reusable."]))
    parts.extend(["", "## Board Purpose", ""])
    parts.extend(_render_bullets(report.board_purpose))
    parts.extend(["", "## Organisation Chart", ""])
    parts.extend(_render_bullets(report.organisation_chart))
    parts.extend(["", "## Board Members", ""])
    parts.extend(_render_members(report.board_members))
    parts.extend(["", "## Weekly Board Meeting", ""])
    parts.extend(_render_bullets(report.weekly_board_meeting))
    parts.extend(["", "## Monthly Board Meeting", ""])
    parts.extend(_render_bullets(report.monthly_board_meeting))
    parts.extend(["", "## Decision Rights", ""])
    parts.extend(_render_bullets(report.decision_rights))
    parts.extend(["", "## Standing Agenda", ""])
    parts.extend(_render_bullets(report.standing_agenda))
    parts.extend(["", "## Board Packs", ""])
    parts.extend(_render_bullets(report.board_packs))
    parts.extend(["", "## Minutes and Actions", ""])
    parts.extend(_render_bullets(report.minutes_and_actions))
    parts.extend(["", "## Registry Summary", ""])
    parts.extend(_render_bullets(report.registry_summary))
    parts.append("")
    return "\n".join(parts)


def render_board_registry_json(report: BoardGovernance) -> str:
    payload = {
        "board_purpose": report.board_purpose,
        "organisation_chart": report.organisation_chart,
        "board_members": [asdict(member) for member in report.board_members],
        "weekly_board_meeting": report.weekly_board_meeting,
        "monthly_board_meeting": report.monthly_board_meeting,
        "decision_rights": report.decision_rights,
        "standing_agenda": report.standing_agenda,
        "board_packs": report.board_packs,
        "minutes_and_actions": report.minutes_and_actions,
        "registry_summary": report.registry_summary,
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _build_members() -> list[BoardMember]:
    return [
        BoardMember(
            name="Phillip",
            role="Chairman",
            purpose="Chair the board and make final executive calls.",
            responsibilities=("Set direction", "Approve decisions", "Resolve escalations"),
            authority="Final board authority on strategy, prioritisation, and governance escalations.",
            meeting_role="Chairs weekly and monthly board meetings.",
            weekly_board_contribution="Approves weekly priorities, resolves blockers, and assigns owners.",
            monthly_board_contribution="Sets strategic direction and validates major governance decisions.",
            prompt_profile="Decisive chair; asks for compressed evidence and clear options.",
            communication_style="Direct, high-judgement, concise.",
            portrait_placeholder="PORTRAIT_PENDING_PHILLIP",
            status="ACTIVE",
        ),
        BoardMember(
            name="Alfred",
            role="Executive Oracle",
            purpose="Synthesize evidence, reasoning, and recommendations for the board.",
            responsibilities=("Summarize evidence", "Generate options", "Highlight risks"),
            authority="Advisory authority across every board domain; no final approval authority.",
            meeting_role="Presents board briefing, options, and recommended actions.",
            weekly_board_contribution="Delivers operating intelligence and action prioritisation.",
            monthly_board_contribution="Delivers executive synthesis across strategy, control, and execution.",
            prompt_profile="Analytical synthesizer with evidence-first reasoning.",
            communication_style="Structured, factual, concise.",
            portrait_placeholder="PORTRAIT_PENDING_ALFRED",
            status="ACTIVE",
        ),
        BoardMember(
            name="Hermes Prime",
            role="Chief of Staff",
            purpose="Coordinate board flow, packs, and follow-through.",
            responsibilities=("Coordinate agenda", "Track actions", "Maintain operating cadence"),
            authority="Operational authority over board process and execution tracking.",
            meeting_role="Runs the board machine around the Chairman and Executive Oracle.",
            weekly_board_contribution="Prepares weekly board pack and action register.",
            monthly_board_contribution="Coordinates strategic review preparation and escalation tracking.",
            prompt_profile="Execution-first coordinator with low tolerance for ambiguity.",
            communication_style="Operational, disciplined, follow-through oriented.",
            portrait_placeholder="PORTRAIT_PENDING_HERMES_PRIME",
            status="ACTIVE",
        ),
        BoardMember(
            name="Athena",
            role="Strategy",
            purpose="Represent strategic planning, objective alignment, and long-range judgment.",
            responsibilities=("Test strategy", "Review objectives", "Challenge drift"),
            authority="Authority to recommend strategic changes and challenge misalignment.",
            meeting_role="Leads strategy segments and objective reviews.",
            weekly_board_contribution="Flags strategic drift in weekly execution signals.",
            monthly_board_contribution="Owns strategy review and objective alignment discussion.",
            prompt_profile="Strategic, comparative, long-horizon.",
            communication_style="Calm, conceptual, high signal.",
            portrait_placeholder="PORTRAIT_PENDING_ATHENA",
            status="ACTIVE",
        ),
        BoardMember(
            name="Titan",
            role="Operations",
            purpose="Represent delivery, execution capacity, and operating resilience.",
            responsibilities=("Monitor execution", "Surface operational issues", "Drive remediation"),
            authority="Authority to recommend operating interventions and delivery resets.",
            meeting_role="Leads execution and delivery review.",
            weekly_board_contribution="Reports operating friction, capacity, and delivery misses.",
            monthly_board_contribution="Reviews operating model health and improvement priorities.",
            prompt_profile="Execution and throughput operator.",
            communication_style="Practical, blunt, execution-heavy.",
            portrait_placeholder="PORTRAIT_PENDING_TITAN",
            status="ACTIVE",
        ),
        BoardMember(
            name="Echo",
            role="Communications",
            purpose="Represent narrative control, board messaging, and stakeholder clarity.",
            responsibilities=("Shape narrative", "Clarify messaging", "Support external and internal communication"),
            authority="Authority to recommend messaging posture and communications sequencing.",
            meeting_role="Advises on narrative, stakeholder messaging, and board wording.",
            weekly_board_contribution="Sharpens weekly briefing language and stakeholder updates.",
            monthly_board_contribution="Frames board-level narratives and summary communications.",
            prompt_profile="Narrative editor with clarity bias.",
            communication_style="Clear, polished, audience-aware.",
            portrait_placeholder="PORTRAIT_PENDING_ECHO",
            status="ACTIVE",
        ),
        BoardMember(
            name="Sterling",
            role="Finance / CFO",
            purpose="Represent capital allocation, financial posture, and economic discipline.",
            responsibilities=("Review spend", "Challenge forecasts", "Guard capital discipline"),
            authority="Authority to recommend or block financial moves pending chair approval.",
            meeting_role="Leads financial posture and capital discussion.",
            weekly_board_contribution="Highlights spend risk, forecast changes, and immediate finance actions.",
            monthly_board_contribution="Owns monthly finance review and board capital recommendations.",
            prompt_profile="Financial controller with value and discipline focus.",
            communication_style="Measured, numeric, sceptical.",
            portrait_placeholder="PORTRAIT_PENDING_STERLING",
            status="ACTIVE",
        ),
        BoardMember(
            name="Sentinel",
            role="Risk",
            purpose="Represent risk, controls, governance exceptions, and compliance posture.",
            responsibilities=("Track risk", "Challenge weak controls", "Escalate governance gaps"),
            authority="Authority to escalate material control failures directly to the Chairman.",
            meeting_role="Leads risk and controls review.",
            weekly_board_contribution="Maintains board awareness of live risks and unresolved controls.",
            monthly_board_contribution="Owns formal risk and governance review.",
            prompt_profile="Risk sentinel focused on controls and exposure.",
            communication_style="Alert, precise, conservative.",
            portrait_placeholder="PORTRAIT_PENDING_SENTINEL",
            status="ACTIVE",
        ),
        BoardMember(
            name="Vector",
            role="Technology / Trading",
            purpose="Represent platform, systems, trading, and technical operating leverage.",
            responsibilities=("Review technical posture", "Assess platform risk", "Advance trading capability"),
            authority="Authority to recommend technology and trading interventions.",
            meeting_role="Leads technology and trading discussion.",
            weekly_board_contribution="Reports platform health, technical debt, and trading-system pressure.",
            monthly_board_contribution="Reviews technology roadmap and trading performance posture.",
            prompt_profile="Technical operator with systems and markets focus.",
            communication_style="Fast, technical, evidence-heavy.",
            portrait_placeholder="PORTRAIT_PENDING_VECTOR",
            status="ACTIVE",
        ),
        BoardMember(
            name="Nigel",
            role="Chief of Staff execution and follow-through",
            purpose="Ensure decisions convert into tracked execution.",
            responsibilities=("Chase actions", "Maintain due dates", "Escalate slippage"),
            authority="Authority to enforce follow-through discipline and escalate stale actions.",
            meeting_role="Owns action closeout and execution discipline in board meetings.",
            weekly_board_contribution="Runs action status review and challenge on missed commitments.",
            monthly_board_contribution="Produces follow-through review and closure rate summary.",
            prompt_profile="Follow-through enforcer with zero-slippage bias.",
            communication_style="Persistent, explicit, deadline-driven.",
            portrait_placeholder="PORTRAIT_PENDING_NIGEL",
            status="ACTIVE",
        ),
        BoardMember(
            name="Victoria",
            role="Board Secretary",
            purpose="Maintain formal records, governance hygiene, and meeting artifacts.",
            responsibilities=("Record minutes", "Maintain registry", "Control board artifacts"),
            authority="Authority over the canonical board record and governance documentation quality.",
            meeting_role="Records minutes, decisions, and formal action statements.",
            weekly_board_contribution="Maintains weekly minute pack and action ledger.",
            monthly_board_contribution="Maintains monthly board records and resolution archive.",
            prompt_profile="Governance recorder with precision and memory discipline.",
            communication_style="Formal, exact, archival.",
            portrait_placeholder="PORTRAIT_PENDING_VICTORIA",
            status="ACTIVE",
        ),
    ]


def _render_bullets(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values] or ["_None found._"]


def _render_members(members: tuple[BoardMember, ...]) -> list[str]:
    lines: list[str] = []
    for member in members:
        responsibilities = ", ".join(member.responsibilities)
        lines.extend(
            [
                f"### {member.name} — {member.role}",
                f"- Purpose: {member.purpose}",
                f"- Responsibilities: {responsibilities}",
                f"- Authority: {member.authority}",
                f"- Meeting Role: {member.meeting_role}",
                f"- Weekly Board Contribution: {member.weekly_board_contribution}",
                f"- Monthly Board Contribution: {member.monthly_board_contribution}",
                f"- Prompt Profile: {member.prompt_profile}",
                f"- Communication Style: {member.communication_style}",
                f"- Portrait Placeholder: {member.portrait_placeholder}",
                f"- Status: {member.status}",
                "",
            ]
        )
    return lines or ["_None found._"]
