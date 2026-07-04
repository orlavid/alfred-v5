from pathlib import Path
from dataclasses import dataclass

from src.knowledge.executive_understanding import classify_executive_note

@dataclass
class VaultNote:
    path: str
    title: str
    folder: str
    text: str
    kind: str

def classify(path: Path, text: str = ""):
    result = classify_executive_note(path, text)
    return result.entity_type if result.entity_type != "note" else "note"

def load_vault(vault_root: Path):
    notes = []

    for path in vault_root.rglob("*.md"):
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue

        rel = path.relative_to(vault_root)

        notes.append(
            VaultNote(
                path=str(rel),
                title=path.stem,
                folder=rel.parts[0] if rel.parts else "",
                text=text,
                kind=classify(path, text),
            )
        )

    return notes
