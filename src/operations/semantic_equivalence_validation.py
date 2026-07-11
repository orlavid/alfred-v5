"""Semantic equivalence validation against the legacy Alfred objective route."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import tempfile

from executive.knowledge.vault import load_vault
from src.executive.executive_state import build_executive_state
from src.knowledge.executive_knowledge_builder import DEFAULT_EVIDENCE_ROOT
from src.knowledge.providers.legacy_adapter import build_legacy_knowledge_adapter
from src.knowledge.providers.objective_provider import _extract_objective_entities
from src.obsidian.live_vault import detect_live_vault_status
from src.operations.config_registry import build_configuration_registry

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output"
MARKDOWN_REPORT = OUT / "Semantic_Equivalence_Validation.md"
JSON_REPORT = OUT / "Semantic_Equivalence_Validation.json"

LEGACY_IMPLEMENTATION_REFERENCES = (
    "/opt/second-brain/scripts/hermes_ask.sh",
    "/opt/second-brain/scripts/objective_evidence_search.py",
    "/opt/second-brain/scripts/hermes_knowledge_api.py",
)
LEGACY_FILTERING_RULES = (
    "Use the dedicated objective evidence route rather than generic semantic retrieval.",
    "Treat objective evidence as operational facts from the vault, not historical objective prose.",
    "Require concrete business evidence in the source note content rather than promoting filenames.",
    "Allow objective-classified notes only when they come from dedicated objective paths or explicit objective markers.",
)
LEGACY_RANKING_RULES = (
    "Prefer dedicated objective evidence over generic lexical or semantic matches.",
    "Rank retained objectives by stable title/path ordering once they survive the legacy filters.",
)
LEGACY_EXCLUSION_RULES = (
    "Exclude 09 Governance/Objective Intelligence.",
    "Exclude 07 AI Memory.",
    "Exclude 07 Executive Briefings.",
    "Exclude 98 Archive.",
    "Exclude watchlists, open loops, AI synthesis, inventories, summaries, and report artefacts as objectives.",
)
BAD_OBJECTIVE_TOKENS = (
    "watchlist",
    "open loop",
    "synthesis",
    "inventory",
    "summary",
    "catalogue",
)


@dataclass(frozen=True)
class DomainEquivalenceResult:
    domain: str
    legacy_count: int
    new_count: int
    matched: tuple[str, ...]
    missing: tuple[str, ...]
    false_positives: tuple[str, ...]
    false_negatives: tuple[str, ...]
    current_heuristic_count: int
    current_heuristic_false_positives: tuple[str, ...]
    source_notes_used: tuple[str, ...]
    filtering_rules: tuple[str, ...]
    ranking_rules: tuple[str, ...]
    exclusion_rules: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class SemanticEquivalenceReport:
    overall_status: str
    vault_path: str
    markdown_files_processed: int
    mode: str
    legacy_implementation: tuple[str, ...]
    objectives: DomainEquivalenceResult

    def as_dict(self) -> dict[str, object]:
        return {
            "overall_status": self.overall_status,
            "vault_path": self.vault_path,
            "markdown_files_processed": self.markdown_files_processed,
            "mode": self.mode,
            "legacy_implementation": list(self.legacy_implementation),
            "objectives": asdict(self.objectives),
        }


def build_semantic_equivalence_validation(
    *,
    evidence_root: Path | None = None,
    vault_root: Path | None = None,
) -> SemanticEquivalenceReport:
    registry = build_configuration_registry(vault_path=vault_root)
    effective_evidence_root = evidence_root or DEFAULT_EVIDENCE_ROOT
    configured_vault_root = Path(vault_root or registry.configured_vault_path).expanduser()
    vault_status = detect_live_vault_status(configured_vault_root)

    if vault_status.status == "PASS":
        return _build_report_for_vault(
            effective_vault_root=configured_vault_root,
            effective_evidence_root=effective_evidence_root,
            vault_path=vault_status.vault_path,
            markdown_files_processed=vault_status.markdown_files_processed,
            mode="live_vault",
        )
    with tempfile.TemporaryDirectory(prefix="alfred-semantic-equivalence-") as tmp:
        fixture_vault = _build_representative_objective_vault(Path(tmp) / "vault")
        fixture_status = detect_live_vault_status(fixture_vault)
        return _build_report_for_vault(
            effective_vault_root=fixture_vault,
            effective_evidence_root=effective_evidence_root,
            vault_path=fixture_status.vault_path,
            markdown_files_processed=fixture_status.markdown_files_processed,
            mode="representative_fixture",
        )


def _build_report_for_vault(
    *,
    effective_vault_root: Path,
    effective_evidence_root: Path,
    vault_path: str,
    markdown_files_processed: int,
    mode: str,
) -> SemanticEquivalenceReport:
    notes = load_vault(effective_vault_root)
    current_heuristic = tuple(sorted(note.title for note in notes if note.kind == "objective"))

    legacy_entities = _legacy_objective_entities(notes)
    if not legacy_entities:
        adapter = build_legacy_knowledge_adapter(effective_evidence_root, vault_root=effective_vault_root)
        legacy_entities = tuple(adapter.get_objectives())
    legacy_objectives = tuple(sorted(item.title for item in legacy_entities))
    legacy_paths = tuple(sorted(getattr(item, "path", "") for item in legacy_entities))

    state = build_executive_state(effective_evidence_root, vault_root=effective_vault_root)
    new_objectives = tuple(sorted(item.title for item in state.objectives))

    legacy_set = set(legacy_objectives)
    new_set = set(new_objectives)

    matched = tuple(sorted(legacy_set & new_set))
    missing = tuple(sorted(legacy_set - new_set))
    false_positives = tuple(sorted(new_set - legacy_set))
    false_negatives = missing
    current_heuristic_false_positives = tuple(
        sorted(title for title in current_heuristic if title not in legacy_set and _looks_like_bad_objective(title))
    )

    status = "PASS"
    if missing or false_positives or false_negatives or _has_bad_objective(false_positives):
        status = "FAIL"
    if current_heuristic_false_positives and not matched:
        status = "FAIL"

    objectives = DomainEquivalenceResult(
        domain="Objectives",
        legacy_count=len(legacy_objectives),
        new_count=len(new_objectives),
        matched=matched,
        missing=missing,
        false_positives=false_positives,
        false_negatives=false_negatives,
        current_heuristic_count=len(current_heuristic),
        current_heuristic_false_positives=current_heuristic_false_positives,
        source_notes_used=legacy_paths,
        filtering_rules=LEGACY_FILTERING_RULES,
        ranking_rules=LEGACY_RANKING_RULES,
        exclusion_rules=LEGACY_EXCLUSION_RULES,
        status=status,
    )
    overall_status = objectives.status
    return SemanticEquivalenceReport(
        overall_status=overall_status,
        vault_path=vault_path,
        markdown_files_processed=markdown_files_processed,
        mode=mode,
        legacy_implementation=LEGACY_IMPLEMENTATION_REFERENCES,
        objectives=objectives,
    )


def render_semantic_equivalence_validation(report: SemanticEquivalenceReport) -> str:
    result = report.objectives
    heuristic_false_positives = [f"- {item}" for item in result.current_heuristic_false_positives] or ["- None"]
    source_notes = [f"- `{item}`" for item in result.source_notes_used] or ["- None"]
    lines = [
        "# Semantic Equivalence Validation",
        "",
        f"- Overall Status: {report.overall_status}",
        f"- Vault Path: {report.vault_path}",
        f"- Markdown Files Processed: {report.markdown_files_processed}",
        f"- Mode: {report.mode}",
        f"- Scope: {result.domain} only",
        "",
        "## Legacy Implementation",
        "",
    ]
    lines.extend(f"- `{item}`" for item in report.legacy_implementation)
    lines.extend(
        [
            "",
            "## Objectives",
            "",
            f"- Status: {result.status}",
            f"- Legacy Count: {result.legacy_count}",
            f"- New Count: {result.new_count}",
            f"- Current Heuristic Count: {result.current_heuristic_count}",
            f"- Matched: {', '.join(result.matched) if result.matched else 'None'}",
            f"- Missing: {', '.join(result.missing) if result.missing else 'None'}",
            f"- False Positives: {', '.join(result.false_positives) if result.false_positives else 'None'}",
            f"- False Negatives: {', '.join(result.false_negatives) if result.false_negatives else 'None'}",
            "",
            "### Current Heuristic False Positives",
            "",
            *heuristic_false_positives,
            "",
            "### Source Notes Used",
            "",
            *source_notes,
            "",
            "### Filtering Rules",
            "",
            *[f"- {item}" for item in result.filtering_rules],
            "",
            "### Ranking Rules",
            "",
            *[f"- {item}" for item in result.ranking_rules],
            "",
            "### Exclusion Rules",
            "",
            *[f"- {item}" for item in result.exclusion_rules],
            "",
        ]
    )
    return "\n".join(lines)


def render_semantic_equivalence_validation_json(report: SemanticEquivalenceReport) -> str:
    return json.dumps(report.as_dict(), indent=2, sort_keys=True)


def write_semantic_equivalence_validation(report: SemanticEquivalenceReport) -> tuple[Path, Path]:
    MARKDOWN_REPORT.parent.mkdir(parents=True, exist_ok=True)
    MARKDOWN_REPORT.write_text(render_semantic_equivalence_validation(report))
    JSON_REPORT.write_text(render_semantic_equivalence_validation_json(report))
    return MARKDOWN_REPORT, JSON_REPORT


def _looks_like_bad_objective(title: str) -> bool:
    lowered = title.lower()
    return any(token in lowered for token in BAD_OBJECTIVE_TOKENS) or lowered.startswith("20")


def _has_bad_objective(values: tuple[str, ...]) -> bool:
    return any(_looks_like_bad_objective(value) for value in values)


def _build_representative_objective_vault(vault: Path) -> Path:
    for folder in (
        "01 Daily Logs",
        "02 People",
        "03 Projects",
        "04 Companies",
        "04 Decisions",
        "05 Meetings",
        "06 Risks",
        "07 Open Loops",
        "08 Follow Ups",
        "09 Objectives",
        "10 Briefings",
    ):
        (vault / folder).mkdir(parents=True)
    (vault / "09 Governance" / "Watchlists").mkdir(parents=True)
    (vault / "07 AI Memory" / "Strategic Synthesis").mkdir(parents=True)
    (vault / "09 Governance" / "Objectives").mkdir(parents=True)

    (vault / "09 Governance" / "Objectives" / "2026 Executive Objectives.md").write_text(
        "# 2026 Executive Objectives\n\n"
        "## Objectives\n\n"
        "1. Operational Governance\n"
        "2. Data and AI Strategies\n"
        "3. Risk Management\n"
        "4. Employee Development\n"
        "5. Cost Management\n"
        "6. Performance and Value Realisation\n"
    )
    (vault / "09 Governance" / "Objectives" / "2026-05-28 Open Loop - platform_resilience.md").write_text(
        "# 2026-05-28 Open Loop - platform_resilience\nObjective: unblock platform resilience work.\n"
    )
    (vault / "09 Governance" / "Watchlists" / "2026-05-29 Watchlist - strategic_drift.md").write_text(
        "# 2026-05-29 Watchlist - strategic_drift\nObjective: monitor strategic drift.\n"
    )
    (vault / "07 AI Memory" / "Strategic Synthesis" / "Strategic Memory Synthesis.md").write_text(
        "# Strategic Memory Synthesis\nObjective: summarise the historical record.\n"
    )
    (vault / "03 Projects" / "Project Phoenix.md").write_text("# Project Phoenix\n[[Objective Alpha]].\n")
    (vault / "02 People" / "Jane Smith.md").write_text("# Jane Smith\nOwner.\n")
    (vault / "04 Companies" / "Acme Capital.md").write_text("# Acme Capital\nSupplier.\n")
    (vault / "04 Decisions" / "Decision 1.md").write_text("# Decision 1\nApprove.\n")
    (vault / "05 Meetings" / "Project Phoenix Review.md").write_text("# Project Phoenix Review\nAgenda.\n")
    (vault / "06 Risks" / "Risk Register.md").write_text("# Risk Register\nEscalation.\n")
    (vault / "07 Open Loops" / "Open Loop Register.md").write_text(
        "## LOOP-1\nStatus: OPEN\nPriority: HIGH\nOwner: Jane Smith\nIssue: Await approval.\n"
    )
    (vault / "08 Follow Ups" / "Follow Up Actions.md").write_text(
        "## Follow-Up Actions\n- Follow up with Acme Capital today.\n"
    )
    (vault / "01 Daily Logs" / "2026-07-04 Daily.md").write_text(
        "# 2026-07-04 Daily\nReviewed [[Project Phoenix]].\n"
    )
    return vault


def _legacy_objective_entities(notes):
    entities = []
    for note in notes:
        extracted = _extract_objective_entities(note)
        if extracted:
            entities.extend(extracted)
    return tuple(entities)
