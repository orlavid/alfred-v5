from pathlib import Path
from dataclasses import dataclass

@dataclass
class VaultNote:
    path: str
    title: str
    folder: str
    text: str
    kind: str

def classify(path: Path):
    p = str(path).lower()

    if "daily" in p or "01 daily logs" in p:
        return "daily_log"
    if "project" in p or "03 projects" in p:
        return "project"
    if "people" in p or "02 people" in p:
        return "person"
    if "compan" in p or "supplier" in p or "04 companies" in p:
        return "company"
    if "decision" in p or "04 decisions" in p:
        return "decision"
    if "open loop" in p or "open loops" in p:
        return "open_loop"
    if "follow" in p:
        return "follow_up"
    if "objective" in p:
        return "objective"

    return "note"

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
                kind=classify(path),
            )
        )

    return notes
