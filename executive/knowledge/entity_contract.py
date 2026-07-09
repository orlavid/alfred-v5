from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
import re


DATE_TOKEN_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2}|\d{8})\b")
FIELD_PATTERNS = {
    "owner": re.compile(r"(?im)^(?:owner|accountable owner|assigned to):\s*(.+?)\s*$"),
    "delegates": re.compile(r"(?im)^(?:delegate|delegates):\s*(.+?)\s*$"),
    "status": re.compile(r"(?im)^status:\s*(.+?)\s*$"),
    "priority": re.compile(r"(?im)^priority:\s*(.+?)\s*$"),
    "risk_level": re.compile(r"(?im)^(?:risk|risk level):\s*(.+?)\s*$"),
    "due_date": re.compile(r"(?im)^(?:due(?: date)?|deadline):\s*(20\d{2}-\d{2}-\d{2}|\d{8})\s*$"),
    "review_date": re.compile(r"(?im)^(?:review date|last reviewed):\s*(20\d{2}-\d{2}-\d{2}|\d{8})\s*$"),
    "created": re.compile(r"(?im)^created:\s*(20\d{2}-\d{2}-\d{2}|\d{8})\s*$"),
    "last_activity": re.compile(r"(?im)^(?:last activity|updated|last updated):\s*(20\d{2}-\d{2}-\d{2}|\d{8})\s*$"),
}


@dataclass(frozen=True)
class CanonicalExecutiveEntityContract:
    entity_id: str
    entity_type: str
    canonical_name: str
    aliases: tuple[str, ...]
    owner: str | None
    delegates: tuple[str, ...]
    status: str | None
    priority: str | None
    risk_level: str | None
    confidence: str
    created: str | None
    last_activity: str | None
    due_date: str | None
    review_date: str | None
    related_objectives: tuple[str, ...]
    related_projects: tuple[str, ...]
    related_people: tuple[str, ...]
    related_meetings: tuple[str, ...]
    dependencies: tuple[str, ...]
    evidence_paths: tuple[str, ...]
    evidence_count: int
    supporting_notes: tuple[str, ...]
    missing_fields: tuple[str, ...]
    provenance: dict[str, tuple[str, ...]] = field(default_factory=dict)
    last_verified: str | None = None
    primary_path: str = ""
    provider: str = ""
    extensions: dict[str, object] = field(default_factory=dict)

    @property
    def id(self) -> str:
        return self.entity_id

    @property
    def type(self) -> str:
        return self.entity_type

    @property
    def title(self) -> str:
        return self.canonical_name

    @property
    def path(self) -> str:
        return self.primary_path


def canonicalise_date(value: str | None) -> str | None:
    if not value:
        return None
    if len(value) == 8 and value.isdigit():
        return f"{value[:4]}-{value[4:6]}-{value[6:]}"
    return value


def extract_explicit_field(field_name: str, grouped_entities: list) -> tuple[str | tuple[str, ...] | None, tuple[str, ...]]:
    pattern = FIELD_PATTERNS[field_name]
    values: list[tuple[str, str]] = []
    for entity in grouped_entities:
        match = pattern.search(getattr(entity, "source_text", ""))
        if not match:
            continue
        values.append((match.group(1).strip(), entity.path))

    if not values:
        return None, ()

    if field_name == "delegates":
        delegates = tuple(
            item.strip()
            for item in re.split(r"[;,]", values[0][0])
            if item.strip()
        )
        return delegates, tuple(sorted({path for _, path in values}))

    value = values[0][0]
    if field_name in {"due_date", "review_date", "created", "last_activity"}:
        value = canonicalise_date(value)
    return value, tuple(sorted({path for _, path in values}))


def latest_date_signal(values: list[str]) -> str | None:
    candidates: list[str] = []
    for value in values:
        for match in DATE_TOKEN_RE.findall(value):
            canonical = canonicalise_date(match)
            if canonical:
                candidates.append(canonical)
    return max(candidates) if candidates else None


def stable_date(values: list[str]) -> str | None:
    candidates: list[str] = []
    for value in values:
        for match in DATE_TOKEN_RE.findall(value):
            canonical = canonicalise_date(match)
            if canonical:
                candidates.append(canonical)
    return min(candidates) if candidates else None


def risk_bucket(score: int | None) -> str | None:
    if score is None:
        return None
    if score >= 80:
        return "CRITICAL"
    if score >= 50:
        return "HIGH"
    if score >= 25:
        return "MEDIUM"
    if score > 0:
        return "LOW"
    return None


def normalise_unknown(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if cleaned.lower() in {"unknown", "none", "not mentioned", ""}:
        return None
    if cleaned.startswith("(unknown "):
        return None
    return cleaned


def iso_today() -> str:
    return date.today().isoformat()
