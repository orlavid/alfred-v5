"""Vault loading and executive note classification."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

EXECUTIVE_EXCLUDED_SEGMENTS = {
    "output",
    "system",
    "trees",
    "python",
    "analysis",
    ".git",
    ".obsidian",
    ".smart-env",
    "node_modules",
    "__pycache__",
}
EXECUTIVE_EXCLUDED_PREFIXES = (
    "docs/migration/",
)


@dataclass(frozen=True)
class VaultNote:
    path: str
    title: str
    folder: str
    text: str
    kind: str


def classify(path: Path, text: str = "") -> str:
    rel_path = str(path).replace("\\", "/").lower()
    lowered = f"{rel_path}\n{text.lower()}"
    folder = path.parts[0].lower() if path.parts else ""

    folder_map = {
        "01 daily logs": "daily_log",
        "02 people": "person",
        "03 projects": "project",
        "04 companies": "company",
        "04 decisions": "decision",
        "05 meetings": "meeting",
        "06 risks": "risk",
        "07 open loops": "open_loop",
        "08 follow ups": "follow_up",
        "08 follow-ups": "follow_up",
        "09 objectives": "objective",
        "10 briefings": "executive_briefing",
    }
    if folder in folder_map:
        return folder_map[folder]

    if "follow-up intelligence" in lowered or "open loop intelligence" in lowered:
        return "report"
    if "01 daily logs" in lowered or "/daily/" in lowered or "daily log" in lowered:
        return "daily_log"
    if "10 briefings" in lowered or "briefing" in lowered or "executive review" in lowered or "board pack" in lowered:
        return "executive_briefing"
    if "05 meetings" in lowered or "meeting" in lowered or "minutes" in lowered or "agenda" in lowered:
        return "meeting"
    if "09 objectives" in lowered or "objective" in lowered or "okr" in lowered:
        return "objective"
    if "03 projects" in lowered or "project" in lowered or "programme" in lowered or "initiative" in lowered:
        return "project"
    if "02 people" in lowered or "people" in lowered or "stakeholder" in lowered or "owner" in lowered:
        return "person"
    if "04 companies" in lowered or "compan" in lowered or "supplier" in lowered or "vendor" in lowered:
        return "company"
    if "04 decisions" in lowered or "decision" in lowered or "approval" in lowered or "sign-off" in lowered:
        return "decision"
    if "06 risks" in lowered or "risk" in lowered or "issue" in lowered or "escalation" in lowered:
        return "risk"
    if "07 open loops" in lowered or "open loop" in lowered:
        return "open_loop"
    if "08 follow ups" in lowered or "08 follow-ups" in lowered or "follow up" in lowered or "follow-up" in lowered:
        return "follow_up"
    if "policy" in lowered or "framework" in lowered or "standard" in lowered or "governance" in lowered:
        return "policy"
    return "note"


def load_vault(vault_root: Path) -> list[VaultNote]:
    notes: list[VaultNote] = []
    if not vault_root.exists() or not vault_root.is_dir():
        return notes

    for path in sorted(vault_root.rglob("*.md")):
        if _is_excluded_path(path, vault_root):
            continue
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue

        rel = path.relative_to(vault_root)
        notes.append(
            VaultNote(
                path=str(rel).replace("\\", "/"),
                title=path.stem,
                folder=rel.parts[0] if rel.parts else "",
                text=text,
                kind=classify(rel, text),
            )
        )

    return notes


def _is_excluded_path(path: Path, vault_root: Path) -> bool:
    rel = str(path.relative_to(vault_root)).replace("\\", "/")
    lowered = rel.lower()
    if any(lowered.startswith(prefix) for prefix in EXECUTIVE_EXCLUDED_PREFIXES):
        return True
    segments = {segment.lower() for segment in path.relative_to(vault_root).parts}
    return any(segment in EXECUTIVE_EXCLUDED_SEGMENTS for segment in segments)
