from pathlib import Path
from executive.knowledge.vault import load_vault
from executive.knowledge.findings import Finding

VAULT_ROOT = Path.home() / "Documents" / "My Vault" / "My Vault"

def analyze(evidence_root):
    notes = load_vault(VAULT_ROOT)

    counts = {}
    for note in notes:
        counts[note.kind] = counts.get(note.kind, 0) + 1

    findings = []

    if counts.get("project", 0) == 0:
        findings.append(Finding(
            category="Knowledge",
            severity="HIGH",
            title="No projects detected in vault",
            evidence="The vault scan did not classify any project notes.",
            recommendation="Review project folder naming or classification rules.",
        ))

    if counts.get("objective", 0) == 0:
        findings.append(Finding(
            category="Knowledge",
            severity="HIGH",
            title="No objectives detected in vault",
            evidence="The vault scan did not classify any objective notes.",
            recommendation="Create or tag objective notes so Alfred can track strategic drift.",
        ))

    return {
        "vault": {
            "note_count": len(notes),
            "kind_counts": counts,
            "findings": findings,
        }
    }
