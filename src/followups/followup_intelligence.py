"""Follow-up intelligence report builder for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
import re
from typing import Iterable

from executive.knowledge.resolver import normalise_name
from executive.knowledge.vault import VaultNote, load_vault
from src.obsidian.live_vault import resolve_live_vault_path

SECTION_HEADINGS = [
    "Overdue",
    "Due Today",
    "Due This Week",
    "Waiting On Others",
    "High Priority",
    "Recommendations",
    "Executive Summary",
]

ACTION_LINE_RE = re.compile(r"^\s*[-*]\s+(.*\S)\s*$")
OPEN_LOOP_RE = re.compile(r"^\s*-\s+\[\s\]\s+(.*\S)\s*$")
DATE_IN_TEXT_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2}|\d{2}/\d{2}/20\d{2})\b")

WAITING_MARKERS = (
    "waiting on",
    "awaiting",
    "pending",
    "come back to me",
    "responding",
    "reviewing",
    "sorting on their end",
    "no response",
    "requested approval",
)

HIGH_PRIORITY_MARKERS = (
    "urgent",
    "high priority",
    "critical",
    "required",
    "need a plan",
    "must",
    "escalation",
    "immediate",
)

DUE_TODAY_MARKERS = ("today", "by end of day", "eod")
DUE_WEEK_MARKERS = ("this week", "next week", "monday", "tuesday", "wednesday", "thursday", "friday")
ACTION_MARKERS = (
    "need to",
    "follow up",
    "follow-up",
    "next step",
    "action",
    "review",
    "confirm",
    "check",
    "lock",
    "agree",
    "raise",
    "resolve",
    "respond",
)


@dataclass(frozen=True)
class FollowupItem:
    title: str
    path: str
    source_kind: str
    due_date: str | None
    priority: str
    waiting_on_others: bool
    summary: str


@dataclass(frozen=True)
class FollowupIntelligence:
    generated_at: str
    followup_count: int
    overdue: list[FollowupItem]
    due_today: list[FollowupItem]
    due_this_week: list[FollowupItem]
    waiting_on_others: list[FollowupItem]
    high_priority: list[FollowupItem]
    recommendations: list[str]
    executive_summary: list[str]


def build_followup_intelligence(vault_root: Path | None = None, today: date | None = None) -> FollowupIntelligence:
    resolved_vault = resolve_live_vault_path(vault_root)
    effective_today = today or date.today()
    notes = load_vault(resolved_vault)

    items = _collect_followups(notes, effective_today)
    overdue = _filter_items(items, lambda item: _parse_due_date(item.due_date) is not None and _parse_due_date(item.due_date) < effective_today)
    due_today = _filter_items(items, lambda item: _parse_due_date(item.due_date) == effective_today)
    due_this_week = _filter_items(
        items,
        lambda item: (
            (due := _parse_due_date(item.due_date)) is not None
            and effective_today < due <= effective_today + timedelta(days=7)
        ),
    )
    waiting_on_others = _filter_items(items, lambda item: item.waiting_on_others)
    high_priority = _filter_items(items, lambda item: item.priority == "HIGH")

    recommendations = _build_recommendations(overdue, due_today, due_this_week, waiting_on_others, high_priority)
    executive_summary = _build_executive_summary(items, overdue, due_today, due_this_week, waiting_on_others, high_priority)

    return FollowupIntelligence(
        generated_at=datetime.now(UTC).isoformat(),
        followup_count=len(items),
        overdue=overdue,
        due_today=due_today,
        due_this_week=due_this_week,
        waiting_on_others=waiting_on_others,
        high_priority=high_priority,
        recommendations=recommendations,
        executive_summary=executive_summary,
    )


def render_followup_intelligence(report: FollowupIntelligence) -> str:
    parts = [
        "# Follow-up Intelligence",
        "",
        f"- Generated: {report.generated_at}",
        f"- Follow-ups Analysed: {report.followup_count}",
        "",
        "## Overdue",
        "",
    ]
    parts.extend(_render_items(report.overdue))
    parts.extend(["", "## Due Today", ""])
    parts.extend(_render_items(report.due_today))
    parts.extend(["", "## Due This Week", ""])
    parts.extend(_render_items(report.due_this_week))
    parts.extend(["", "## Waiting On Others", ""])
    parts.extend(_render_items(report.waiting_on_others))
    parts.extend(["", "## High Priority", ""])
    parts.extend(_render_items(report.high_priority))
    parts.extend(["", "## Recommendations", ""])
    parts.extend(_render_bullets(report.recommendations))
    parts.extend(["", "## Executive Summary", ""])
    parts.extend(_render_bullets(report.executive_summary))
    parts.append("")
    return "\n".join(parts)


def _render_items(items: Iterable[FollowupItem]) -> list[str]:
    rendered = []
    for item in items:
        due = item.due_date or "No explicit due date"
        rendered.append(
            f"- {item.summary} [{item.path}]"
            f" (Source: {item.source_kind}; Due: {due}; Priority: {item.priority})"
        )
    return rendered or ["_None found._"]


def _render_bullets(values: Iterable[str]) -> list[str]:
    items = [f"- {value}" for value in values if value]
    return items or ["_None found._"]


def _collect_followups(notes: list[VaultNote], today: date) -> list[FollowupItem]:
    items: list[FollowupItem] = []
    seen: set[tuple[str, str]] = set()

    for note in notes:
        note_date = _extract_note_date(note)
        for summary, due_date, reason in _extract_followup_candidates(note, note_date, today):
            key = (note.path, normalise_name(summary))
            if key in seen:
                continue
            seen.add(key)
            waiting_on_others = any(marker in summary.lower() for marker in WAITING_MARKERS)
            priority = "HIGH" if reason == "open_loop" or any(marker in summary.lower() for marker in HIGH_PRIORITY_MARKERS) else "NORMAL"
            items.append(
                FollowupItem(
                    title=note.title,
                    path=note.path,
                    source_kind=note.kind,
                    due_date=due_date.isoformat() if due_date else None,
                    priority=priority,
                    waiting_on_others=waiting_on_others,
                    summary=summary.rstrip(".") + ".",
                )
            )

    items.sort(key=lambda item: (_sort_due_date(item.due_date), item.priority != "HIGH", item.path, item.summary))
    return items[:200]


def _extract_followup_candidates(note: VaultNote, note_date: date | None, today: date) -> list[tuple[str, date | None, str]]:
    candidates: list[tuple[str, date | None, str]] = []
    lines = note.text.splitlines()

    for raw_line in lines:
        match = OPEN_LOOP_RE.match(raw_line)
        if not match:
            continue
        summary = _clean_line(match.group(1))
        if not summary:
            continue
        due_date = _infer_due_date(summary, note_date, today, prefer_open_loop=True)
        candidates.append((summary, due_date, "open_loop"))

    followup_section = _extract_section(lines, "Follow-Up Actions")
    for line in followup_section:
        match = ACTION_LINE_RE.match(line)
        summary = _clean_line(match.group(1) if match else line)
        if not _is_actionable(summary):
            continue
        due_date = _infer_due_date(summary, note_date, today)
        candidates.append((summary, due_date, "followup_section"))

    if note.kind in {"daily_log", "project", "company", "person", "objective", "open_loop"}:
        for raw_line in lines:
            summary = _clean_line(raw_line)
            if not _is_actionable(summary):
                continue
            due_date = _infer_due_date(summary, note_date, today)
            candidates.append((summary, due_date, "inferred"))

    return candidates


def _extract_section(lines: list[str], title: str) -> list[str]:
    wanted = f"## {title}".lower()
    captured: list[str] = []
    active = False
    for line in lines:
        lowered = line.strip().lower()
        if lowered == wanted:
            active = True
            continue
        if active and lowered.startswith("## "):
            break
        if active:
            captured.append(line)
    return captured


def _clean_line(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", value)
    value = re.sub(r"\[\[([^\]]+)\]\]", r"\1", value)
    value = re.sub(r"\[[^\]]+\]\([^)]+\)", "", value)
    value = re.sub(r"\s+", " ", value).strip(" -\t")
    return value


def _is_actionable(summary: str) -> bool:
    if not summary or len(summary) < 18:
        return False
    lowered = summary.lower()
    if lowered.startswith("#"):
        return False
    if any(marker in lowered for marker in ("stub — created", "please see the meeting minutes", "**summary**:", "summary:", "|")):
        return False
    return any(marker in lowered for marker in ACTION_MARKERS + WAITING_MARKERS + HIGH_PRIORITY_MARKERS + DUE_TODAY_MARKERS + DUE_WEEK_MARKERS)


def _infer_due_date(summary: str, note_date: date | None, today: date, *, prefer_open_loop: bool = False) -> date | None:
    lowered = summary.lower()
    explicit = _extract_date_from_text(summary)
    if explicit is not None:
        return explicit
    if "tomorrow" in lowered:
        if note_date is not None:
            return note_date + timedelta(days=1)
        return today + timedelta(days=1)
    if any(marker in lowered for marker in DUE_TODAY_MARKERS):
        return today
    if "this week" in lowered:
        return today + timedelta(days=max(0, 4 - today.weekday()))
    weekday_offsets = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
    }
    for name, target in weekday_offsets.items():
        if name in lowered:
            return today + timedelta(days=(target - today.weekday()) % 7)
    if prefer_open_loop and note_date is not None:
        return note_date
    return None


def _extract_date_from_text(summary: str) -> date | None:
    match = DATE_IN_TEXT_RE.search(summary)
    if not match:
        return None
    value = match.group(1)
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def _extract_note_date(note: VaultNote) -> date | None:
    for candidate in (note.title, note.path):
        match = DATE_IN_TEXT_RE.search(candidate)
        if not match:
            continue
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(match.group(1), fmt).date()
            except ValueError:
                continue
    return None


def _parse_due_date(value: str | None) -> date | None:
    if value is None:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def _sort_due_date(value: str | None) -> tuple[int, str]:
    if value is None:
        return (1, "")
    return (0, value)


def _filter_items(items: list[FollowupItem], predicate) -> list[FollowupItem]:
    return [item for item in items if predicate(item)][:15]


def _build_recommendations(
    overdue: list[FollowupItem],
    due_today: list[FollowupItem],
    due_this_week: list[FollowupItem],
    waiting_on_others: list[FollowupItem],
    high_priority: list[FollowupItem],
) -> list[str]:
    recommendations = []
    if overdue:
        recommendations.append(f"Escalate {len(overdue)} overdue follow-ups and assign clear owners with dated closure targets.")
    if due_today:
        recommendations.append(f"Review the {len(due_today)} items due today first and decide which need same-day executive attention.")
    if waiting_on_others:
        recommendations.append(f"Chase dependencies on {len(waiting_on_others)} items that are blocked by external or cross-team responses.")
    if high_priority:
        recommendations.append(f"Protect time for the {len(high_priority)} highest-priority items, especially unresolved open loops and escalation paths.")
    if due_this_week:
        recommendations.append(f"Sequence this week’s delivery plan around the {len(due_this_week)} near-term follow-ups before new work expands scope.")
    return recommendations[:5]


def _build_executive_summary(
    items: list[FollowupItem],
    overdue: list[FollowupItem],
    due_today: list[FollowupItem],
    due_this_week: list[FollowupItem],
    waiting_on_others: list[FollowupItem],
    high_priority: list[FollowupItem],
) -> list[str]:
    summary = [
        f"Analysed {len(items)} inferred follow-ups from daily logs, open loops, and operating notes.",
        f"Detected {len(overdue)} overdue items, {len(due_today)} due today, and {len(due_this_week)} due this week.",
        f"Found {len(waiting_on_others)} dependency-led follow-ups waiting on others and {len(high_priority)} high-priority items.",
    ]
    if overdue:
        summary.append(f"Oldest overdue item: {overdue[0].summary}")
    elif due_today:
        summary.append(f"Most immediate dated item: {due_today[0].summary}")
    return summary[:4]
