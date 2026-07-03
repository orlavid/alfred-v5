"""Executive knowledge housekeeping report builder."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re

from src.executive.executive_intelligence import build_executive_intelligence, render_executive_intelligence
from src.executive.executive_reasoning import build_executive_reasoning, render_executive_reasoning
from src.mining.knowledge_miner import (
    DEFAULT_LEGACY_ROOT,
    build_knowledge_mining_report,
    render_knowledge_mining_report,
)

SECTION_HEADINGS = [
    "Executive Summary",
    "Active Records",
    "Dormant Records",
    "Archived Candidates",
    "Orphaned Records",
    "Duplicate Candidates",
    "Review Required",
    "Recommended Actions",
]

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_ROOT = ROOT / "output"
DEFAULT_EVIDENCE_ROOT = ROOT / "evidence" / "alfred-inventory"

DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
ARTEFACT_RE = re.compile(
    r"^- (?P<title>.+?) \| Type: (?P<record_type>[^|]+) \| Source: (?P<source>[^|]+) \| "
    r"Confidence: (?P<confidence>[^|]+) \| Import: (?P<import_recommendation>[^|]+) \| "
    r"ExecutiveState: (?P<mapping>.+)$"
)


@dataclass(frozen=True)
class CuratedRecord:
    title: str
    record_type: str
    source: str
    confidence: str
    import_recommendation: str
    suggested_mapping: str
    detail: str
    classification: str
    rationale: str


@dataclass(frozen=True)
class KnowledgeHousekeepingReport:
    executive_summary: list[str]
    active_records: list[CuratedRecord]
    dormant_records: list[CuratedRecord]
    archived_candidates: list[CuratedRecord]
    orphaned_records: list[CuratedRecord]
    duplicate_candidates: list[CuratedRecord]
    review_required: list[CuratedRecord]
    recommended_actions: list[str]


def build_knowledge_housekeeping(
    output_root: Path | None = None,
    *,
    evidence_root: Path | None = None,
    legacy_root: Path | None = None,
    today: date | None = None,
) -> KnowledgeHousekeepingReport:
    effective_output_root = output_root or DEFAULT_OUTPUT_ROOT
    effective_evidence_root = evidence_root or DEFAULT_EVIDENCE_ROOT
    effective_legacy_root = legacy_root or DEFAULT_LEGACY_ROOT
    effective_today = today or date.today()

    records = _collect_records(effective_output_root, effective_evidence_root, effective_legacy_root)
    records = _annotate_duplicates(records)
    classified = [_classify_record(record, effective_today) for record in records]

    active = _select(classified, "Active")
    dormant = _select(classified, "Dormant")
    archived = _select(classified, "Archived")
    orphaned = _select(classified, "Orphaned")
    duplicates = _select(classified, "Duplicate Candidate")
    review = _select(classified, "Review Required")

    summary = [
        f"Curated {len(classified)} executive records from generated intelligence and mining outputs.",
        f"Active: {len(active)}; Dormant: {len(dormant)}; Archived Candidates: {len(archived)}.",
        f"Orphaned: {len(orphaned)}; Duplicate Candidates: {len(duplicates)}; Review Required: {len(review)}.",
    ]
    actions = _build_recommended_actions(active, dormant, archived, orphaned, duplicates, review)

    return KnowledgeHousekeepingReport(
        executive_summary=summary,
        active_records=active,
        dormant_records=dormant,
        archived_candidates=archived,
        orphaned_records=orphaned,
        duplicate_candidates=duplicates,
        review_required=review,
        recommended_actions=actions,
    )


def render_knowledge_housekeeping(report: KnowledgeHousekeepingReport) -> str:
    parts = ["# Knowledge Housekeeping", ""]
    parts.extend(["## Executive Summary", ""])
    parts.extend(_render_bullets(report.executive_summary))
    parts.extend(["", "## Active Records", ""])
    parts.extend(_render_records(report.active_records))
    parts.extend(["", "## Dormant Records", ""])
    parts.extend(_render_records(report.dormant_records))
    parts.extend(["", "## Archived Candidates", ""])
    parts.extend(_render_records(report.archived_candidates))
    parts.extend(["", "## Orphaned Records", ""])
    parts.extend(_render_records(report.orphaned_records))
    parts.extend(["", "## Duplicate Candidates", ""])
    parts.extend(_render_records(report.duplicate_candidates))
    parts.extend(["", "## Review Required", ""])
    parts.extend(_render_records(report.review_required))
    parts.extend(["", "## Recommended Actions", ""])
    parts.extend(_render_bullets(report.recommended_actions))
    parts.append("")
    return "\n".join(parts)


def _collect_records(output_root: Path, evidence_root: Path, legacy_root: Path) -> list[CuratedRecord]:
    records = []
    records.extend(_parse_mining_report(_load_mining_text(output_root, legacy_root)))
    records.extend(_parse_markdown_sections(_load_executive_intelligence_text(output_root, evidence_root), "Executive_Intelligence.md"))
    records.extend(_parse_markdown_sections(_load_executive_reasoning_text(output_root, evidence_root), "Executive_Reasoning.md"))
    deduped: list[CuratedRecord] = []
    seen = set()
    for record in sorted(records, key=lambda item: (item.title.lower(), item.source, item.record_type, item.detail)):
        key = (record.title.lower(), record.source, record.record_type, record.detail)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(record)
    return deduped


def _load_mining_text(output_root: Path, legacy_root: Path) -> str:
    path = output_root / "Knowledge_Mining_Report.md"
    if path.exists():
        return path.read_text()
    return render_knowledge_mining_report(build_knowledge_mining_report(legacy_root))


def _load_executive_intelligence_text(output_root: Path, evidence_root: Path) -> str:
    path = output_root / "Executive_Intelligence.md"
    if path.exists():
        return path.read_text()
    return render_executive_intelligence(build_executive_intelligence(evidence_root))


def _load_executive_reasoning_text(output_root: Path, evidence_root: Path) -> str:
    path = output_root / "Executive_Reasoning.md"
    if path.exists():
        return path.read_text()
    return render_executive_reasoning(build_executive_reasoning(evidence_root))


def _parse_mining_report(text: str) -> list[CuratedRecord]:
    records: list[CuratedRecord] = []
    current_section = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        match = ARTEFACT_RE.match(line)
        if match:
            mapping = match.groupdict()
            records.append(
                CuratedRecord(
                    title=mapping["title"].strip(),
                    record_type=mapping["record_type"].strip(),
                    source=mapping["source"].strip(),
                    confidence=mapping["confidence"].strip(),
                    import_recommendation=mapping["import_recommendation"].strip(),
                    suggested_mapping=mapping["mapping"].strip(),
                    detail=f"Mining section: {current_section}",
                    classification="",
                    rationale="",
                )
            )
            continue
        if current_section == "Discarded Technical Debt" and line.startswith("- "):
            item = line[2:].strip()
            records.append(
                CuratedRecord(
                    title=item,
                    record_type="technical_debt",
                    source="Knowledge_Mining_Report.md",
                    confidence="LOW",
                    import_recommendation="DISCARD",
                    suggested_mapping="none",
                    detail="Discarded technical debt from mining report.",
                    classification="",
                    rationale="",
                )
            )
    return records


def _parse_markdown_sections(text: str, filename: str) -> list[CuratedRecord]:
    allowed = {
        "Top Priorities": ("priority", "recommendations", "HIGH"),
        "Objectives Requiring Attention": ("objective", "objectives", "MEDIUM"),
        "Critical Meetings": ("meeting", "meetings", "MEDIUM"),
        "Projects At Risk": ("project", "projects", "HIGH"),
        "Follow-ups Requiring Action": ("followup", "followups", "MEDIUM"),
        "Open Loops": ("open_loop", "open_loops", "HIGH"),
        "Key People": ("person", "people", "MEDIUM"),
        "Supplier Risks": ("company", "suppliers", "HIGH"),
        "Decisions Awaiting Attention": ("decision", "recommendations", "MEDIUM"),
        "Recommended Actions Today": ("recommendation", "recommendations", "HIGH"),
        "Top 10 Executive Actions": ("recommendation", "recommendations", "HIGH"),
        "Risks Requiring Immediate Attention": ("risk", "risks", "HIGH"),
        "Decisions Required": ("decision", "recommendations", "HIGH"),
        "Recommended Agenda For Today": ("recommendation", "recommendations", "MEDIUM"),
    }
    records: list[CuratedRecord] = []
    section = ""
    action_title = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            section = line[3:].strip()
            action_title = ""
            continue
        if line.startswith("### "):
            action_title = line[4:].strip()
            continue
        if section not in allowed or not line.startswith("- "):
            continue
        record_type, mapping, confidence = allowed[section]
        detail = line[2:].strip()
        if section == "Top 10 Executive Actions":
            if not detail.startswith("Action: "):
                continue
            detail = detail.removeprefix("Action: ").strip()
        title = action_title if section == "Top 10 Executive Actions" and action_title else _derive_title(detail)
        records.append(
            CuratedRecord(
                title=title,
                record_type=record_type,
                source=f"{filename}::{section}",
                confidence=confidence,
                import_recommendation="REVIEW" if confidence == "MEDIUM" else "IMPORT",
                suggested_mapping=mapping,
                detail=detail,
                classification="",
                rationale="",
            )
        )
    return records


def _annotate_duplicates(records: list[CuratedRecord]) -> list[CuratedRecord]:
    grouped: dict[str, list[CuratedRecord]] = {}
    for record in records:
        grouped.setdefault(_normalise(record.title), []).append(record)

    annotated = []
    for record in records:
        peers = grouped[_normalise(record.title)]
        if len(peers) < 2:
            annotated.append(record)
            continue
        sources = ", ".join(sorted({peer.source for peer in peers}))
        annotated.append(
            CuratedRecord(
                title=record.title,
                record_type=record.record_type,
                source=record.source,
                confidence=record.confidence,
                import_recommendation=record.import_recommendation,
                suggested_mapping=record.suggested_mapping,
                detail=record.detail,
                classification="Duplicate Candidate",
                rationale=f"Same normalised title appears across {len(peers)} records: {sources}.",
            )
        )
    return annotated


def _classify_record(record: CuratedRecord, today: date) -> CuratedRecord:
    if record.classification == "Duplicate Candidate":
        return record

    lowered = f"{record.title} {record.detail}".lower()
    if record.import_recommendation == "DISCARD" or record.record_type == "technical_debt":
        return _with_classification(record, "Archived", "Marked for discard or identified as technical debt.")

    if any(marker in lowered for marker in ("owner: unknown", "owner: none", "no owner", "no objective linked", "no supplier/company linked", "no graph linkage", "projects 0; objectives 0")):
        return _with_classification(record, "Orphaned", "Record lacks a clear owner, linkage, or supporting context.")

    stale_date = _extract_latest_date(lowered)
    if stale_date is not None and (today - stale_date).days >= 30:
        return _with_classification(record, "Dormant", f"Latest explicit date {stale_date.isoformat()} is more than 30 days old.")

    if record.import_recommendation == "REVIEW" or record.confidence == "MEDIUM" or any(marker in lowered for marker in ("watch", "limited supporting evidence", "review whether", "importance ")):
        return _with_classification(record, "Review Required", "Evidence is partial, medium-confidence, or explicitly asks for review.")

    return _with_classification(record, "Active", "Current intelligence marks this as active or import-worthy.")


def _with_classification(record: CuratedRecord, classification: str, rationale: str) -> CuratedRecord:
    return CuratedRecord(
        title=record.title,
        record_type=record.record_type,
        source=record.source,
        confidence=record.confidence,
        import_recommendation=record.import_recommendation,
        suggested_mapping=record.suggested_mapping,
        detail=record.detail,
        classification=classification,
        rationale=rationale,
    )


def _select(records: list[CuratedRecord], classification: str) -> list[CuratedRecord]:
    return [
        record
        for record in sorted(records, key=lambda item: (item.title.lower(), item.source, item.detail))
        if record.classification == classification
    ][:25]


def _build_recommended_actions(
    active: list[CuratedRecord],
    dormant: list[CuratedRecord],
    archived: list[CuratedRecord],
    orphaned: list[CuratedRecord],
    duplicates: list[CuratedRecord],
    review: list[CuratedRecord],
) -> list[str]:
    actions = []
    if orphaned:
        actions.append(f"Assign owners or supporting links to {len(orphaned)} orphaned records first.")
    if duplicates:
        actions.append(f"Merge or suppress {len(duplicates)} duplicate candidates before importing them into ExecutiveState.")
    if review:
        actions.append(f"Review {len(review)} medium-confidence or ambiguous records before promotion.")
    if dormant:
        actions.append(f"Reconfirm whether {len(dormant)} stale records should be reactivated or archived.")
    if archived:
        actions.append(f"Archive or ignore {len(archived)} records already marked as technical debt or discard candidates.")
    if active:
        actions.append(f"Keep {len(active)} active records in the live executive briefing set.")
    return actions or ["No housekeeping action required."]


def _derive_title(detail: str) -> str:
    cleaned = detail
    for separator in (": ", ". ", " | ", "; "):
        if separator in cleaned:
            head = cleaned.split(separator, 1)[0].strip()
            if head:
                return head
    return cleaned.strip()


def _normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _extract_latest_date(value: str) -> date | None:
    dates = []
    for match in DATE_RE.findall(value):
        try:
            dates.append(date.fromisoformat(match))
        except ValueError:
            continue
    return max(dates) if dates else None


def _render_records(records: list[CuratedRecord]) -> list[str]:
    if not records:
        return ["_None found._"]
    return [
        f"- {record.title} | Type: {record.record_type} | Source: {record.source} | "
        f"Confidence: {record.confidence} | Mapping: {record.suggested_mapping} | "
        f"Why: {record.rationale}"
        for record in records
    ]


def _render_bullets(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values] or ["_None found._"]
