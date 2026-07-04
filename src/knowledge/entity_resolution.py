"""Canonical executive entity resolution for Alfred."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable

CANONICAL_FOLDER_PRIORITY = [
    "09 Governance/",
    "03 Projects/",
    "04 Companies/",
    "02 People/",
    "01 Daily Logs/",
    "06 Systems/",
    "05 Knowledge/",
    "07 AI Memory/Entities/",
]

CANONICAL_ENTITY_TYPES = {
    "objective",
    "project",
    "company",
    "person",
    "meeting",
    "decision",
    "risk",
    "policy",
}

COMPANY_SUFFIXES = {
    "limited",
    "ltd",
    "plc",
    "csp",
    "inc",
    "llc",
    "corp",
    "corporation",
    "group",
}

ABBREVIATION_OVERRIDES = {
    "microsoft": {"msft"},
}
REVERSE_ABBREVIATION_OVERRIDES = {
    alias: canonical
    for canonical, aliases in ABBREVIATION_OVERRIDES.items()
    for alias in aliases
}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class AliasResolution:
    alias: str
    canonical_id: str
    canonical_name: str
    confidence: str


@dataclass(frozen=True)
class CanonicalEntity:
    canonical_id: str
    canonical_name: str
    entity_type: str
    source_path: str
    aliases: tuple[str, ...]
    confidence: str


@dataclass(frozen=True)
class EntityResolutionModel:
    index: dict[str, list]
    canonical_entities: tuple[CanonicalEntity, ...]
    aliases: tuple[AliasResolution, ...]
    relationships: tuple[dict, ...]


def normalise_name(value: str) -> str:
    if not value:
        return ""
    value = _strip_wikilinks(value)
    value = value.lower().strip()
    value = re.sub(r"\.md$", "", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    words = [word for word in value.split() if word not in COMPANY_SUFFIXES]
    return " ".join(words).strip()


def build_entity_resolution(entities: Iterable) -> EntityResolutionModel:
    grouped: dict[tuple[str, str], list] = defaultdict(list)
    index: dict[str, list] = defaultdict(list)

    for entity in entities:
        entity_type = _canonical_type(entity.type)
        canonical_key = _canonical_group_key(entity)
        grouped[(entity_type, canonical_key)].append(entity)

        for key in _resolution_keys(entity):
            if not key:
                continue
            index[key].append(entity)

    canonical_entities: list[CanonicalEntity] = []
    aliases: list[AliasResolution] = []
    relationships: list[dict] = []
    seen_alias_keys = set()

    for (_entity_type, _key), candidates in sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1])):
        canonical = choose_canonical(candidates)
        alias_values = sorted(
            {
                _display_alias(value)
                for entity in candidates
                for value in _raw_resolution_values(entity)
                if _display_alias(value)
            }
        )
        confidence = _canonical_confidence(candidates)
        canonical_entities.append(
            CanonicalEntity(
                canonical_id=canonical.id,
                canonical_name=canonical.title,
                entity_type=_canonical_type(canonical.type),
                source_path=canonical.path,
                aliases=tuple(alias_values),
                confidence=confidence,
            )
        )

        for alias in alias_values:
            alias_key = normalise_name(alias)
            dedupe_key = (alias_key, canonical.id)
            if not alias_key or dedupe_key in seen_alias_keys:
                continue
            seen_alias_keys.add(dedupe_key)
            aliases.append(
                AliasResolution(
                    alias=alias,
                    canonical_id=canonical.id,
                    canonical_name=canonical.title,
                    confidence=_alias_confidence(alias, canonical.title),
                )
            )
            if alias_key != normalise_name(canonical.title):
                relationships.append(
                    {
                        "source": alias,
                        "target": canonical.title,
                        "relationship_type": "alias_of",
                    }
                )

    normalised_index = {
        key: sorted(value, key=lambda entity: (canonical_rank(entity), len(entity.path), entity.path))
        for key, value in sorted(index.items())
    }
    relationships.sort(key=lambda item: (item["target"], item["source"], item["relationship_type"]))

    return EntityResolutionModel(
        index=normalised_index,
        canonical_entities=tuple(canonical_entities),
        aliases=tuple(aliases),
        relationships=tuple(relationships),
    )


def canonical_rank(entity) -> int:
    for i, prefix in enumerate(CANONICAL_FOLDER_PRIORITY):
        if entity.path.startswith(prefix):
            return i
    return 999


def choose_canonical(candidates: list) -> object:
    return sorted(
        candidates,
        key=lambda entity: (
            canonical_rank(entity),
            normalise_name(entity.title) in REVERSE_ABBREVIATION_OVERRIDES,
            _canonical_type(entity.type) not in CANONICAL_ENTITY_TYPES,
            len(entity.path),
            entity.path,
        ),
    )[0]


def build_resolution_index(entities: Iterable) -> dict[str, list]:
    return build_entity_resolution(entities).index


def resolve_link_with_index(link: str, index: dict[str, list]):
    candidates = index.get(normalise_name(link), [])
    if not candidates:
        return None
    return choose_canonical(candidates)


def auto_resolution_map_from_index(index: dict[str, list]) -> dict[str, dict]:
    resolved = {}
    for key, candidates in index.items():
        if len(candidates) <= 1:
            continue
        canonical = choose_canonical(candidates)
        resolved[key] = {
            "canonical": canonical.id,
            "variants": [entity.id for entity in candidates if entity.id != canonical.id],
        }
    return resolved


def unresolved_links_with_index(entities: Iterable, index: dict[str, list]) -> list[dict]:
    unresolved = []
    for entity in entities:
        for link in entity.links:
            if resolve_link_with_index(link, index):
                continue
            unresolved.append(
                {
                    "source": entity.title,
                    "source_path": entity.path,
                    "missing": link,
                }
            )
    return unresolved


def resolution_summary_from_index(index: dict[str, list]) -> dict:
    auto_map = auto_resolution_map_from_index(index)
    ambiguous = {
        key: [entity.id for entity in value]
        for key, value in index.items()
        if len(value) > 1
    }
    return {
        "resolution_keys": len(index),
        "ambiguous_keys": len(ambiguous),
        "auto_resolvable_keys": len(auto_map),
        "ambiguous_examples": dict(list(sorted(ambiguous.items()))[:10]),
        "auto_resolution_examples": dict(list(sorted(auto_map.items()))[:10]),
    }


def _canonical_group_key(entity) -> str:
    title_key = normalise_name(entity.title)
    stem_key = normalise_name(Path(entity.path).stem)
    if title_key in REVERSE_ABBREVIATION_OVERRIDES:
        return REVERSE_ABBREVIATION_OVERRIDES[title_key]
    if stem_key in REVERSE_ABBREVIATION_OVERRIDES:
        return REVERSE_ABBREVIATION_OVERRIDES[stem_key]
    raw_keys = sorted(
        {
            key
            for key in (title_key, stem_key, _company_base_key(entity.title))
            if key
        }
    )
    return raw_keys[0] if raw_keys else normalise_name(entity.path)


def _resolution_keys(entity) -> set[str]:
    keys = set()
    for value in _raw_resolution_values(entity):
        if value:
            keys.add(normalise_name(value))
    base = _company_base_key(entity.title)
    if base:
        keys.add(base)
        keys.update(ABBREVIATION_OVERRIDES.get(base, set()))
    abbreviation = _abbreviation_key(entity.title)
    if abbreviation:
        keys.add(abbreviation)
    return {key for key in keys if key}


def _raw_resolution_values(entity) -> list[str]:
    values = [
        entity.title,
        Path(entity.path).stem,
        entity.path.split("/")[-1],
    ]
    values.extend(getattr(entity, "aliases", []))
    values.extend(_wikilink_variants(entity.title))
    return values


def _wikilink_variants(value: str) -> list[str]:
    matches = []
    for match in WIKILINK_RE.findall(value):
        matches.append(match.split("|")[0].strip())
    return matches


def _canonical_type(value: str) -> str:
    lowered = value.lower()
    if lowered == "daily_log":
        return "daily_log"
    if lowered == "executive_briefing":
        return "executive_briefing"
    return lowered


def _company_base_key(value: str) -> str:
    words = normalise_name(value).split()
    if not words:
        return ""
    filtered = [word for word in words if word not in COMPANY_SUFFIXES]
    return " ".join(filtered or words)


def _abbreviation_key(value: str) -> str:
    words = [word for word in normalise_name(value).split() if word]
    if len(words) < 2:
        return ""
    abbreviation = "".join(word[0] for word in words)
    return abbreviation if len(abbreviation) >= 2 else ""


def _alias_confidence(alias: str, canonical_name: str) -> str:
    if normalise_name(alias) == normalise_name(canonical_name):
        return "HIGH"
    if _abbreviation_key(canonical_name) and normalise_name(alias) == _abbreviation_key(canonical_name):
        return "MEDIUM"
    return "MEDIUM"


def _canonical_confidence(candidates: list) -> str:
    if len(candidates) >= 3:
        return "HIGH"
    if len(candidates) == 2:
        return "MEDIUM"
    return "LOW"


def _display_alias(value: str) -> str:
    value = _strip_wikilinks(value).strip()
    value = re.sub(r"\.md$", "", value, flags=re.IGNORECASE)
    return value


def _strip_wikilinks(value: str) -> str:
    return WIKILINK_RE.sub(lambda match: match.group(1).split("|")[0].strip(), value)
