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
    if "project intelligence" in p:
        return "report"
    if "historical capture" in p:
        return "capture"
    if "capture -" in p:
        return "capture"
    if "briefing" in p or "executive review" in p or "board pack" in p:
        return "executive_briefing"
    if "meeting" in p or "minutes" in p or "agenda" in p:
        return "meeting"
    if "03 projects" in p:
        return "project"
    if "project" in p:
        return "project"
    if "people" in p or "02 people" in p:
        return "person"
    if "compan" in p or "supplier" in p or "04 companies" in p:
        return "company"
    if "risk" in p or "issue" in p or "escalation" in p:
        return "risk"
    if "decision intelligence" in p:
        return "report"
    if "04 decisions" in p:
        return "decision"
    if "decision" in p:
        return "decision"
    if "policy" in p or "framework" in p or "standard" in p:
        return "policy"
    if "open loop" in p or "open loops" in p:
        return "open_loop"
    if "follow" in p:
        return "follow_up"
    if "objective intelligence" in p:
        return "report"
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
