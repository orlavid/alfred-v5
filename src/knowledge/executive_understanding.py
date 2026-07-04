"""Executive note-understanding heuristics for Alfred."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Iterable

ENTITY_TYPES = (
    "objective",
    "project",
    "company",
    "person",
    "meeting",
    "decision",
    "risk",
    "policy",
    "daily_log",
    "executive_briefing",
)

TAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9_/-]+)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

FOLDER_RULES = {
    "objective": ("09 governance", "objectives", "objective", "okr", "goals"),
    "project": ("03 projects", "project", "programme", "initiative", "roadmap", "milestone"),
    "company": ("04 companies", "company", "supplier", "vendor", "customer", "partner"),
    "person": ("02 people", "people", "person", "stakeholder", "contacts"),
    "meeting": ("meeting", "minutes", "agenda", "committee", "board packs"),
    "decision": ("decision", "approvals", "decision log"),
    "risk": ("risk", "issue", "incident", "escalation"),
    "policy": ("policy", "standard", "governance", "framework", "control"),
    "daily_log": ("01 daily logs", "daily", "journal", "log"),
    "executive_briefing": ("briefing", "executive review", "board brief", "executive summary"),
}

KEYWORD_RULES = {
    "objective": ("objective", "okr", "goal", "target outcome", "strategic priority"),
    "project": ("project", "programme", "initiative", "delivery plan", "milestone"),
    "company": ("company", "supplier", "vendor", "csp", "partner", "counterparty"),
    "person": ("owner", "stakeholder", "lead", "chairman", "cfo", "chief"),
    "meeting": ("meeting", "agenda", "minutes", "attendees", "discussion"),
    "decision": ("decision", "approved", "approval", "decision required"),
    "risk": ("risk", "issue", "escalation", "blocked", "exposure"),
    "policy": ("policy", "standard", "control", "governance", "compliance"),
    "daily_log": ("daily", "today", "yesterday", "journal", "log"),
    "executive_briefing": ("briefing", "executive review", "board pack", "committee summary"),
}

TAG_RULES = {
    "objective": ("objective", "objectives", "okr", "goal"),
    "project": ("project", "projects", "programme", "initiative"),
    "company": ("company", "supplier", "vendor", "partner"),
    "person": ("people", "person", "owner", "stakeholder"),
    "meeting": ("meeting", "meetings", "agenda", "minutes"),
    "decision": ("decision", "decisions", "approval"),
    "risk": ("risk", "issue", "escalation"),
    "policy": ("policy", "governance", "compliance"),
    "daily_log": ("daily", "journal", "log"),
    "executive_briefing": ("briefing", "board-pack", "executive-review"),
}


@dataclass(frozen=True)
class ExecutiveUnderstandingResult:
    entity_type: str
    confidence: str
    score: int
    reasons: tuple[str, ...]
    tags: tuple[str, ...]
    frontmatter: dict[str, object]
    aliases: tuple[str, ...]
    links: tuple[str, ...]


@dataclass(frozen=True)
class ExecutiveUnderstandingRecord:
    path: str
    title: str
    entity_type: str
    confidence: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class ExecutiveUnderstandingReport:
    source_root: str
    records: tuple[ExecutiveUnderstandingRecord, ...]
    inventory: dict[str, int]
    summary: tuple[str, ...]


def classify_executive_note(path: Path | str, text: str) -> ExecutiveUnderstandingResult:
    note_path = Path(path)
    frontmatter = parse_frontmatter(text)
    tags = _combine_tags(extract_tags(text), frontmatter)
    links = extract_links(text)
    aliases = extract_aliases(frontmatter)
    lowered_path = str(note_path).lower()
    lowered_text = text.lower()
    title = note_path.stem.lower()

    best_type = "note"
    best_score = 0
    best_reasons: list[str] = []

    for entity_type in ENTITY_TYPES:
        score = 0
        reasons: list[str] = []

        if _matches_any(lowered_path, FOLDER_RULES[entity_type]):
            score += 4
            reasons.append("folder convention")
        if _matches_any(title, KEYWORD_RULES[entity_type]):
            score += 2
            reasons.append("title language")
        if _matches_any(lowered_text, KEYWORD_RULES[entity_type]):
            score += 1
            reasons.append("executive language")
        if _match_frontmatter(frontmatter, entity_type):
            score += 5
            reasons.append("frontmatter")
        if _match_tags(tags, entity_type):
            score += 3
            reasons.append("tags")
        if entity_type == "meeting" and links:
            score += 1
            reasons.append("wikilinks")
        if entity_type == "executive_briefing" and "executive" in lowered_text:
            score += 1
            reasons.append("executive phrasing")

        if score > best_score:
            best_type = entity_type
            best_score = score
            best_reasons = reasons

    confidence = _score_to_confidence(best_score)
    return ExecutiveUnderstandingResult(
        entity_type=best_type,
        confidence=confidence,
        score=best_score,
        reasons=tuple(dict.fromkeys(best_reasons)),
        tags=tuple(tags),
        frontmatter=frontmatter,
        aliases=tuple(aliases),
        links=tuple(links),
    )


def build_executive_understanding(source_root: Path) -> ExecutiveUnderstandingReport:
    records: list[ExecutiveUnderstandingRecord] = []
    inventory = {entity_type: 0 for entity_type in ENTITY_TYPES}
    for path in sorted(source_root.rglob("*.md")):
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        result = classify_executive_note(path.relative_to(source_root), text)
        if result.entity_type not in ENTITY_TYPES:
            continue
        inventory[result.entity_type] += 1
        records.append(
            ExecutiveUnderstandingRecord(
                path=str(path.relative_to(source_root)),
                title=path.stem,
                entity_type=result.entity_type,
                confidence=result.confidence,
                reasons=result.reasons,
            )
        )
    summary = (
        f"Source root: {source_root}.",
        f"Recognised {len(records)} executive entities.",
        f"Objectives: {inventory['objective']}; Projects: {inventory['project']}; Meetings: {inventory['meeting']}.",
    )
    return ExecutiveUnderstandingReport(
        source_root=str(source_root),
        records=tuple(records),
        inventory=inventory,
        summary=summary,
    )


def render_executive_understanding(report: ExecutiveUnderstandingReport) -> str:
    parts = ["# Executive Understanding", "", "## Summary", ""]
    parts.extend(f"- {item}" for item in report.summary)
    parts.extend(["", "## Inventory", ""])
    parts.extend(f"- {entity_type}: {report.inventory.get(entity_type, 0)}" for entity_type in ENTITY_TYPES)
    parts.extend(["", "## Recognised Entities", ""])
    if report.records:
        parts.extend(
            f"- {record.title} | Type: {record.entity_type} | Confidence: {record.confidence} | Reasons: {', '.join(record.reasons) or 'none'} | Source: {record.path}"
            for record in report.records[:100]
        )
    else:
        parts.append("_None found._")
    parts.append("")
    return "\n".join(parts)


def render_executive_understanding_json(report: ExecutiveUnderstandingReport) -> str:
    return json.dumps(
        {
            "source_root": report.source_root,
            "inventory": report.inventory,
            "records": [
                {
                    "path": record.path,
                    "title": record.title,
                    "entity_type": record.entity_type,
                    "confidence": record.confidence,
                    "reasons": list(record.reasons),
                }
                for record in report.records
            ],
            "summary": list(report.summary),
        },
        indent=2,
        sort_keys=True,
    )


def parse_frontmatter(text: str) -> dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, object] = {}
    current_list_key: str | None = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- ") and current_list_key:
            existing = data.setdefault(current_list_key, [])
            if isinstance(existing, list):
                existing.append(line[2:].strip().strip("'\""))
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if not value:
            data[key] = []
            current_list_key = key
            continue
        if value.startswith("[") and value.endswith("]"):
            data[key] = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
        else:
            data[key] = value.strip("'\"")
    return data


def extract_tags(text: str) -> list[str]:
    return sorted(set(match.lower() for match in TAG_RE.findall(text)))


def extract_links(text: str) -> list[str]:
    return sorted({match.split("|")[0].strip() for match in WIKILINK_RE.findall(text)})


def extract_aliases(frontmatter: dict[str, object]) -> list[str]:
    aliases = frontmatter.get("aliases") or frontmatter.get("alias") or []
    if isinstance(aliases, str):
        return [aliases]
    if isinstance(aliases, list):
        return [str(item) for item in aliases]
    return []


def _combine_tags(tags: Iterable[str], frontmatter: dict[str, object]) -> list[str]:
    merged = {tag.lower() for tag in tags}
    frontmatter_tags = frontmatter.get("tags") or []
    if isinstance(frontmatter_tags, str):
        merged.add(frontmatter_tags.lower())
    elif isinstance(frontmatter_tags, list):
        merged.update(str(item).lower() for item in frontmatter_tags)
    return sorted(merged)


def _matches_any(value: str, tokens: Iterable[str]) -> bool:
    return any(token in value for token in tokens)


def _match_tags(tags: Iterable[str], entity_type: str) -> bool:
    tag_values = {tag.lower() for tag in tags}
    return bool(tag_values & set(TAG_RULES[entity_type]))


def _match_frontmatter(frontmatter: dict[str, object], entity_type: str) -> bool:
    frontmatter_values: list[str] = []
    for key, value in frontmatter.items():
        frontmatter_values.append(key.lower())
        if isinstance(value, str):
            frontmatter_values.append(value.lower())
        elif isinstance(value, list):
            frontmatter_values.extend(str(item).lower() for item in value)
    return _matches_any(" ".join(frontmatter_values), FOLDER_RULES[entity_type] + KEYWORD_RULES[entity_type])


def _score_to_confidence(score: int) -> str:
    if score >= 6:
        return "HIGH"
    if score >= 3:
        return "MEDIUM"
    return "LOW"
