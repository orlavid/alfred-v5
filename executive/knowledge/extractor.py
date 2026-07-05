"""Provider-backed entity extraction from executive Obsidian notes."""

from __future__ import annotations

import re
from pathlib import Path

from src.knowledge.providers import extract_provider_entities

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9_/-]+)")


def extract_links(text: str) -> list[str]:
    return [match.split("|")[0].strip() for match in WIKILINK_RE.findall(text)]


def extract_tags(text: str) -> list[str]:
    return sorted(set(TAG_RE.findall(text)))


def extract_entities(vault_root: Path):
    return list(extract_provider_entities(vault_root))
