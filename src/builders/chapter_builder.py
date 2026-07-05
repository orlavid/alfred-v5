"""Build structured handbook chapters from collected evidence."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, List

from .loader import EvidenceFile


class ChapterBuilder:
    """Turn raw Alfred evidence into an engineer-readable handbook."""

    def __init__(self, evidence: Dict[str, EvidenceFile]) -> None:
        self.evidence = evidence

    def build(self) -> Dict[str, str]:
        return {
            "01-executive-summary.md": self._executive_summary(),
            "02-system-platform.md": self._component_chapter(
                title="System Platform",
                purpose="Defines the VPS operating environment that hosts Alfred.",
                responsibilities=[
                    "Run Alfred services and timers.",
                    "Provide network, Docker, Python and systemd runtime support.",
                    "Expose required local ports for Cloudflare and internal services.",
                ],
                inputs=["Systemd services", "Timers", "Cron", "Listening ports"],
                outputs=["Available runtime services", "Operational logs", "Health status"],
                dependencies=["Ubuntu/Linux", "systemd", "Python", "Docker", "cloudflared"],
                failure_modes=[
                    "Service stopped or disabled.",
                    "Wrong local port exposed.",
                    "Timer or cron job missing.",
                    "Disk space exhaustion.",
                ],
                recovery=[
                    "Check systemctl status for affected services.",
                    "Check listening ports with ss -ltnp.",
                    "Review journalctl logs.",
                    "Restore from Recovery Point Alpha if configuration drift is suspected.",
                ],
                evidence_paths=[
                    "system/services.txt",
                    "system/timers.txt",
                    "system/listening_ports.txt",
                    "system/cron.txt",
                ],
            ),
            "03-obsidian.md": self._component_chapter(
                title="Obsidian Knowledge Platform",
                purpose="Defines the live Obsidian vault as Alfred's authoritative source of truth.",
                responsibilities=[
                    "Store source notes, captures, daily logs, people, companies, projects and governance artefacts.",
                    "Remain human-readable and recoverable without Alfred.",
                    "Provide the evidence base for enrichment, routing and semantic retrieval.",
                ],
                inputs=["User notes", "Captures", "Daily logs", "Batch enrichments"],
                outputs=["Markdown evidence", "Source paths", "Knowledge graph substrate"],
                dependencies=["Obsidian Sync", "Markdown files", "Vault filesystem"],
                failure_modes=[
                    "Vault stale or not synced.",
                    "Wrong vault path indexed.",
                    "Derived artefacts mistaken for source truth.",
                ],
                recovery=[
                    "Verify `/docker/obsidian-vault` exists.",
                    "Check markdown count and recent files.",
                    "Confirm sync markers or recent expected notes.",
                    "Rebuild LlamaIndex from the live vault only.",
                ],
                evidence_paths=["obsidian/vault_summary.txt", "trees/vault.json"],
            ),
            "04-alfred-router.md": self._component_chapter(
                title="Alfred Router",
                purpose="Defines the orchestration and quality gate layer used by Telegram and deterministic workflows.",
                responsibilities=[
                    "Classify user intent.",
                    "Select the correct retrieval or deterministic strategy.",
                    "Execute protected routes.",
                    "Validate answers before returning them.",
                    "Withhold unsupported answers rather than hallucinate.",
                ],
                inputs=["User query", "Strategy definitions", "Hermes compatibility path", "Evidence policies"],
                outputs=["Validated answer", "Quality-gate rejection", "Audit trail"],
                dependencies=["alfred_router.sh", "alfred_router.py", "strategies.py", "validation.py", "hermes_ask.sh"],
                failure_modes=[
                    "Strategy returns non-zero exit code.",
                    "Answer is empty.",
                    "Container default points to stale runtime.",
                    "OpenRouter key unavailable for legacy path.",
                ],
                recovery=[
                    "Run alfred_router.sh directly with a known query.",
                    "Check strategies.py defaults.",
                    "Check hermes_ask.sh environment handling.",
                    "Confirm Telegram service environment matches working router configuration.",
                ],
                evidence_paths=[
                    "key_files/opt__second-brain__scripts__alfred_router.sh",
                    "key_files/opt__second-brain__retrieval__alfred_router.py",
                    "key_files/opt__second-brain__retrieval__strategies.py",
                    "key_files/opt__second-brain__scripts__hermes_ask.sh",
                ],
            ),
            "05-telegram.md": self._component_chapter(
                title="Telegram Interface",
                purpose="Defines Telegram as Alfred's mobile executive interface.",
                responsibilities=[
                    "Receive user messages.",
                    "Pass free-text queries to Alfred Router.",
                    "Return validated responses in manageable parts.",
                    "Preserve useful legacy deterministic routes.",
                ],
                inputs=["Telegram messages", "Bot token", "Router output"],
                outputs=["Telegram replies", "Parted long responses", "Operational logs"],
                dependencies=["hermes-telegram.service", "/root/hermes-telegram.py", "alfred_router.sh", "OpenRouter env for legacy synthesis"],
                failure_modes=[
                    "Service inactive.",
                    "Service override points to old container.",
                    "OpenRouter env file not loaded.",
                    "Router withholds answer due to strategy failure.",
                ],
                recovery=[
                    "Check hermes-telegram.service status.",
                    "Inspect systemctl cat hermes-telegram.service.",
                    "Check journalctl logs.",
                    "Run the same query through alfred_router.sh manually.",
                ],
                evidence_paths=["telegram/service.txt", "telegram/status.txt", "telegram/script.py"],
            ),
            "06-llamaindex.md": self._component_chapter(
                title="LlamaIndex Evidence Engine",
                purpose="Defines semantic retrieval and ChatGPT Action evidence packaging.",
                responsibilities=[
                    "Index the live Obsidian vault.",
                    "Retrieve semantically relevant evidence.",
                    "Package evidence for ChatGPT reasoning.",
                    "Support the Custom GPT Action endpoint.",
                ],
                inputs=["/docker/obsidian-vault", "Embedding model", "User question"],
                outputs=["Evidence package", "Source paths", "Similarity-scored nodes"],
                dependencies=["FastAPI app", "alfred.py", "LlamaIndex index folder", "Python virtual environment"],
                failure_modes=[
                    "API not running.",
                    "Index stale or missing.",
                    "Evidence package returned but GPT instructions misaligned.",
                    "Subprocess output includes warnings before JSON.",
                ],
                recovery=[
                    "Run alfred.py directly with --json.",
                    "Test local API on 127.0.0.1:8788.",
                    "Rebuild index from the live vault if needed.",
                    "Confirm GPT Action instructions treat API output as evidence package.",
                ],
                evidence_paths=[
                    "llamaindex/index_summary.txt",
                    "key_files/opt__llamaindex-bakeoff__app.py",
                    "key_files/opt__llamaindex-bakeoff__alfred.py",
                    "key_files/opt__llamaindex-bakeoff__test_index.py",
                ],
            ),
            "07-docker-cloudflare.md": self._component_chapter(
                title="Docker and Cloudflare",
                purpose="Defines container/runtime exposure and public HTTPS routing.",
                responsibilities=[
                    "Provide any required container runtime compatibility.",
                    "Expose public Alfred endpoints through Cloudflare Tunnel.",
                    "Map hostnames to correct local ports.",
                ],
                inputs=["Docker containers", "Cloudflare tunnel config", "Local services"],
                outputs=["Public HTTPS endpoints", "Container runtime state"],
                dependencies=["Docker", "cloudflared", "Cloudflare ingress configuration"],
                failure_modes=[
                    "Cloudflare points to wrong local port.",
                    "Container name exists historically but is not valid for current path.",
                    "Service returns 502 because local target is not listening.",
                ],
                recovery=[
                    "Use ss -ltnp to confirm local listeners.",
                    "Check /etc/cloudflared/config.yml.",
                    "Restart cloudflared only after confirming local target.",
                    "Inspect containers before assuming they are current production runtime.",
                ],
                evidence_paths=["docker/containers.txt", "docker/images.txt", "cloudflare/config.yml"],
            ),
            "08-python-codebase.md": self._component_chapter(
                title="Python Codebase Catalogue",
                purpose="Summarises discovered Python modules, imports, functions and classes.",
                responsibilities=[
                    "Provide a searchable engineering inventory.",
                    "Support future architecture documentation generation.",
                    "Expose likely extension points without manual inspection.",
                ],
                inputs=["AST parser output", "Python source files"],
                outputs=["Module catalogue", "Function inventory", "Class inventory"],
                dependencies=["Python source code", "Evidence collector"],
                failure_modes=[
                    "Syntax warnings from source files.",
                    "Generated catalogue becomes stale if not regenerated after changes.",
                ],
                recovery=["Regenerate engineering evidence pack.", "Review parsing errors in catalogue output."],
                evidence_paths=[
                    "python/second_brain_python_inventory.json",
                    "python/alfred_v2_python_inventory.json",
                    "python/llamaindex_python_inventory.json",
                ],
            ),
            "09-build-and-recovery.md": self._build_and_recovery(),
        }

    def _header(self, title: str) -> str:
        return f"# {title}\n\nGenerated: {datetime.now().isoformat()}\n\n"

    def _executive_summary(self) -> str:
        return self._header("Executive Summary") + """
