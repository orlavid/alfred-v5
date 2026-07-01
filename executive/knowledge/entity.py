from dataclasses import dataclass, field

@dataclass
class VaultEntity:
    id: str
    type: str
    title: str
    path: str
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    relationships: list[dict] = field(default_factory=list)
