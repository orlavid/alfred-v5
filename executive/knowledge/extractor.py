import re
from executive.knowledge.entity import VaultEntity
from executive.knowledge.vault import load_vault
from src.knowledge.executive_understanding import classify_executive_note, extract_aliases

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9_/-]+)")

def extract_links(text):
    links = []
    for match in WIKILINK_RE.findall(text):
        links.append(match.split("|")[0].strip())
    return links

def extract_tags(text):
    return sorted(set(TAG_RE.findall(text)))

def extract_entities(vault_root):
    notes = load_vault(vault_root)
    entities = []

    for note in notes:
        understanding = classify_executive_note(note.path, note.text)
        entities.append(
            VaultEntity(
                id=note.path,
                type=understanding.entity_type if understanding.entity_type != "note" else note.kind,
                title=note.title,
                path=note.path,
                aliases=extract_aliases(understanding.frontmatter),
                tags=extract_tags(note.text),
                links=extract_links(note.text),
            )
        )

    return entities
