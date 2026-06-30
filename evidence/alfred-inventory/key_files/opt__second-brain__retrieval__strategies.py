from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .models import RouteDecision


DAILY_READER = Path(
    "/opt/second-brain/scripts/get_daily_section.py"
)

LEGACY_ROUTER = Path(
    "/opt/second-brain/scripts/hermes_ask.sh"
)


@dataclass
class StrategyResult:
    stdout: str
    stderr: str
    exit_code: int
    sources: list[str]
    fallback_used: bool


def _run(
    command: list[str],
    timeout_seconds: int,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        env=env,
        check=False,
    )


def deterministic_daily_log(
    decision: RouteDecision,
) -> StrategyResult:
    outputs: list[str] = []
    errors: list[str] = []
    sources: list[str] = []
    exit_code = 0

    if not decision.date_reference:
        return StrategyResult(
            stdout="",
            stderr="Daily-log route did not receive a date.",
            exit_code=2,
            sources=[],
            fallback_used=False,
        )

    for section in decision.sections:
        completed = _run(
            [
                str(DAILY_READER),
                decision.date_reference,
                section,
            ],
            timeout_seconds=30,
        )

        if completed.stdout.strip():
            outputs.append(completed.stdout.strip())

        if completed.stderr.strip():
            errors.append(completed.stderr.strip())

        if completed.returncode != 0:
            exit_code = completed.returncode

    date_display = decision.date_reference

    if date_display not in {"today", "yesterday"}:
        sources.append(
            f"01 Daily Logs/{date_display}.md"
        )

    return StrategyResult(
        stdout="\n\n".join(outputs).strip() + "\n",
        stderr="\n".join(errors),
        exit_code=exit_code,
        sources=sources,
        fallback_used=False,
    )


def protected_legacy(
    decision: RouteDecision,
    question: str,
) -> StrategyResult:
    env = os.environ.copy()
    env.setdefault(
        "HERMES_CONTAINER",
        "hermes-agent-mctr-hermes-agent-1",
    )

    completed = _run(
        [
            str(LEGACY_ROUTER),
            question,
        ],
        timeout_seconds=650,
        env=env,
    )

    return StrategyResult(
        stdout=completed.stdout,
        stderr=completed.stderr,
        exit_code=completed.returncode,
        sources=[],
        fallback_used=True,
    )


def execute_strategy(
    decision: RouteDecision,
    question: str,
) -> StrategyResult:
    if decision.strategy == "reject_empty":
        return StrategyResult(
            stdout="No question was provided.\n",
            stderr="",
            exit_code=2,
            sources=[],
            fallback_used=False,
        )

    if decision.strategy == "deterministic_daily_log":
        return deterministic_daily_log(decision)

    if decision.strategy == "validated_tprm_evidence":
        return protected_legacy(
            decision=decision,
            question=f"__ALFRED_TPRM_EVIDENCE__ {question}",
        )

    if decision.strategy == "validated_cost_evidence":
        return protected_legacy(
            decision=decision,
            question=f"__ALFRED_COST_EVIDENCE__ {question}",
        )

    if decision.strategy in {
        "validated_objective_evidence",
        "protected_legacy_evidence",
        "protected_legacy_entity",
        "protected_legacy_general",
    }:
        return protected_legacy(
            decision=decision,
            question=question,
        )

    return StrategyResult(
        stdout="",
        stderr=(
            f"Unsupported retrieval strategy: "
            f"{decision.strategy}"
        ),
        exit_code=2,
        sources=[],
        fallback_used=False,
    )
