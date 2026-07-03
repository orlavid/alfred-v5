"""Read-only archaeology report builder for legacy Alfred environments."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json

from src.mining.knowledge_miner import (
    _derive_confidence,
    _derive_title,
    _iter_candidate_files,
    _read_text,
    build_knowledge_mining_report,
)

DEFAULT_ARCHAEOLOGY_SOURCE = Path("/root/legacy-alfred")

SECTION_HEADINGS = [
    "Executive Summary",
    "Objectives",
    "Projects",
    "Companies",
    "People",
    "Decisions",
    "Governance",
    "Risks",
    "Open Loops",
    "Dashboard Ideas",
    "Import Summary",
]

ARCHAEOLOGY_RULES = {
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
    "governance": {
        "section": "Governance",
        "mapping": "recommendations",
        "patterns": ("governance", "committee", "oversight", "policy", "standard", "framework"),
    },
    "risk": {
        "section": "Risks",
        "mapping": "risks",
        "patterns": ("risk", "issue", "concern", "escalation"),
    },
    "open_loop": {
        "section": "Open Loops",
        "mapping": "open_loops",
        "patterns": ("open loop", "blocked", "waiting", "pending"),
    },
    "dashboard": {
        "section": "Dashboard Ideas",
        "mapping": "recommendations",
        "patterns": ("dashboard", "kpi", "scorecard", "heatmap"),
    },
}


@dataclass(frozen=True)
class ArchaeologyFinding:
    title: str
    finding_type: str
    section: str
    source: str
    confidence: str
    classification: str
    reason: str
    suggested_mapping: str


@dataclass(frozen=True)
class ArchaeologyReport:
    source_root: str
    findings: list[ArchaeologyFinding]
    import_candidates: list[ArchaeologyFinding]
    discarded_technical_debt: list[str]
    executive_summary: list[str]
    import_summary: list[str]


def build_archaeology_report(source_root: Path | None = None) -> ArchaeologyReport:
    root = source_root or DEFAULT_ARCHAEOLOGY_SOURCE
    mining_report = build_knowledge_mining_report(root)

    if not root.exists():
        summary = [
            f"No archaeology performed because the configured source path does not exist: {root}.",
            "Safe default mode preserved read-only execution without requiring access to the old VPS path.",
        ]
        return ArchaeologyReport(
            source_root=str(root),
            findings=[],
            import_candidates=[],
            discarded_technical_debt=mining_report.discarded_technical_debt,
            executive_summary=summary,
            import_summary=mining_report.import_summary,
        )

    findings = _build_findings(root)
    import_candidates = [
        finding
        for finding in findings
        if finding.classification in {"Import", "Review"}
    ]
    summary = _build_summary(root, findings, mining_report.discarded_technical_debt)

    return ArchaeologyReport(
        source_root=str(root),
        findings=findings,
        import_candidates=import_candidates,
        discarded_technical_debt=mining_report.discarded_technical_debt,
        executive_summary=summary,
        import_summary=_build_import_summary(findings, mining_report.discarded_technical_debt),
    )


def render_archaeology_report(report: ArchaeologyReport) -> str:
    parts = [
        "# Alfred Archaeology Report",
        "",
        f"- Source Root: {report.source_root}",
        "",
        "## Executive Summary",
        "",
    ]
    parts.extend(_render_bullets(report.executive_summary))
    for section in SECTION_HEADINGS[1:-1]:
        parts.extend(["", f"## {section}", ""])
        section_items = [finding for finding in report.findings if finding.section == section]
        parts.extend(_render_findings(section_items))
    parts.extend(["", "## Import Summary", ""])
    parts.extend(_render_bullets(report.import_summary))
    parts.append("")
    return "\n".join(parts)


def render_import_candidates_json(report: ArchaeologyReport) -> str:
    payload = {
        "source_root": report.source_root,
        "import_candidates": [asdict(finding) for finding in report.import_candidates],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def _build_findings(root: Path) -> list[ArchaeologyFinding]:
    findings: list[ArchaeologyFinding] = []
    seen = set()

    for path in sorted(_iter_candidate_files(root)):
        text = _read_text(path)
        if not text:
            continue

        lowered = f"{path.name.lower()}\n{text.lower()}"
        for finding_type, rule in ARCHAEOLOGY_RULES.items():
            if not any(pattern in lowered for pattern in rule["patterns"]):
                continue
            title = _derive_title(path, text, finding_type)
            confidence = _derive_confidence(path, text, rule["patterns"])
            classification, reason = _classify_finding(path, text, finding_type, confidence)
            finding = ArchaeologyFinding(
                title=title,
                finding_type=finding_type,
                section=rule["section"],
                source=str(path.relative_to(root)),
                confidence=confidence,
                classification=classification,
                reason=reason,
                suggested_mapping=rule["mapping"],
            )
            key = (finding.section, finding.title.lower(), finding.source, finding.finding_type)
            if key in seen:
                continue
            seen.add(key)
            findings.append(finding)

    findings.sort(key=lambda item: (item.section, item.title.lower(), item.source, item.finding_type))
    return findings


def _classify_finding(path: Path, text: str, finding_type: str, confidence: str) -> tuple[str, str]:
    lowered = f"{path.name.lower()}\n{text.lower()}"

    if any(marker in lowered for marker in ("archive", "archived", "obsolete", "deprecated", "historical", "legacy", "superseded")):
        return "Archive", "The content appears historical or explicitly archived."
    if confidence == "HIGH":
        return "Import", "The file contains strong executive signals and clear category matches."
    if confidence == "MEDIUM":
        return "Review", "The file contains plausible executive content but needs human review before import."
    if finding_type in {"governance", "dashboard", "decision"}:
        return "Review", "The content may be useful but the evidence is weak, so manual review is safer than direct import."
    return "Discard", "The evidence is too weak or generic to justify import in phase 1."


def _build_summary(root: Path, findings: list[ArchaeologyFinding], discarded_technical_debt: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    classifications: dict[str, int] = {}
    for finding in findings:
        counts[finding.section] = counts.get(finding.section, 0) + 1
        classifications[finding.classification] = classifications.get(finding.classification, 0) + 1
    return [
        f"Archaeology source scanned read-only: {root}.",
        "Findings by classification: "
        f"Import {classifications.get('Import', 0)}, Review {classifications.get('Review', 0)}, "
        f"Archive {classifications.get('Archive', 0)}, Discard {classifications.get('Discard', 0)}.",
        "Executive artefacts found: "
        + ", ".join(
            f"{section} {counts.get(section, 0)}"
            for section in (
                "Objectives",
                "Projects",
                "Companies",
                "People",
                "Decisions",
                "Governance",
                "Risks",
                "Open Loops",
                "Dashboard Ideas",
            )
        )
        + ".",
        f"Discarded technical debt files inherited from the base miner: {len(discarded_technical_debt)}.",
    ]


def _build_import_summary(findings: list[ArchaeologyFinding], discarded_technical_debt: list[str]) -> list[str]:
    imports = [finding for finding in findings if finding.classification == "Import"]
    reviews = [finding for finding in findings if finding.classification == "Review"]
    archives = [finding for finding in findings if finding.classification == "Archive"]
    discards = [finding for finding in findings if finding.classification == "Discard"]
    return [
        f"Import candidates: {len(imports)}.",
        f"Review candidates: {len(reviews)}.",
        f"Archive candidates: {len(archives)}.",
        f"Discarded findings: {len(discards)}.",
        f"Technical debt files ignored by the base miner: {len(discarded_technical_debt)}.",
    ]


def _render_findings(findings: list[ArchaeologyFinding]) -> list[str]:
    if not findings:
        return ["_None found._"]
    return [
        f"- {finding.title} | Type: {finding.finding_type} | Source: {finding.source} | "
        f"Classification: {finding.classification} | Confidence: {finding.confidence} | "
        f"Reason: {finding.reason} | ExecutiveState: {finding.suggested_mapping}"
        for finding in findings
    ]


def _render_bullets(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values] or ["_None found._"]
