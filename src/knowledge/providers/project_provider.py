"""Project extraction provider.

This mirrors the proven legacy project behaviour:

- projects come from curated notes under `03 Projects`
- recent executive references support inclusion
- engineering artefacts, dated files, and generic generated notes are excluded
- filenames alone are not enough unless the note behaves like a project note
"""

from __future__ import annotations

import re

from executive.knowledge.entity import VaultEntity
from executive.knowledge.vault import VaultNote

from src.knowledge.providers.base import ExecutiveKnowledgeProvider, ProviderMatch, _extract_links, _extract_tags

PROJECT_ROOT = "03 Projects/"
PROJECT_REFERENCE_ROOTS = (
    "01 Daily Logs/",
    "04 Companies/",
    "04 Decisions/",
    "05 Meetings/",
    "06 Risks/",
    "Minutes/",
)
EXCLUDED_PATH_PARTS = (
    "/archive/",
    "98 archive/",
    "07 ai memory/",
    "09 governance/watchlists/",
    "09 governance/open loops/",
    "output/",
    "analysis/",
    "docs/",
)
EXCLUDED_TITLE_RE = re.compile(
    r"(?i)\b("
    r"watchlist|open loop|strategic memory synthesis|synthesis|inventory|catalogue|summary|"
    r"entity graph|latest entity graph|charter|weekly|daily|report|objective intelligence|uuid|"
    r"capture|enriched"
    r")\b"
)
DATE_ONLY_RE = re.compile(r"^(?:19|20)\d{2}(?:-\d{2}-\d{2})?$")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f-]{27,}$", re.I)
PROJECT_SIGNAL_RE = re.compile(
    r"(?is)\b("
    r"project|programme|program|initiative|implementation|migration|rollout|workstream|"
    r"vendor management|procurement|tprm|due diligence|contract|remediation|target|milestone|"
    r"delivery|phase\s+\d+|operating model|review|approval|action|objective|scope|"
    r"transition|onboarding|business case"
    r")\b"
)
PROJECT_TAG_RE = re.compile(
    r"(?im)^tags:\s*\[[^\]]*\b(programme|project-[a-z0-9_-]+|vendor-governance|procurement-support|tprm)\b[^\]]*\]"
    r"|(?<!\w)#(programme|project-[a-z0-9_-]+|vendor-governance|procurement-support|tprm)\b"
)
PROJECT_STRUCTURE_RE = re.compile(
    r"(?im)^##\s+.*\b("
    r"context|objective|scope|service model|delivery options|follow-up tasks|meeting notes|"
    r"next steps|risk|actions underway|timeline|dependencies"
    r")\b"
)


class ProjectProvider(ExecutiveKnowledgeProvider):
    domain = "projects"

    def extract_matches(self, notes: list[VaultNote]) -> list[ProviderMatch]:
        references = _project_references(notes)
        matches: list[ProviderMatch] = []
        for note in notes:
            if _is_legacy_project_note(note, references):
                matches.append(ProviderMatch("project", note))
        return matches

    def extract_entities(self, notes: list[VaultNote]) -> list[VaultEntity]:
        return [
            VaultEntity(
                id=match.note.path,
                type=match.entity_type,
                title=match.note.title,
                path=match.note.path,
                tags=_extract_tags(match.note.text),
                links=_extract_links(match.note.text),
                source_text=match.note.text,
            )
            for match in self.extract_matches(notes)
        ]


def _project_references(notes: list[VaultNote]) -> set[str]:
    references: set[str] = set()
    for note in notes:
        if not any(note.path.startswith(root) for root in PROJECT_REFERENCE_ROOTS):
            continue
        for link in _extract_links(note.text):
            target = link.split("|", 1)[0].strip().replace("\\", "/")
            if target.startswith(PROJECT_ROOT):
                references.add(target)
                if not target.endswith(".md"):
                    references.add(f"{target}.md")
                continue
            slug = target.rsplit("/", 1)[-1].strip()
            if slug:
                references.add(f"{PROJECT_ROOT}{slug}.md")
    return references


def _is_legacy_project_note(note: VaultNote, references: set[str]) -> bool:
    path = note.path.replace("\\", "/")
    lowered_path = path.lower()
    title = note.title.strip()
    lowered_title = title.lower()

    if not path.startswith(PROJECT_ROOT):
        return False
    if any(part in lowered_path for part in EXCLUDED_PATH_PARTS):
        return False
    if EXCLUDED_TITLE_RE.search(title):
        return False
    if DATE_ONLY_RE.match(title) or UUID_RE.match(title):
        return False
    if lowered_title.endswith(" review") and "bia review" not in lowered_title:
        return False
    if lowered_title.endswith(" discussion") or lowered_title.endswith(" lookup"):
        return False
    if lowered_title in {"finance", "legal", "itinerary", "data types"}:
        return False

    explicit_marker = bool(PROJECT_TAG_RE.search(note.text))
    project_signal = bool(PROJECT_SIGNAL_RE.search(note.text))
    title_signal = bool(PROJECT_SIGNAL_RE.search(title))
    structured_project_note = bool(PROJECT_STRUCTURE_RE.search(note.text))
    tags = {tag.lower() for tag in _extract_tags(note.text)}
    lowered_text = note.text.lower()
    links = _extract_links(note.text)
    executive_path_links = any(
        link.startswith(("04 Companies/", "04 Decisions/", "02 People/", "05 Meetings/", "01 Daily Logs/", "09 Governance/Objectives/", "09 Objectives/"))
        for link in links
    )
    objective_title_links = any(
        "/" not in link and not link.lower().endswith(".md")
        for link in links
    )
    linked_to_executive_domains = executive_path_links or objective_title_links
    explicit_metadata = any(
        marker in note.text.lower()
        for marker in ("status:", "owner:", "accountable:", "deadline:", "target date:", "next review:")
    )
    if ("insurance-tech" in tags or "insurance-tech" in lowered_text) and not (
        title_signal or structured_project_note or explicit_marker or explicit_metadata
    ):
        return False

    return (
        explicit_marker
        or title_signal
        or project_signal
        or structured_project_note
        or (title_signal and explicit_metadata)
        or (linked_to_executive_domains and (title_signal or project_signal or structured_project_note))
    )
