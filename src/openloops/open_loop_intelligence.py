"""Open loop intelligence report builder for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import json
import os
import re
from typing import Iterable

from executive.knowledge.resolver import normalise_name
from executive.knowledge.vault import VaultNote, load_vault
from src.obsidian.live_vault import resolve_live_vault_path

SECTION_HEADINGS = [
    "Critical Open Loops",
    "Waiting For",
    "Stalled Projects",
    "Missing Decisions",
    "Missing Owners",
    "Recommended Actions",
    "Executive Summary",
]

REGISTER_BLOCK_RE = re.compile(r"^## (LOOP-\d+)\s*$", re.MULTILINE)
KEY_VALUE_RE = re.compile(r"^([A-Za-z /]+):\s*(.*)$")

WAITING_MARKERS = (
    "waiting for",
    "waiting on",
    "awaiting",
    "pending",
    "blocked",
    "no response",
    "come back to me",
    "respond",
)

DECISION_MARKERS = (
    "decision",
    "approve",
    "approval",
    "sign-off",
    "agree",
    "finalize",
    "confirm",
)

OWNERLESS_MARKERS = (
    "owner: not mentioned",
    "owner: none",
    "no owner",
)

STALL_MARKERS = (
    "stalled",
    "slipped",
    "not currently usable",
    "need a plan",
    "workarounds",
    "blocked",
    "cannot progress",
)

SECOND_BRAIN_ROOT = Path(os.environ.get("ALFRED_SECOND_BRAIN_ROOT", "/opt/second-brain"))
DAILY_GOVERNANCE_INDEX = Path(
    os.environ.get(
        "ALFRED_DAILY_GOVERNANCE_INDEX",
        str(SECOND_BRAIN_ROOT / "executive" / "daily_governance_index.json"),
    )
)


@dataclass(frozen=True)
class OpenLoopItem:
    title: str
    path: str
    source_kind: str
    status: str
    priority: str
    owner: str
    summary: str


@dataclass(frozen=True)
class OpenLoopIntelligence:
    generated_at: str
    open_loop_count: int
    critical_open_loops: list[OpenLoopItem]
    waiting_for: list[OpenLoopItem]
    stalled_projects: list[OpenLoopItem]
    missing_decisions: list[OpenLoopItem]
    missing_owners: list[OpenLoopItem]
    recommended_actions: list[str]
    executive_summary: list[str]


def build_open_loop_intelligence(vault_root: Path | None = None) -> OpenLoopIntelligence:
    # Deprecated direct retrieval path retained for the default knowledge provider.
    # ExecutiveState is the canonical consumer for user-facing runtime knowledge.
    resolved_vault = resolve_live_vault_path(vault_root)
    daily_governance_items = _collect_daily_governance_open_loops()
    if daily_governance_items:
        items = daily_governance_items
    else:
        notes = load_vault(resolved_vault)
        items = _collect_open_loops(notes)

    critical_open_loops = _filter_items(items, lambda item: item.priority in {"CRITICAL", "HIGH"} or item.status in {"BLOCKED", "OPEN"})
    waiting_for = _filter_items(items, lambda item: any(marker in item.summary.lower() for marker in WAITING_MARKERS) or item.status == "BLOCKED")
    stalled_projects = _filter_items(items, lambda item: ("project" in item.path.lower() or "dora" in item.summary.lower()) and any(marker in item.summary.lower() for marker in STALL_MARKERS))
    missing_decisions = _filter_items(items, lambda item: _looks_like_missing_decision(item))
    missing_owners = _filter_items(items, lambda item: item.owner in {"Unknown", "Not mentioned", "None"} or any(marker in item.summary.lower() for marker in OWNERLESS_MARKERS))

    recommended_actions = _build_recommendations(critical_open_loops, waiting_for, stalled_projects, missing_decisions, missing_owners)
    executive_summary = _build_summary(items, critical_open_loops, waiting_for, stalled_projects, missing_decisions, missing_owners)

    return OpenLoopIntelligence(
        generated_at=datetime.now(UTC).isoformat(),
        open_loop_count=len(items),
        critical_open_loops=critical_open_loops,
        waiting_for=waiting_for,
        stalled_projects=stalled_projects,
        missing_decisions=missing_decisions,
        missing_owners=missing_owners,
        recommended_actions=recommended_actions,
        executive_summary=executive_summary,
    )


def _collect_daily_governance_open_loops() -> list[OpenLoopItem]:
    if not DAILY_GOVERNANCE_INDEX.exists():
        return []
    try:
        payload = json.loads(DAILY_GOVERNANCE_INDEX.read_text(encoding="utf-8"))
    except Exception:
        return []

    items: list[OpenLoopItem] = []
    seen: set[str] = set()
    records = payload.get("records", []) if isinstance(payload, dict) else []
    for record in records:
        if not isinstance(record, dict):
            continue
        if record.get("type") != "open_loop":
            continue
        if str(record.get("status", "open")).lower() != "open":
            continue
        summary = _clean_text(str(record.get("text", "")))
        if not summary or _looks_like_bad_open_loop(summary):
            continue
        key = normalise_name(summary)
        if key in seen:
            continue
        seen.add(key)
        items.append(
            OpenLoopItem(
                title=summary[:160],
                path=_relative_source_path(record.get("source")),
                source_kind="daily_governance_index",
                status="OPEN",
                priority=_derive_daily_governance_priority(summary),
                owner=(str(record.get("owner", "")).strip() or "Unknown"),
                summary=summary,
            )
        )

    items.sort(key=lambda item: (_priority_rank(item.priority), _status_rank(item.status), item.path, item.summary))
    return items[:250]


def _looks_like_bad_open_loop(summary: str) -> bool:
    lowered = summary.lower()
    return any(
        marker in lowered
        for marker in (
            "watchlist",
            "strategic memory synthesis",
            "latest entity graph",
            "governance charter",
            "what was on my follow up and open loops",
            "what as on my follow up and open loops",
        )
    )


def _derive_daily_governance_priority(summary: str) -> str:
    lowered = summary.lower()
    if any(marker in lowered for marker in ("deadline", "due", "eod", "urgent", "critical", "approval", "awaiting")):
        return "HIGH"
    return "MEDIUM"


def _relative_source_path(value: object) -> str:
    if not isinstance(value, str) or not value:
        return ""
    marker = "/docker/obsidian-vault/"
    if marker in value:
        return value.split(marker, 1)[1]
    return value


def render_open_loop_intelligence(report: OpenLoopIntelligence) -> str:
    parts = [
        "# Open Loop Intelligence",
        "",
        f"- Generated: {report.generated_at}",
        f"- Open Loops Analysed: {report.open_loop_count}",
        "",
        "## Critical Open Loops",
        "",
    ]
    parts.extend(_render_items(report.critical_open_loops))
    parts.extend(["", "## Waiting For", ""])
    parts.extend(_render_items(report.waiting_for))
    parts.extend(["", "## Stalled Projects", ""])
    parts.extend(_render_items(report.stalled_projects))
    parts.extend(["", "## Missing Decisions", ""])
    parts.extend(_render_items(report.missing_decisions))
    parts.extend(["", "## Missing Owners", ""])
    parts.extend(_render_items(report.missing_owners))
    parts.extend(["", "## Recommended Actions", ""])
    parts.extend(_render_bullets(report.recommended_actions))
    parts.extend(["", "## Executive Summary", ""])
    parts.extend(_render_bullets(report.executive_summary))
    parts.append("")
    return "\n".join(parts)


def _render_items(items: Iterable[OpenLoopItem]) -> list[str]:
    rendered = [
        f"- {item.summary} [{item.path}] (Status: {item.status}; Priority: {item.priority}; Owner: {item.owner})"
        for item in items
    ]
    return rendered or ["_None found._"]


def _render_bullets(values: Iterable[str]) -> list[str]:
    items = [f"- {value}" for value in values if value]
    return items or ["_None found._"]


def _collect_open_loops(notes: list[VaultNote]) -> list[OpenLoopItem]:
    items: list[OpenLoopItem] = []
    seen: set[tuple[str, str]] = set()

    for note in notes:
        if note.kind != "open_loop":
            continue

        extracted = _extract_register_items(note) if note.title == "Open Loop Register" else _extract_note_items(note)
        for item in extracted:
            key = (item.path, normalise_name(item.summary))
            if key in seen:
                continue
            seen.add(key)
            items.append(item)

    items.sort(key=lambda item: (_priority_rank(item.priority), _status_rank(item.status), item.path, item.summary))
    return items[:250]


def _extract_register_items(note: VaultNote) -> list[OpenLoopItem]:
    blocks = []
    matches = list(REGISTER_BLOCK_RE.finditer(note.text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(note.text)
        blocks.append((match.group(1), note.text[start:end]))

    items = []
    for loop_id, block in blocks:
        parsed = _parse_register_block(block)
        status = parsed.get("Status", "OPEN").upper()
        if status in {"CLOSED", "ARCHIVED"}:
            continue
        priority = parsed.get("Priority", "MEDIUM").upper()
        owner = parsed.get("Owner", "Unknown") or "Unknown"
        summary = parsed.get("Issue", loop_id)
        items.append(
            OpenLoopItem(
                title=loop_id,
                path=note.path,
                source_kind=note.kind,
                status=status,
                priority=priority,
                owner=owner,
                summary=_clean_text(summary),
            )
        )
    return items


def _parse_register_block(block: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    lines = block.splitlines()
    current_key: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal current_key, buffer
        if current_key is not None:
            parsed[current_key] = _strip_value(" ".join(buffer))
        current_key = None
        buffer = []

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        match = KEY_VALUE_RE.match(line)
        if match and match.group(1) in {"Status", "Priority", "Owner", "Category", "Created", "Last Reviewed", "Issue", "Evidence / Signals", "Closure Criteria", "Related Notes", "Reason"}:
            flush()
            current_key = match.group(1)
            buffer = [match.group(2)]
        elif current_key is not None:
            buffer.append(line)
    flush()
    return parsed


def _extract_note_items(note: VaultNote) -> list[OpenLoopItem]:
    title = note.title
    text = note.text
    items: list[OpenLoopItem] = []

    if "Open Loop Report" in text or "## Top 10 Open Loops" in text:
        items.extend(_extract_ranked_report_items(note))

    if note.path.startswith("09 Governance/Open Loops/"):
        items.append(
            OpenLoopItem(
                title=title,
                path=note.path,
                source_kind=note.kind,
                status=_extract_heading_value(text, "Status", default="OPEN").upper(),
                priority=_derive_watchlist_priority(text),
                owner=_derive_owner(text),
                summary=_derive_summary_from_watchlist(note),
            )
        )
        return items

    if not items:
        items.append(
            OpenLoopItem(
                title=title,
                path=note.path,
                source_kind=note.kind,
                status=_extract_status_from_text(text),
                priority=_derive_priority(text),
                owner=_derive_owner(text),
                summary=_derive_fallback_summary(note),
            )
        )

    return items


def _extract_ranked_report_items(note: VaultNote) -> list[OpenLoopItem]:
    items = []
    lines = note.text.splitlines()
    current_title = ""
    owner = "Unknown"
    summary = ""

    for line in lines:
        stripped = line.strip()
        match = re.match(r"^\d+\.\s+\*\*(.+?)\*\*$", stripped)
        if match:
            if current_title:
                items.append(
                    OpenLoopItem(
                        title=current_title,
                        path=note.path,
                        source_kind=note.kind,
                        status="OPEN",
                        priority="HIGH" if "critical" in summary.lower() else "MEDIUM",
                        owner=owner,
                        summary=summary or current_title,
                    )
                )
            current_title = _clean_text(match.group(1))
            owner = "Unknown"
            summary = current_title
            continue
        if stripped.startswith("- **Owner:**"):
            owner = _clean_text(stripped.split(":", 1)[1]) or "Unknown"
        elif stripped.startswith("- **Why it matters:**"):
            why = _clean_text(stripped.split(":", 1)[1])
            if why:
                summary = f"{current_title}. {why}"

    if current_title:
        items.append(
            OpenLoopItem(
                title=current_title,
                path=note.path,
                source_kind=note.kind,
                status="OPEN",
                priority="HIGH" if "critical" in summary.lower() else "MEDIUM",
                owner=owner,
                summary=summary or current_title,
            )
        )

    return items


def _extract_heading_value(text: str, heading: str, *, default: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\s*$\n(.+)$", re.MULTILINE)
    match = pattern.search(text)
    return _strip_value(match.group(1)) if match else default


def _derive_watchlist_priority(text: str) -> str:
    if _extract_heading_value(text, "Severity", default="").upper() in {"CRITICAL", "HIGH"}:
        return _extract_heading_value(text, "Severity", default="").upper()
    materiality = _extract_heading_value(text, "Materiality Score", default="")
    if materiality.startswith("10/10"):
        return "CRITICAL"
    if materiality.startswith("9/10"):
        return "HIGH"
    return "MEDIUM"


def _derive_owner(text: str) -> str:
    for marker in OWNERLESS_MARKERS:
        if marker in text.lower():
            return "Not mentioned"
    owner = _extract_heading_value(text, "Owner", default="")
    return owner or "Unknown"


def _derive_summary_from_watchlist(note: VaultNote) -> str:
    title = note.title.replace("Open Loop - ", "")
    trigger = _extract_heading_value(note.text, "Trigger", default="")
    recommended = _find_section_bullet(note.text, "Recommended actions")
    parts = [title]
    if trigger:
        parts.append(trigger)
    if recommended:
        parts.append(recommended)
    return _clean_text(". ".join(parts))


def _derive_fallback_summary(note: VaultNote) -> str:
    for line in note.text.splitlines():
        cleaned = _clean_text(line)
        if len(cleaned) < 24:
            continue
        if cleaned.startswith("#"):
            continue
        return cleaned
    return note.title


def _find_section_bullet(text: str, section_name: str) -> str:
    capture = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower() == f"## {section_name}".lower():
            capture = True
            continue
        if capture and stripped.startswith("## "):
            break
        if capture and stripped.startswith("-"):
            return _clean_text(stripped[1:])
    return ""


def _extract_status_from_text(text: str) -> str:
    lowered = text.lower()
    if "status: blocked" in lowered or "cannot progress" in lowered:
        return "BLOCKED"
    if "status: delegated" in lowered:
        return "DELEGATED"
    return "OPEN"


def _derive_priority(text: str) -> str:
    lowered = text.lower()
    if "critical" in lowered:
        return "CRITICAL"
    if "high" in lowered or "urgent" in lowered:
        return "HIGH"
    return "MEDIUM"


def _looks_like_missing_decision(item: OpenLoopItem) -> bool:
    lowered = item.summary.lower()
    return any(marker in lowered for marker in DECISION_MARKERS) and any(
        marker in lowered
        for marker in ("need", "pending", "missing", "required", "not mentioned", "finalize", "confirm")
    )


def _clean_text(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", value)
    value = re.sub(r"\[\[([^\]]+)\]\]", r"\1", value)
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -\t.").rstrip(".") + "."


def _strip_value(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", value)
    value = re.sub(r"\[\[([^\]]+)\]\]", r"\1", value)
    value = re.sub(r"\*\*(.*?)\*\*", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -\t.")


def _priority_rank(priority: str) -> int:
    return {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(priority, 9)


def _status_rank(status: str) -> int:
    return {"BLOCKED": 0, "OPEN": 1, "ACTIVE": 2, "DELEGATED": 3}.get(status, 9)


def _filter_items(items: list[OpenLoopItem], predicate) -> list[OpenLoopItem]:
    filtered = []
    for item in items:
        if item.summary.startswith("Generated:"):
            continue
        if predicate(item):
            filtered.append(item)
    return filtered[:15]


def _build_recommendations(
    critical_open_loops: list[OpenLoopItem],
    waiting_for: list[OpenLoopItem],
    stalled_projects: list[OpenLoopItem],
    missing_decisions: list[OpenLoopItem],
    missing_owners: list[OpenLoopItem],
) -> list[str]:
    recommendations = []
    if critical_open_loops:
        recommendations.append(f"Escalate the {len(critical_open_loops)} highest-risk open loops into a dated action register with explicit closure criteria.")
    if waiting_for:
        recommendations.append(f"Chase or reassign the {len(waiting_for)} blocked or dependency-led loops that are waiting for external response.")
    if stalled_projects:
        recommendations.append(f"Review the {len(stalled_projects)} stalled project loops and decide whether to unblock, de-scope, or escalate them.")
    if missing_decisions:
        recommendations.append(f"Push the {len(missing_decisions)} unresolved decision items into the next governance or operating review.")
    if missing_owners:
        recommendations.append(f"Assign owners to the {len(missing_owners)} ownerless loops before new open-loop debt accumulates.")
    return recommendations[:5]


def _build_summary(
    items: list[OpenLoopItem],
    critical_open_loops: list[OpenLoopItem],
    waiting_for: list[OpenLoopItem],
    stalled_projects: list[OpenLoopItem],
    missing_decisions: list[OpenLoopItem],
    missing_owners: list[OpenLoopItem],
) -> list[str]:
    summary = [
        f"Analysed {len(items)} active open loops from the register, governance watchlists, and generated loop reviews.",
        f"Detected {len(critical_open_loops)} critical or high-priority loops and {len(waiting_for)} loops waiting on dependencies or blocked progress.",
        f"Found {len(stalled_projects)} stalled project loops, {len(missing_decisions)} decision gaps, and {len(missing_owners)} owner gaps.",
    ]
    if critical_open_loops:
        summary.append(f"Top critical loop: {critical_open_loops[0].summary}")
    return summary[:4]
