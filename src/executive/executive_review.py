from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class HealthSection:
    name: str
    status: str
    evidence: List[str]
    risks: List[str]
    actions: List[str]


class ExecutiveReview:
    def __init__(self, evidence_root: Path):
        self.evidence_root = evidence_root

    def build(self) -> Dict[str, object]:
        sections = [
            self.platform(),
            self.telegram(),
            self.obsidian(),
            self.llamaindex(),
        ]
        return {
            "summary": self.summary(sections),
            "sections": sections,
            "risks": self.risks(sections),
            "recommendations": self.recommendations(sections),
        }

    def summary(self, sections: List[HealthSection]) -> List[str]:
        red = [s.name for s in sections if s.status == "RED"]
        amber = [s.name for s in sections if s.status == "AMBER"]
        if red:
            return [f"RED: {', '.join(red)} require immediate attention."]
        if amber:
            return [f"AMBER: {', '.join(amber)} require review."]
        return ["GREEN: Recovery Point Alpha evidence indicates core platform components are available."]

    def platform(self) -> HealthSection:
        services = self._read("system/services.txt")
        ports = self._read("system/listening_ports.txt")
        evidence = []
        risks = []
        actions = []

        if "hermes-telegram.service" in services:
            evidence.append("hermes-telegram.service appears in service inventory.")
        else:
            risks.append("Telegram service not found in service inventory.")
            actions.append("Verify systemd service installation.")

        if "127.0.0.1:8788" in ports or ":8788" in ports:
            evidence.append("LlamaIndex/API listener evidence found on port 8788.")
        else:
            risks.append("No listener evidence found for port 8788.")
            actions.append("Verify LlamaIndex API listener.")

        status = self._status(risks)
        return HealthSection("Platform", status, evidence, risks, actions)

    def telegram(self) -> HealthSection:
        status_text = self._read("telegram/status.txt")
        service_text = self._read("telegram/service.txt")
        evidence = []
        risks = []
        actions = []

        if "active (running)" in status_text:
            evidence.append("Telegram service status shows active running.")
        else:
            risks.append("Telegram service status does not show active running.")
            actions.append("Run systemctl status hermes-telegram.service.")

        if "hermes-agent-mctr-hermes-agent-1" in service_text:
            evidence.append("Telegram service uses restored Hermes container override.")
        else:
            risks.append("Telegram container override not evidenced in service definition.")
            actions.append("Check hermes-telegram.service overrides.")

        return HealthSection("Telegram", self._status(risks), evidence, risks, actions)

    def obsidian(self) -> HealthSection:
        vault = self._read("obsidian/vault_summary.txt")
        evidence = []
        risks = []
        actions = []

        if "markdown count" in vault.lower() or ".md" in vault:
            evidence.append("Vault summary includes markdown inventory evidence.")
        else:
            risks.append("Vault markdown inventory evidence not found.")
            actions.append("Re-run vault inventory collector.")

        if "/docker/obsidian-vault" in vault:
            evidence.append("Vault path is recorded as /docker/obsidian-vault.")
        else:
            risks.append("Canonical vault path not present in vault summary.")
            actions.append("Verify evidence collector used the live VPS vault path.")

        return HealthSection("Obsidian", self._status(risks), evidence, risks, actions)

    def llamaindex(self) -> HealthSection:
        index = self._read("llamaindex/index_summary.txt")
        evidence = []
        risks = []
        actions = []

        if "index" in index.lower():
            evidence.append("LlamaIndex summary evidence is present.")
        else:
            risks.append("LlamaIndex index evidence not found.")
            actions.append("Verify index folder and collector output.")

        if "requirements" in index.lower():
            evidence.append("LlamaIndex requirements evidence is present.")
        else:
            risks.append("LlamaIndex dependency evidence not present.")
            actions.append("Capture requirements and runtime metadata.")

        return HealthSection("LlamaIndex", self._status(risks), evidence, risks, actions)

    def risks(self, sections: List[HealthSection]) -> List[str]:
        out: List[str] = []
        for section in sections:
            out.extend(f"{section.name}: {risk}" for risk in section.risks)
        return out or ["No RED/AMBER risks detected from available evidence."]

    def recommendations(self, sections: List[HealthSection]) -> List[str]:
        out: List[str] = []
        for section in sections:
            out.extend(f"{section.name}: {action}" for action in section.actions)
        out.append("Next: replace platform-health evidence review with executive-domain review over daily logs, follow-ups, meetings, objectives and open loops.")
        return out

    def _status(self, risks: List[str]) -> str:
        return "AMBER" if risks else "GREEN"

    def _read(self, rel: str) -> str:
        path = self.evidence_root / rel
        if not path.exists():
            return ""
        return path.read_text(errors="ignore")
