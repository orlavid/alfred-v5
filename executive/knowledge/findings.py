from dataclasses import dataclass

@dataclass
class Finding:
    category: str
    severity: str
    title: str
    evidence: str
    recommendation: str
