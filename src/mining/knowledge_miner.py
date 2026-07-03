"""Read-only executive knowledge miner for legacy Alfred installations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Iterable

DEFAULT_LEGACY_ROOT = Path("/root")

EXECUTIVE_SECTIONS = [
    "Objectives",
    "Projects",
    "Companies",
    "People",
    "Decisions",
    "Open Loops",
    "Risks",
    "Relationships",
    "Dashboard Ideas",
    "Recommended Imports",
    "Discarded Technical Debt",
    "Import Summary",
]

TEXT_EXTENSIONS = {".md", ".txt", ".json", ".yml", ".yaml"}
IGNORE_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "logs",
    "log",
    "backups",
    "backup",
    "deploy",
    "deployments",
    "docker",
    ".pytest_cache",
}
IGNORE_FILE_PATTERNS = (
    "backup",
    ".log",
    ".py",
    ".sh",
    ".tar",
    ".zip",
    ".sqlite",
)

CATEGORY_RULES = {
    "objective": {
        "section": "Objectives",
        "mapping": "objectives",
        "patterns": ("objective", "okr", "goal", "strategy"),
    },
    "project": {
        "section": "Projects",
        "mapping": "projects",
        "patterns": ("project", "programme", "initiative", "workstream"),
    },
    "company": {
        "section": "Companies",
        "mapping": "suppliers",
        "patterns": ("company", "supplier", "vendor", "partner"),
    },
    "person": {
        "section": "People",
        "mapping": "people",
        "patterns": ("people", "person", "stakeholder", "owner"),
    },
    "decision": {
        "section": "Decisions",
        "mapping": "recommendations",
        "patterns": ("decision", "approval", "sign-off"),
    },
    "open_loop": {
        "section": "Open Loops",
        "mapping": "open_loops",
        "patterns": ("open loop", "blocked", "waiting", "pending"),
    },
    "risk": {
        "section": "Risks",
        "mapping": "risks",
        "patterns": ("risk", "issue", "concern", "escalation"),
    },
    "relationship": {
        "section": "Relationships",
        "mapping": "meetings",
        "patterns": ("relationship", "linked", "depends on", "reports to"),
    },
    "dashboard": {
        "section": "Dashboard Ideas",
        "mapping": "recommendations",
        "patterns": ("dashboard", "kpi", "scorecard", "heatmap"),
    },
    "meeting": {
        "section": "Relationships",
        "mapping": "meetings",
        "patterns": ("meeting", "agenda", "attendees", "minutes"),
    },
    "governance": {
        "section": "Risks",
        "mapping": "recommendations",
        "patterns": ("governance", "committee", "oversight"),
    },
    "policy": {
        "section": "Risks",
        "mapping": "recommendations",
        "patterns": ("policy", "standard", "framework"),
    },
}


@dataclass(frozen=True)
class MinedArtefact:
    title: str
    artefact_type: str
    source: str
    confidence: str
    import_recommendation: str
    executive_state_mapping: str
    section: str


@dataclass(frozen=True)
class MiningReport:
    root: str
    artefacts: list[MinedArtefact]
    discarded_technical_debt: list[str]
    recommended_imports: list[MinedArtefact]
    import_summary: list[str]


def build_knowledge_mining_report(legacy_root: Path | None = None) -> MiningReport:
    root = legacy_root or DEFAULT_LEGACY_ROOT
    if not root.exists():
        return MiningReport(
            root=str(root),
            artefacts=[],
            discarded_technical_debt=[f"Legacy root not found: {root}"],
            recommended_imports=[],
            import_summary=[f"No mining performed because the target root does not exist: {root}."],
        )

    artefacts: list[MinedArtefact] = []
    discarded: list[str] = []

    for path in sorted(_iter_candidate_files(root)):
        if _is_technical_debt(path):
            discarded.append(str(path.relative_to(root)))
            continue

        text = _read_text(path)
        if not text:
            continue

        artefacts.extend(_extract_artefacts(root, path, text))

    artefacts = _dedupe_artefacts(artefacts)
    recommended = [artefact for artefact in artefacts if artefact.import_recommendation in {"IMPORT", "REVIEW"}][:25]
    summary = _build_summary(root, artefacts, discarded, recommended)

    return MiningReport(
        root=str(root),
        artefacts=artefacts,
        discarded_technical_debt=sorted(discarded),
        recommended_imports=recommended,
        import_summary=summary,
    )


def render_knowledge_mining_report(report: MiningReport) -> str:
    parts = [
        "# Executive Knowledge Inventory",
        "",
        f"- Target Root: {report.root}",
        "",
    ]
    for section in EXECUTIVE_SECTIONS[:-2]:
        parts.extend([f"## {section}", ""])
        if section == "Discarded Technical Debt":
            parts.extend(_render_bullets(report.discarded_technical_debt))
            parts.append("")
            continue
        if section == "Recommended Imports":
            parts.extend(_render_artefacts(report.recommended_imports))
            parts.append("")
            continue
        section_items = [artefact for artefact in report.artefacts if artefact.section == section]
        parts.extend(_render_artefacts(section_items))
        parts.append("")

    parts.extend(["## Discarded Technical Debt", ""])
    parts.extend(_render_bullets(report.discarded_technical_debt))
    parts.extend(["", "## Import Summary", ""])
    parts.extend(_render_bullets(report.import_summary))
    parts.append("")
    return "\n".join(parts)


def _iter_candidate_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        yield path


def _is_technical_debt(path: Path) -> bool:
    lowered = str(path).lower()
    return any(pattern in lowered for pattern in IGNORE_FILE_PATTERNS)


def _read_text(path: Path) -> str:
    try:
        if path.suffix.lower() == ".json":
            parsed = json.loads(path.read_text(errors="ignore"))
            return json.dumps(parsed, indent=2, sort_keys=True)
        return path.read_text(errors="ignore")
    except Exception:
        return ""


def _extract_artefacts(root: Path, path: Path, text: str) -> list[MinedArtefact]:
    lowered = f"{path.name.lower()}\n{text.lower()}"
    artefacts: list[MinedArtefact] = []

    for artefact_type, rule in CATEGORY_RULES.items():
        if not any(pattern in lowered for pattern in rule["patterns"]):
            continue
        title = _derive_title(path, text, artefact_type)
        confidence = _derive_confidence(path, text, rule["patterns"])
        recommendation = _derive_recommendation(confidence, artefact_type)
        artefacts.append(
            MinedArtefact(
                title=title,
                artefact_type=artefact_type,
                source=str(path.relative_to(root)),
                confidence=confidence,
                import_recommendation=recommendation,
                executive_state_mapping=rule["mapping"],
                section=rule["section"],
            )
        )

    return artefacts


def _derive_title(path: Path, text: str, artefact_type: str) -> str:
    first_heading = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if first_heading:
        return first_heading.group(1).strip()
    name = path.stem.replace("_", " ").replace("-", " ").strip()
    if artefact_type == "dashboard" and "dashboard" not in name.lower():
        return f"{name} dashboard concept"
    return name


def _derive_confidence(path: Path, text: str, patterns: tuple[str, ...]) -> str:
    score = 0
    lowered_path = str(path).lower()
    lowered_text = text.lower()
    for pattern in patterns:
        if pattern in lowered_path:
            score += 2
        if pattern in lowered_text:
            score += 1
    if "# " in text:
        score += 1
    if "## " in text:
        score += 1
    if score >= 5:
        return "HIGH"
    if score >= 3:
        return "MEDIUM"
    return "LOW"


def _derive_recommendation(confidence: str, artefact_type: str) -> str:
    if confidence == "HIGH":
        return "IMPORT"
    if confidence == "MEDIUM":
        return "REVIEW"
    if artefact_type in {"dashboard", "relationship"}:
        return "REVIEW"
    return "DISCARD"


def _dedupe_artefacts(artefacts: list[MinedArtefact]) -> list[MinedArtefact]:
    deduped: list[MinedArtefact] = []
    seen = set()
    for artefact in sorted(artefacts, key=lambda item: (item.section, item.title.lower(), item.source)):
        key = (artefact.section, artefact.title.lower(), artefact.source)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(artefact)
    return deduped


def _build_summary(root: Path, artefacts: list[MinedArtefact], discarded: list[str], recommended: list[MinedArtefact]) -> list[str]:
    counts = {}
    for artefact in artefacts:
        counts[artefact.section] = counts.get(artefact.section, 0) + 1
    lines = [f"Target root scanned: {root}."]
    for section in (
        "Objectives",
        "Projects",
        "Companies",
        "People",
        "Decisions",
        "Open Loops",
        "Risks",
        "Relationships",
        "Dashboard Ideas",
    ):
        lines.append(f"{section}: {counts.get(section, 0)} artefacts.")
    lines.append(f"Recommended imports: {len(recommended)}.")
    lines.append(f"Discarded technical debt files: {len(discarded)}.")
    return lines


def _render_artefacts(artefacts: list[MinedArtefact]) -> list[str]:
    if not artefacts:
        return ["_None found._"]
    lines = []
    for artefact in artefacts:
        lines.append(
            f"- {artefact.title} | Type: {artefact.artefact_type} | Source: {artefact.source} | "
            f"Confidence: {artefact.confidence} | Import: {artefact.import_recommendation} | "
            f"ExecutiveState: {artefact.executive_state_mapping}"
        )
    return lines


def _render_bullets(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values] or ["_None found._"]
