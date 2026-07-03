from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


SUPPORTED_EXTENSIONS = {".txt", ".md", ".json", ".py", ".sh", ".yml", ".yaml"}


@dataclass(frozen=True)
class EvidenceHit:
    path: str
    score: int
    snippet: str


@dataclass(frozen=True)
class MeetingBrief:
    query: str
    hits: List[EvidenceHit]
    risks: List[str]
    questions: List[str]
    recommendations: List[str]


class MeetingIntelligence:
    def __init__(self, evidence_root: Path) -> None:
        self.evidence_root = evidence_root

    def build(self, query: str, limit: int = 12) -> MeetingBrief:
        cleaned = query.strip()
        if not cleaned:
            raise ValueError("Meeting query must not be empty.")

        hits = self.search(cleaned, limit=limit)
        return MeetingBrief(
            query=cleaned,
            hits=hits,
            risks=self._risks(cleaned, hits),
            questions=self._questions(cleaned),
            recommendations=self._recommendations(hits),
        )

    def search(self, query: str, limit: int = 12) -> List[EvidenceHit]:
        terms = self._terms(query)
        hits: List[EvidenceHit] = []

        for path in self._files():
            text = self._read(path)
            score = self._score(path, text, terms)
            if score <= 0:
                continue
            hits.append(
                EvidenceHit(
                    path=path.relative_to(self.evidence_root).as_posix(),
                    score=score,
                    snippet=self._snippet(text, terms),
                )
            )

        hits.sort(key=lambda hit: (-hit.score, hit.path))
        return hits[:limit]

    def render_markdown(self, brief: MeetingBrief) -> str:
        lines: List[str] = [
            "# Meeting Brief",
            "",
            "## Query",
            "",
            brief.query,
            "",
            "## Executive Summary",
            "",
        ]

        if brief.hits:
            lines.append(f"Found {len(brief.hits)} evidence item(s) relevant to `{brief.query}`.")
        else:
            lines.append("No directly relevant evidence was found in the current evidence pack.")

        lines.extend(["", "## Evidence", ""])

        if brief.hits:
            for hit in brief.hits:
                lines.extend([
                    f"### {hit.path}",
                    "",
                    f"Score: {hit.score}",
                    "",
                    "```text",
                    hit.snippet,
                    "```",
                    "",
                ])
        else:
            lines.extend(["_No evidence found._", ""])

        lines.extend(["## Risks", "", self._bullets(brief.risks), ""])
        lines.extend(["## Recommended Questions", "", self._bullets(brief.questions), ""])
        lines.extend(["## Recommended Actions", "", self._bullets(brief.recommendations), ""])
        return "\n".join(lines).strip() + "\n"

    def _files(self) -> Iterable[Path]:
        if not self.evidence_root.exists():
            return []
        return (
            path
            for path in sorted(self.evidence_root.rglob("*"))
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        )

    def _read(self, path: Path) -> str:
        return path.read_text(errors="ignore")

    def _terms(self, query: str) -> List[str]:
        return [term.lower() for term in query.replace("-", " ").split() if term.strip()]

    def _score(self, path: Path, text: str, terms: List[str]) -> int:
        haystack = f"{path.as_posix()}\n{text}".lower()
        score = 0
        for term in terms:
            score += haystack.count(term)
            if term in path.name.lower():
                score += 10
        return score

    def _snippet(self, text: str, terms: List[str], radius: int = 900) -> str:
        lowered = text.lower()
        positions = [lowered.find(term) for term in terms if lowered.find(term) >= 0]
        if not positions:
            return text[: radius * 2].strip()
        start = max(min(positions) - radius, 0)
        end = min(max(positions) + radius, len(text))
        return text[start:end].strip()

    def _risks(self, query: str, hits: List[EvidenceHit]) -> List[str]:
        if not hits:
            return [f"No evidence found for `{query}`; briefing confidence is low."]
        if len(hits) < 3:
            return ["Limited evidence found; validate manually before relying on the brief."]
        return ["No immediate evidence-volume risk detected."]

    def _questions(self, query: str) -> List[str]:
        return [
            f"What has changed recently regarding {query}?",
            "What decision, commitment, or follow-up is needed from this meeting?",
            "Are there unresolved risks, owners, or dependencies?",
            "What outcome should be captured in Obsidian after the meeting?",
        ]

