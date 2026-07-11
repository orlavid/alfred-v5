"""Objective extraction provider.

This provider intentionally mirrors the legacy Alfred objective route:

- objectives are a dedicated retrieval path
- generated governance/AI/archive artefacts are excluded
- watchlists and open loops can support objectives but cannot become them
- filenames alone never create objective entities
"""

from __future__ import annotations

import re

from executive.knowledge.entity import VaultEntity
from executive.knowledge.vault import VaultNote

from src.knowledge.providers.base import ExecutiveKnowledgeProvider, ProviderMatch, _extract_links, _extract_tags

LEGACY_OBJECTIVE_ALLOWED_PATHS = (
    "09 objectives/",
    "09 governance/objectives/",
)
LEGACY_OBJECTIVE_EXCLUDED_PATHS = (
    "07 ai memory/",
    "07 executive briefings/",
    "09 governance/objective intelligence/",
    "09 governance/watchlists/",
    "09 governance/open loops/",
    "09 governance/escalations/",
    "09 governance/human action queue/",
    "09 governance/daily governance/",
    "09 governance/board packs/",
    "09 governance/board secretary/",
    "09 governance/governance intelligence/",
    "09 governance/executive metrics/",
    "09 governance/executive signals/",
    "09 governance/reflection intelligence/",
    "98 archive/",
)
EXPLICIT_OBJECTIVE_MARKER_RE = re.compile(
    r"(?im)^(?:type|entity_type|kind):\s*objective\s*$|(?<!\w)#(?:objective|objectives|okr)\b"
)
DATE_PREFIX_RE = re.compile(r"^(?:19|20)\d{2}-\d{2}-\d{2}\b")
BAD_TITLE_RE = re.compile(
    r"(?i)\b("
    r"watchlist|open loop|strategic memory synthesis|synthesis|inventory|catalogue|summary|"
    r"board pack|briefing|report|daily governance|governance intelligence|executive metrics"
    r")\b"
)
OBJECTIVE_EVIDENCE_RE = re.compile(
    r"(?is)\b(objective|objectives|goal|okr|target|deliverable|outcome|measure|milestone)\b"
)
OBJECTIVE_LIST_SECTION_RE = re.compile(
    r"(?ims)^##\s+Objectives\s*$\s*(.+?)(?:^\s*##\s+|\Z)"
)
OBJECTIVE_LIST_ITEM_RE = re.compile(r"(?im)^\s*\d+\.\s+(.+?)\s*$")
CANONICAL_OBJECTIVE_REGISTER_RE = re.compile(r"(?i)(?:^|/)09 governance/objectives/2026 executive objectives\.md$")


class ObjectiveProvider(ExecutiveKnowledgeProvider):
    domain = "objectives"

    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        matches: list[ProviderMatch] = []
        for note in notes:
            if _is_legacy_objective_note(note):
                matches.append(ProviderMatch("objective", note))
        return matches

    def extract_entities(self, notes: list[VaultNote]) -> list[VaultEntity]:
        entities: list[VaultEntity] = []
        for match in self.extract_matches(notes):
            extracted = _extract_objective_entities(match.note)
            if extracted:
                entities.extend(extracted)
                continue
            entities.append(
                VaultEntity(
                    id=match.note.path,
                    type=match.entity_type,
                    title=match.note.title,
                    path=match.note.path,
                    tags=_extract_tags(match.note.text),
                    links=_extract_links(match.note.text),
                    source_text=match.note.text,
                )
            )
        return entities


def _is_legacy_objective_note(note: VaultNote) -> bool:
    path = note.path.replace("\\", "/")
    lowered_path = path.lower()
    lowered_title = note.title.lower()

    if any(excluded in lowered_path for excluded in LEGACY_OBJECTIVE_EXCLUDED_PATHS):
        return False
    if DATE_PREFIX_RE.match(note.title) and BAD_TITLE_RE.search(note.title):
        return False
    if BAD_TITLE_RE.search(note.title):
        return False

    allowed_path = any(allowed in lowered_path for allowed in LEGACY_OBJECTIVE_ALLOWED_PATHS)
    explicit_marker = bool(EXPLICIT_OBJECTIVE_MARKER_RE.search(note.text))

    if not allowed_path and not explicit_marker:
        return False

    if "watchlist" in lowered_title or "open loop" in lowered_title:
        return False
    if "ai memory" in lowered_path or "executive briefings" in lowered_path:
        return False

    # Legacy objective retrieval uses operational evidence, not filenames.
    return bool(OBJECTIVE_EVIDENCE_RE.search(note.text))


def _extract_objective_entities(note: VaultNote) -> list[VaultEntity]:
    if not CANONICAL_OBJECTIVE_REGISTER_RE.search(note.path.replace("\\", "/")):
        return []

    section_match = OBJECTIVE_LIST_SECTION_RE.search(note.text)
    if not section_match:
        return []

    entities: list[VaultEntity] = []
    section = section_match.group(1)
    for index, raw_title in enumerate(OBJECTIVE_LIST_ITEM_RE.findall(section), start=1):
        title = raw_title.strip()
        if not title:
            continue
        slug = _slugify(title)
        anchored_path = f"{note.path}#objective-{index}-{slug}"
        entities.append(
            VaultEntity(
                id=anchored_path,
                type="objective",
                title=title,
                path=anchored_path,
                aliases=[],
                tags=_extract_tags(note.text),
                links=_extract_links(note.text),
                source_text=note.text,
            )
        )
    return entities


def _slugify(value: str) -> str:
    lowered = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return lowered or "objective"