## Purpose

This handbook documents Alfred Executive Operating System at Recovery Point Alpha. It is generated from collected engineering evidence and is intended to support rebuild, recovery, extension and onboarding.

## System Role

Alfred is an evidence-first executive operating system. It combines a human-readable Obsidian vault, deterministic routing, semantic retrieval, background enrichment, Telegram access and ChatGPT reasoning.

## Core Architecture

```text
Obsidian Vault
    ↓
Hermes / Second Brain enrichment and deterministic workflows
    ↓
Alfred Router and quality gates
    ↓
LlamaIndex evidence retrieval where required
    ↓
ChatGPT / OpenRouter reasoning path depending on interface
    ↓
Executive response
```

## Current Recovery State

Recovery Point Alpha preserves the restored platform, router, Telegram path, LlamaIndex evidence engine, Cloudflare routing and engineering evidence pack.

## Engineering Principle

The system should be evolved by preserving known-good components and making the smallest safe change that advances the current phase.
"""

    def _component_chapter(
        self,
        *,
        title: str,
        purpose: str,
        responsibilities: List[str],
        inputs: List[str],
        outputs: List[str],
        dependencies: List[str],
        failure_modes: List[str],
        recovery: List[str],
        evidence_paths: Iterable[str],
    ) -> str:
        parts = [self._header(title)]
        parts.append(f"## Purpose\n\n{purpose}\n")
        parts.append(self._list("Responsibilities", responsibilities))
        parts.append(self._list("Inputs", inputs))
        parts.append(self._list("Outputs", outputs))
        parts.append(self._list("Dependencies", dependencies))
        parts.append(self._list("Failure Modes", failure_modes))
        parts.append(self._list("Recovery Procedure", recovery))
        parts.append("## Source Evidence\n")
        for rel in evidence_paths:
            item = self.evidence.get(rel)
            if item is None:
                parts.append(f"### {rel}\n\n_Evidence file not found._\n")
            else:
                parts.append(
                    f"### {rel}\n\n"
                    f"Size: {item.size_bytes} bytes\n\n"
                    f"```text\n{item.content[:70000]}\n```\n"
                )
        return "\n".join(parts)

    def _list(self, title: str, values: List[str]) -> str:
        lines = [f"## {title}", ""]
        lines.extend(f"- {value}" for value in values)
        lines.append("")
        return "\n".join(lines)

    def _build_and_recovery(self) -> str:
        return self._header("Build and Recovery Guide") + """
## Restore Order

1. Provision the VPS operating system.
2. Install Python, Docker, systemd-compatible services and cloudflared.
3. Restore `/opt/second-brain`.
4. Restore `/opt/llamaindex-bakeoff`.
5. Restore `/opt/alfred-v2`.
6. Restore `/docker/obsidian-vault`.
7. Restore `/etc/cloudflared`.
8. Restore systemd service files and overrides.
9. Restore environment files without exposing secrets.
10. Start Cloudflare.
11. Start LlamaIndex API.
12. Start Telegram.
13. Validate ChatGPT Action.
14. Validate Telegram.
15. Validate Obsidian vault freshness.

## Validation Tests

```bash
curl -I https://v2.alfreddoheny.cloud
curl -s http://127.0.0.1:8788/docs | head
/opt/second-brain/scripts/alfred_router.sh "tell me about the barclays meeting tomorrow"
systemctl status hermes-telegram.service --no-pager -l
```

## Expected Functional Questions

- Prepare me for the next executive meeting in my vault.
- Tell me about the next executive meeting.
- Who is the owner linked to Project Phoenix?
- Find the test sync note containing 641923.

## Recovery Rule

During recovery, do not redesign. Restore the smallest broken component that returns the system to intended behaviour.
"""
