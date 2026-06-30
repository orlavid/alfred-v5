"""Evidence loading for the Alfred Engineering Handbook Generator."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

TEXT_EXTENSIONS = {".txt", ".md", ".py", ".sh", ".json", ".yml", ".yaml", ".service", ".timer"}


@dataclass(frozen=True)
class EvidenceFile:
    relative_path: str
    absolute_path: Path
    content: str
    size_bytes: int


class EvidenceLoader:
    def __init__(self, evidence_root: Path) -> None:
        self.evidence_root = evidence_root

    def load(self) -> Dict[str, EvidenceFile]:
        if not self.evidence_root.exists():
            raise FileNotFoundError(f"Evidence folder not found: {self.evidence_root}")

        evidence: Dict[str, EvidenceFile] = {}
        for path in self._iter_files(self.evidence_root):
            relative = path.relative_to(self.evidence_root).as_posix()
            evidence[relative] = EvidenceFile(
                relative_path=relative,
                absolute_path=path,
                content=path.read_text(errors="ignore"),
                size_bytes=path.stat().st_size,
            )
        return evidence

    def _iter_files(self, root: Path) -> Iterable[Path]:
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
                yield path


def select(evidence: Dict[str, EvidenceFile], *paths: str, limit: int = 60000) -> str:
    blocks: List[str] = []
    for rel in paths:
        item = evidence.get(rel)
        if not item:
            blocks.append(f"## {rel}\n\n_Evidence file not found._")
        else:
            blocks.append(f"## {rel}\n\n```text\n{item.content[:limit]}\n```")
    return "\n\n".join(blocks)
