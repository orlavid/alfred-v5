# Alfred Router

Generated: 2026-06-30T21:41:58.616557


## Purpose

Defines the orchestration and quality gate layer used by Telegram and deterministic workflows.

## Responsibilities

- Classify user intent.
- Select the correct retrieval or deterministic strategy.
- Execute protected routes.
- Validate answers before returning them.
- Withhold unsupported answers rather than hallucinate.

## Inputs

- User query
- Strategy definitions
- Hermes compatibility path
- Evidence policies

## Outputs

- Validated answer
- Quality-gate rejection
- Audit trail

## Dependencies

- alfred_router.sh
- alfred_router.py
- strategies.py
- validation.py
- hermes_ask.sh

## Failure Modes

- Strategy returns non-zero exit code.
- Answer is empty.
- Container default points to stale runtime.
- OpenRouter key unavailable for legacy path.

## Recovery Procedure

- Run alfred_router.sh directly with a known query.
- Check strategies.py defaults.
- Check hermes_ask.sh environment handling.
- Confirm Telegram service environment matches working router configuration.

## Source Evidence

### key_files/opt__second-brain__scripts__alfred_router.sh

Size: 151 bytes

```text
#!/usr/bin/env bash
set -Eeuo pipefail

export PYTHONPATH="/opt/second-brain${PYTHONPATH:+:$PYTHONPATH}"

exec python3 -m retrieval.alfred_router "$@"

```

### key_files/opt__second-brain__retrieval__alfred_router.py

Size: 5719 bytes

```text
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

from .audit import append_audit
from .classifiers import classify_query
from .strategies import StrategyResult, execute_strategy
from .validators import validate_answer


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def output_hash(value: str) -> str:
    return hashlib.sha256(
        value.encode("utf-8", errors="ignore")
    ).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Alfred structured retrieval router",
    )

    parser.add_argument(
        "--explain",
        action="store_true",
        help="Classify and explain the route without answering.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Return a structured response envelope.",
    )

    parser.add_argument(
        "--no-audit",
        action="store_true",
        help="Do not append an audit event.",
    )

    parser.add_argument(
        "question",
        nargs="+",
        help="Natural-language question.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    question = " ".join(args.question).strip()
    decision = classify_query(question)

    if args.explain:
        print(
            json.dumps(
                decision.to_dict(),
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    started_monotonic = time.monotonic()
    started_at = utc_now()

    result = execute_strategy(
        decision=decision,
        question=question,
    )

    validation = validate_answer(
        decision=decision,
        question=question,
        answer=result.stdout,
        exit_code=result.exit_code,
    )

    rejected_output_path = None

    if not validation.passed:
        rejection_root = Path(
            "/opt/second-brain/logs/validation-rejections"
        )

        rejection_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        stamp = datetime.now(
            timezone.utc
        ).strftime("%Y%m%d-%H%M%S-%f")

        rejected_output = (
            rejection_root
            / f"rejected-{stamp}.txt"
        )

        rejected_output.write_text(
            "\n".join(
                [
                    f"Question: {question}",
                    f"Intent: {decision.intent}",
                    f"Strategy: {decision.strategy}",
                    "",
                    "Validation failures:",
                    *[
                        f"- {failure}"
                        for failure in validation.failures
                    ],
                    "",
                    "Rejected answer:",
                    result.stdout,
                    "",
                    "Retrieval stderr:",
                    result.stderr,
                ]
            ),
            encoding="utf-8",
        )

        rejected_output_path = str(
            rejected_output
        )

        controlled_message = "\n".join(
            [
                "Alfred withheld this answer because it "
                "did not meet the evidence-quality standard.",
                "",
                "Validation issues:",
                *[
                    f"- {failure}"
                    for failure in validation.failures
                ],
                "",
                "No unsupported answer has been returned.",
            ]
        ) + "\n"

        result = StrategyResult(
            stdout=controlled_message,
            stderr=result.stderr,
            exit_code=3,
            sources=result.sources,
            fallback_used=result.fallback_used,
        )

    duration_seconds = round(
        time.monotonic() - started_monotonic,
        3,
    )

    event: dict[str, Any] = {
        "timestamp": started_at,
        "question": question,
        "decision": decision.to_dict(),
        "result": {
            "exit_code": result.exit_code,
            "duration_seconds": duration_seconds,
            "output_characters": len(result.stdout),
            "output_sha256": output_hash(result.stdout),
            "sources": result.sources,
            "fallback_used": result.fallback_used,
        },
        "validation": {
            **validation.to_dict(),
            "rejected_output_path": rejected_output_path,
        },
        "runtime": {
            "hermes_container": os.environ.get(
                "HERMES_CONTAINER",
                "hermes-authoritative-vault",
            ),
            "router_version": "0.2.0",
        },
    }

    if not args.no_audit:
        append_audit(event)

    if args.json:
        envelope = {
            "route": decision.to_dict(),
            "result": {
                "answer": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.exit_code,
                "duration_seconds": duration_seconds,
                "sources": result.sources,
                "fallback_used": result.fallback_used,
            },
        }

        print(
            json.dumps(
                envelope,
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        if result.stdout:
            sys.stdout.write(result.stdout)

        if result.stderr:
            sys.stderr.write(result.stderr)

            if not result.stderr.endswith("\n"):
                sys.stderr.write("\n")

    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())

```

### key_files/opt__second-brain__retrieval__strategies.py

Size: 3960 bytes

```text
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

```

### key_files/opt__second-brain__scripts__hermes_ask.sh

Size: 31008 bytes

```text
#!/bin/bash
set -euo pipefail

QUERY="$*"
printf "%s\n---\n" "$QUERY" >> /tmp/hermes_ask_queries.log

# Allow callers to select the Hermes runtime explicitly.
# Keep the previous runtime as the temporary default until migration is complete.
HERMES_CONTAINER="${HERMES_CONTAINER:-hermes-agent-mctr-hermes-agent-1}"

KEY_CONTAINER="${HERMES_KEY_CONTAINER:-hermes-agent-mctr-hermes-agent-1}"

if [ -n "${OPENROUTER_API_KEY:-}" ]; then
  REAL_KEY="$OPENROUTER_API_KEY"
else
  REAL_KEY=$(docker inspect "$KEY_CONTAINER" --format '{{range .Config.Env}}{{println .}}{{end}}' | grep '^OPENROUTER_API_KEY=<redacted>
fi

if [[ "${HERMES_SYNTHESIS_ONLY:-0}" == "1" ]]; then
  PROMPT="$QUERY"

  timeout 300 docker exec \
    -e HERMES_PROMPT="$PROMPT" \
    -e OPENROUTER_API_KEY=<redacted>
    "$HERMES_CONTAINER" \
    bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
    2>/tmp/hermes_ask.err \
    | tr -d '\000' \
    | sed '/session_id:/d'

  exit ${PIPESTATUS[0]}
fi


if [ -z "$QUERY" ]; then
  echo "No query supplied."
  exit 1
fi

# Deterministic routing for structured daily-log requests.
# These requests must not use entity, direct-reference or semantic retrieval.
LOWER_QUERY=$(printf '%s' "$QUERY" | tr '[:upper:]' '[:lower:]')

# Deterministic routing for explicit ISO dates such as 2026-06-10.
# A structured date + section request must not fall through to semantic search.
EXPLICIT_ROUTE=$(
  python3 - "$QUERY" <<'PYROUTE'
import re
import sys

query = sys.argv[1].lower()

date_match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", query)
if not date_match:
    raise SystemExit(0)

sections = []

if re.search(r"\bfollow[\s-]*ups?\b|\bfollow[\s-]*up actions?\b", query):
    sections.append("follow-ups")

if re.search(r"\bopen[\s-]*loops?\b", query):
    sections.append("open-loops")

if re.search(r"\bdecisions?\b", query):
    sections.append("decisions")

if sections:
    print(f"{date_match.group(1)}\t{','.join(sections)}")
PYROUTE
)

if [[ -n "$EXPLICIT_ROUTE" ]]; then
  IFS=$'\t' read -r EXPLICIT_DATE EXPLICIT_SECTIONS <<< "$EXPLICIT_ROUTE"
  IFS=',' read -r -a SECTION_LIST <<< "$EXPLICIT_SECTIONS"

  for INDEX in "${!SECTION_LIST[@]}"; do
    if (( INDEX > 0 )); then
      printf '\n'
    fi

    /opt/second-brain/scripts/get_daily_section.py       "$EXPLICIT_DATE"       "${SECTION_LIST[$INDEX]}"
  done

  exit 0
fi

case "$LOWER_QUERY" in
  *yesterday*"follow up"*"open loop"*|*yesterday*"open loop"*"follow up"*|*"follow up"*"open loop"*yesterday*|*"open loop"*"follow up"*yesterday*)
    /opt/second-brain/scripts/get_daily_section.py yesterday follow-ups
    printf '\n'
    exec /opt/second-brain/scripts/get_daily_section.py yesterday open-loops
    ;;
  *today*"follow up"*"open loop"*|*today*"open loop"*"follow up"*|*"follow up"*"open loop"*today*|*"open loop"*"follow up"*today*)
    /opt/second-brain/scripts/get_daily_section.py today follow-ups
    printf '\n'
    exec /opt/second-brain/scripts/get_daily_section.py today open-loops
    ;;
  *yesterday*"follow up"*|*"follow up"*yesterday*)
    exec /opt/second-brain/scripts/get_daily_section.py yesterday follow-ups
    ;;
  *today*"follow up"*|*"follow up"*today*)
    exec /opt/second-brain/scripts/get_daily_section.py today follow-ups
    ;;
  *yesterday*"open loop"*|*"open loop"*yesterday*)
    exec /opt/second-brain/scripts/get_daily_section.py yesterday open-loops
    ;;
  *today*"open loop"*|*"open loop"*today*)
    exec /opt/second-brain/scripts/get_daily_section.py today open-loops
    ;;
  *yesterday*"decision"*|*"decision"*yesterday*)
    exec /opt/second-brain/scripts/get_daily_section.py yesterday decisions
    ;;
  *today*"decision"*|*"decision"*today*)
    exec /opt/second-brain/scripts/get_daily_section.py today decisions
    ;;
esac

# Objective, HR-goal and performance-review questions use an exclusive,
# evidence-led route. They must not be contaminated by generic semantic
# results, generated Objective Intelligence reports, board packs, or prior
# AI-generated summaries.
if printf '%s' "$LOWER_QUERY" | grep -Eq \
  '(hr|team|annual|year|performance review|performance-review).*(objective|goal)|(objective|goal).*(hr|team|annual|year|performance review|performance-review)'
then
  OBJECTIVE_EVIDENCE=$(
    /opt/second-brain/scripts/objective_evidence_search.py \
      | sed -n '1,320p'
  )

  OBJECTIVE_PROMPT="
You are Alfred, Phillip's operational second brain and executive chief-of-staff AI.

The user is asking for HR, team, annual, or performance-review objectives.

Use ONLY the concrete source evidence supplied below.
Do not use semantic memory, generated governance reports, Objective Intelligence reports, board packs, executive briefings, AI Memory, archived summaries, or previous objective wording.

The objective is not to produce generic HR language. The objective is to identify the specific business needs evidenced in the vault and convert them into practical, measurable objectives.

STRICT RULES

1. Each objective must include at least two concrete business facts from the supplied evidence.

2. At least one fact must be one of:
   - a named initiative;
   - a control failure;
   - a regulatory obligation;
   - a delivery problem;
   - a financial amount;
   - an explicit target;
   - a missing process;
   - a documented risk;
   - a required remediation;
   - a named system, supplier, team or programme.

3. Use only the source paths and line numbers included in the supplied evidence.

4. Never invent:
   - percentages;
   - deadlines;
   - financial targets;
   - completion rates;
   - efficiency improvements;
   - implementation dates.

5. Where the evidence contains no agreed numerical target or date, write:
   Target and completion date to be agreed with the objective owner.

6. Do not use unsupported phrases such as:
   - improve efficiency;
   - enhance governance;
   - drive innovation;
   - support development;
   - strengthen capability;
unless you immediately state the specific process, control, deliverable, metric or business condition that will change.

7. Do not cite any source under:
   - 09 Governance
   - 07 AI Memory
   - 07 Executive Briefings
   - 98 Archive

8. Historical objective prose is not evidence. Base the answer on operational facts, problems, initiatives, risks, targets and obligations.

9. Produce one objective from each of the six supplied evidence themes:
   - Operational Governance and DORA
   - Supplier Risk and Contractual Control
   - Data, AI and Automation
   - People, Capability and Succession
   - Cost, Spend and Procurement Control
   - Performance, Reporting and Delivery

   Do not replace any of these with a generic management category.
   Where a theme lacks sufficient evidence, state that rather than inventing content.

10. For every objective, use exactly these headings:

### <number>. <specific objective title>

BUSINESS NEED
State the concrete source facts that justify the objective.

OBJECTIVE
State the specific result the team member or team must deliver.

DELIVERABLES
List tangible outputs such as a deployed process, completed remediation, approved policy, implemented control, dashboard, signed-off framework, training plan, or documented operating model.

MEASURES
Use only measures already explicit in the evidence. Where no agreed target exists, state that the target must be agreed.

SOURCES
List exact vault paths and line numbers.

INFERENCE
State precisely which parts of the objective or deliverables were synthesised by Alfred rather than explicitly stated in the notes.

11. End with:
Evidence coverage: Strong / Moderate / Weak
Source notes used: <paths>
Inferred or newly suggested content: <honest summary>

CONCRETE OBJECTIVE EVIDENCE:
$OBJECTIVE_EVIDENCE

USER QUESTION:
$QUERY

Produce a concise but operationally specific answer.
"

  OBJECTIVE_OUTPUT=$(mktemp /tmp/alfred-objective-output.XXXXXX)
  OBJECTIVE_ERROR=$(mktemp /tmp/alfred-objective-error.XXXXXX)

  cleanup_objective_files() {
    rm -f "$OBJECTIVE_OUTPUT" "$OBJECTIVE_ERROR"
  }

  validate_objective_answer() {
    local answer_file="$1"
    local objective_count
    local marker_count=0

    [[ -s "$answer_file" ]] || {
      echo "VALIDATION: answer was empty" >&2
      return 1
    }

    if grep -qiE \
      '09 Governance/Objective Intelligence|07 AI Memory|07 Executive Briefings|98 Archive|15% by|20% by|90% completion|nothing inferred|Inferred or newly suggested content:[[:space:]]*(None|none)' \
      "$answer_file"
    then
      echo "VALIDATION: forbidden source or unsupported claim detected" >&2
      return 1
    fi

    for heading in \
      "BUSINESS NEED" \
      "OBJECTIVE" \
      "DELIVERABLES" \
      "MEASURES" \
      "SOURCES" \
      "INFERENCE"
    do
      if ! grep -q "$heading" "$answer_file"; then
        echo "VALIDATION: required heading missing: $heading" >&2
        return 1
      fi
    done

    objective_count=$(
      grep -Ec '^###[[:space:]]+[1-6]\.' "$answer_file" || true
    )

    if (( objective_count < 6 )); then
      echo \
        "VALIDATION: expected six objectives, found $objective_count" \
        >&2
      return 1
    fi

    for marker in \
      'TPRM 2\.0' \
      'DORA' \
      '70011' \
      'duplicate invoice|£95k|95k' \
      'controllable OPEX|OPEX' \
      '\$1\.5m|1\.5m|savings' \
      'AI strategy|AI governance' \
      'key person|retention|succession' \
      'SLA|KPI|dashboard' \
      'subcontract|audit right|exit plan'
    do
      if grep -qiE "$marker" "$answer_file"; then
        marker_count=$((marker_count + 1))
      fi
    done

    if (( marker_count < 4 )); then
      echo \
        "VALIDATION: insufficient concrete business evidence markers: $marker_count/4" \
        >&2
      return 1
    fi

    if ! grep -qiE \
      'Inferred or newly suggested content:[[:space:]]*.+' \
      "$answer_file"
    then
      echo "VALIDATION: provenance footer missing" >&2
      return 1
    fi

    return 0
  }

  generate_objective_answer() {
    local prompt="$1"
    local output_file="$2"
    local error_file="$3"
    local status

    set +e

    timeout 300 docker exec \
      -e HERMES_PROMPT="$prompt" \
      -e OPENROUTER_API_KEY=<redacted>
      "$HERMES_CONTAINER" \
      bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
      2>"$error_file" \
      | tr -d '\000' \
      | sed '/session_id:/d' \
      > "$output_file"

    status=${PIPESTATUS[0]}

    set -e

    return "$status"
  }

  if ! generate_objective_answer \
    "$OBJECTIVE_PROMPT" \
    "$OBJECTIVE_OUTPUT" \
    "$OBJECTIVE_ERROR"
  then
    cat "$OBJECTIVE_ERROR" > /tmp/hermes_ask.err
    cleanup_objective_files
    echo \
      "Alfred could not generate the objective answer because the model call failed."
    exit 1
  fi

  if ! validate_objective_answer "$OBJECTIVE_OUTPUT"; then
    CORRECTIVE_OBJECTIVE_PROMPT="$OBJECTIVE_PROMPT

QUALITY-CONTROL CORRECTION

The previous draft failed the evidence-quality validation.

Regenerate the complete answer from the supplied concrete evidence.

Mandatory corrections:

- Produce exactly six numbered objectives.
- Use all six required headings for every objective.
- Include at least four distinct concrete operational facts across the answer.
- Do not cite any generated or governance-summary source.
- Do not invent percentages, financial amounts, deadlines or completion rates.
- Do not claim that nothing was inferred.
- The objective wording, grouping and proposed deliverables are necessarily inferred and must be declared honestly.
- Use only paths and line numbers supplied in CONCRETE OBJECTIVE EVIDENCE.
- Prefer named initiatives, control failures, financial facts, regulatory obligations and delivery gaps over generic management language.
"

    : > "$OBJECTIVE_OUTPUT"
    : > "$OBJECTIVE_ERROR"

    if ! generate_objective_answer \
      "$CORRECTIVE_OBJECTIVE_PROMPT" \
      "$OBJECTIVE_OUTPUT" \
      "$OBJECTIVE_ERROR"
    then
      cat "$OBJECTIVE_ERROR" > /tmp/hermes_ask.err
      cleanup_objective_files
      echo \
        "Alfred could not generate the objective answer because the corrective model call failed."
      exit 1
    fi
  fi

  if ! validate_objective_answer "$OBJECTIVE_OUTPUT"; then
    {
      echo "Objective answer failed validation after two attempts."
      echo
      echo "The answer was withheld because it did not meet Alfred's evidence-quality standard."
      echo "No unsupported objective has been returned."
    }

    {
      echo "=== Rejected answer ==="
      cat "$OBJECTIVE_OUTPUT"
      echo
      echo "=== Model error output ==="
      cat "$OBJECTIVE_ERROR"
    } > "/tmp/alfred-objective-rejected-$(date +%Y%m%d-%H%M%S).log"

    cleanup_objective_files
    exit 1
  fi

  cat "$OBJECTIVE_OUTPUT"
  cat "$OBJECTIVE_ERROR" > /tmp/hermes_ask.err

  cleanup_objective_files
  exit 0
fi

# Internal protected TPRM route used by the structured Python candidate.
if [[ "$QUERY" == "__ALFRED_TPRM_EVIDENCE__"* ]]; then
  TPRM_QUERY="${QUERY#__ALFRED_TPRM_EVIDENCE__}"
  TPRM_QUERY="${TPRM_QUERY# }"

  TPRM_EVIDENCE=$(
    /opt/second-brain/scripts/tprm_evidence_search.py \
      | sed -n '1,340p'
  )

  TPRM_PROMPT="
You are Alfred, Phillip's operational second brain and executive chief-of-staff AI.

The user is asking about TPRM 2.0 business problems, risks, controls,
implementation gaps or required remediation.

Use ONLY the concrete primary-source evidence below.

Do not use generated governance reports, Objective Intelligence, board packs,
AI Memory, executive briefings, archived summaries or previous AI answers.

STRICT RULES

1. Identify the specific TPRM 2.0 problems evidenced in the notes.

2. Cover the relevant evidence categories:
   - current-system failure and MVP replacement;
   - DORA, tiering and service-level design;
   - subcontracting and supply-chain control;
   - exit planning and substitutability;
   - SLA and obligation monitoring;
   - operational process, ownership and remediation.

3. Every material point must identify:
   - the concrete problem;
   - the business or regulatory consequence;
   - the required action;
   - the exact source path and line number;
   - what Alfred inferred.

4. Preserve concrete facts such as:
   - the current system being non-functional;
   - the need for an MVP replacement;
   - DORA decision-tree or toggle defects;
   - service-level risk and tiering;
   - subcontractor RTS and supply-chain visibility;
   - exit planning and substitutability;
   - SLA or obligation monitoring;
   - missing operating processes;
   - remediation across the contract population.

5. Do not invent dates, percentages, financial values or completion targets.

6. Do not say evidence is absent when it is supplied.

7. Do not claim that nothing was inferred.

Use this format:

### <number>. <specific TPRM problem>

BUSINESS EVIDENCE
CONSEQUENCE
ACTION REQUIRED
SOURCES
INFERENCE

End with:

Evidence coverage: Strong / Moderate / Weak
Source notes used: <paths>
Inferred or newly suggested content: <honest description>

PRIMARY TPRM EVIDENCE:
$TPRM_EVIDENCE

USER QUESTION:
$TPRM_QUERY
"

  TPRM_OUTPUT=$(mktemp /tmp/alfred-tprm-output.XXXXXX)
  TPRM_ERROR=$(mktemp /tmp/alfred-tprm-error.XXXXXX)

  cleanup_tprm_files() {
    rm -f "$TPRM_OUTPUT" "$TPRM_ERROR"
  }

  generate_tprm_answer() {
    local prompt="$1"

    set +e

    timeout 300 docker exec \
      -e HERMES_PROMPT="$prompt" \
      -e OPENROUTER_API_KEY=<redacted>
      "$HERMES_CONTAINER" \
      bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
      2>"$TPRM_ERROR" \
      | tr -d '\000' \
      | sed '/session_id:/d' \
      > "$TPRM_OUTPUT"

    local status=${PIPESTATUS[0]}

    set -e
    return "$status"
  }

  validate_tprm_answer() {
    local markers=0

    [[ -s "$TPRM_OUTPUT" ]] || return 1

    if grep -qiE \
      '09 Governance|Objective Intelligence|07 AI Memory|07 Executive Briefings|no relevant information|nothing inferred|Inferred or newly suggested content:[[:space:]]*(None|none)' \
      "$TPRM_OUTPUT"
    then
      return 1
    fi

    for heading in \
      "BUSINESS EVIDENCE" \
      "CONSEQUENCE" \
      "ACTION REQUIRED" \
      "SOURCES" \
      "INFERENCE"
    do
      grep -q "$heading" "$TPRM_OUTPUT" || return 1
    done

    for marker in \
      'MVP|non-functional|not working' \
      'DORA decision tree|DORA toggle|tiering|service level' \
      'subcontract|supply chain|RTS' \
      'exit plan|substitutability' \
      'SLA|obligation|monitoring' \
      'operational process|procedure|remediation|170 contracts'
    do
      if grep -qiE "$marker" "$TPRM_OUTPUT"; then
        markers=$((markers + 1))
      fi
    done

    (( markers >= 3 ))
  }

  if ! generate_tprm_answer "$TPRM_PROMPT"; then
    cat "$TPRM_ERROR" > /tmp/hermes_ask.err
    cleanup_tprm_files
    echo "Alfred could not generate the TPRM answer."
    exit 1
  fi

  if ! validate_tprm_answer; then
    TPRM_CORRECTION="$TPRM_PROMPT

QUALITY-CONTROL CORRECTION

The previous answer failed validation.

Regenerate the answer and include at least three distinct concrete problem
groups from the supplied evidence, including the non-functional system/MVP
and at least two of:

- DORA decision-tree or service-level design;
- subcontracting or RTS;
- exit planning or substitutability;
- SLA and obligation monitoring;
- missing operational processes or remediation.

Use only supplied source paths and line numbers. Declare synthesis honestly.
"

    : > "$TPRM_OUTPUT"
    : > "$TPRM_ERROR"

    if ! generate_tprm_answer "$TPRM_CORRECTION"; then
      cat "$TPRM_ERROR" > /tmp/hermes_ask.err
      cleanup_tprm_files
      echo "Alfred could not generate the corrected TPRM answer."
      exit 1
    fi
  fi

  if ! validate_tprm_answer; then
    echo "The TPRM answer was withheld because it failed Alfred's evidence-quality validation."
    echo "No unsupported answer has been returned."

    {
      echo "=== Rejected TPRM answer ==="
      cat "$TPRM_OUTPUT"
      echo
      echo "=== Error output ==="
      cat "$TPRM_ERROR"
    } > "/tmp/alfred-tprm-rejected-$(date +%Y%m%d-%H%M%S).log"

    cleanup_tprm_files
    exit 1
  fi

  cat "$TPRM_OUTPUT"
  cat "$TPRM_ERROR" > /tmp/hermes_ask.err
  cleanup_tprm_files
  exit 0
fi

# Internal protected route used only by the structured Python candidate.
# The prefix is removed before the user's question is presented.
if [[ "$QUERY" == "__ALFRED_COST_EVIDENCE__"* ]]; then
  COST_QUERY="${QUERY#__ALFRED_COST_EVIDENCE__}"
  COST_QUERY="${COST_QUERY# }"

  COST_EVIDENCE=$(
    /opt/second-brain/scripts/cost_evidence_search.py \
      | sed -n '1,360p'
  )

  COST_PROMPT="
You are Alfred, Phillip's operational second brain and executive chief-of-staff AI.

The user is asking for cost-control, expenditure, budget, accounts-payable,
purchase-order or spend-governance priorities.

Use ONLY the concrete primary-source evidence supplied below.

Do not use:
- generic semantic retrieval;
- 09 Governance;
- Objective Intelligence;
- board packs;
- AI Memory;
- executive briefings;
- archived summaries;
- previous AI-generated recommendations.

STRICT EVIDENCE RULES

1. Identify the strongest business priorities from the supplied evidence.

2. Every priority must contain:
   - a concrete problem, control failure, target or obligation;
   - the specific action required;
   - a measure taken directly from the evidence, where available;
   - exact source paths and line numbers;
   - an honest statement of what Alfred inferred.

3. Preserve specific facts such as:
   - PO requirements;
   - duplicate or erroneous invoices;
   - payment-term configuration;
   - segregation-of-duty concerns;
   - controllable OPEX;
   - travel and expense control;
   - savings targets;
   - CAPEX/OPEX governance;
   - budget and invoice reconciliation.

4. Never invent:
   - percentages;
   - deadlines;
   - financial amounts;
   - savings targets;
   - completion dates.

5. Where a target or date is not explicit, state:
   Target and completion date to be agreed with the owner.

6. Do not say that no evidence exists when concrete evidence is supplied.

7. Do not claim that nothing was inferred. Priority grouping and action wording
   are necessarily Alfred synthesis.

For each priority, use:

### <number>. <specific priority title>

BUSINESS EVIDENCE
ACTION REQUIRED
MEASURES
SOURCES
INFERENCE

End with:

Evidence coverage: Strong / Moderate / Weak
Source notes used: <paths>
Inferred or newly suggested content: <honest description>

PRIMARY COST AND VALUE EVIDENCE:
$COST_EVIDENCE

USER QUESTION:
$COST_QUERY
"

  COST_OUTPUT=$(mktemp /tmp/alfred-cost-output.XXXXXX)
  COST_ERROR=$(mktemp /tmp/alfred-cost-error.XXXXXX)

  cleanup_cost_files() {
    rm -f "$COST_OUTPUT" "$COST_ERROR"
  }

  generate_cost_answer() {
    local prompt="$1"

    set +e

    timeout 300 docker exec \
      -e HERMES_PROMPT="$prompt" \
      -e OPENROUTER_API_KEY=<redacted>
      "$HERMES_CONTAINER" \
      bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
      2>"$COST_ERROR" \
      | tr -d '\000' \
      | sed '/session_id:/d' \
      > "$COST_OUTPUT"

    local status=${PIPESTATUS[0]}

    set -e
    return "$status"
  }

  validate_cost_answer() {
    local markers=0

    [[ -s "$COST_OUTPUT" ]] || return 1

    if grep -qiE \
      '09 Governance|Objective Intelligence|07 AI Memory|07 Executive Briefings|no direct references|no relevant information|nothing inferred|Inferred or newly suggested content:[[:space:]]*(None|none)' \
      "$COST_OUTPUT"
    then
      return 1
    fi

    for heading in \
      "BUSINESS EVIDENCE" \
      "ACTION REQUIRED" \
      "MEASURES" \
      "SOURCES" \
      "INFERENCE"
    do
      grep -q "$heading" "$COST_OUTPUT" || return 1
    done

    for marker in \
      'PO|70011' \
      'duplicate invoice|£95k|95k' \
      'travel|controllable OPEX' \
      '\$1\.5m|1\.5m|savings' \
      'CAPEX|OPEX' \
      'payment terms|separation of duties'
    do
      if grep -qiE "$marker" "$COST_OUTPUT"; then
        markers=$((markers + 1))
      fi
    done

    (( markers >= 3 ))
  }

  if ! generate_cost_answer "$COST_PROMPT"; then
    cat "$COST_ERROR" > /tmp/hermes_ask.err
    cleanup_cost_files
    echo "Alfred could not generate the cost-control answer."
    exit 1
  fi

  if ! validate_cost_answer; then
    COST_CORRECTION="$COST_PROMPT

QUALITY-CONTROL CORRECTION

The previous answer failed validation.

Regenerate it using the concrete source facts. Include at least three of:
PO controls, the £95k duplicate invoice, payment terms, segregation of duties,
controllable OPEX, travel controls, the \$1.5m savings target, or CAPEX/OPEX
finance governance.

Do not claim evidence is absent. Do not cite generated sources. Declare all
synthesis honestly.
"

    : > "$COST_OUTPUT"
    : > "$COST_ERROR"

    if ! generate_cost_answer "$COST_CORRECTION"; then
      cat "$COST_ERROR" > /tmp/hermes_ask.err
      cleanup_cost_files
      echo "Alfred could not generate the corrected cost-control answer."
      exit 1
    fi
  fi

  if ! validate_cost_answer; then
    {
      echo "The cost-control answer was withheld because it failed Alfred's evidence-quality validation."
      echo "No unsupported answer has been returned."
    }

    {
      echo "=== Rejected cost answer ==="
      cat "$COST_OUTPUT"
      echo
      echo "=== Error output ==="
      cat "$COST_ERROR"
    } > "/tmp/alfred-cost-rejected-$(date +%Y%m%d-%H%M%S).log"

    cleanup_cost_files
    exit 1
  fi

  cat "$COST_OUTPUT"
  cat "$COST_ERROR" > /tmp/hermes_ask.err
  cleanup_cost_files
  exit 0
fi

ENTITY=$(/opt/second-brain/scripts/entity_resolver.py "$QUERY" | sed -n "1,120p")
DIRECT=$(/opt/second-brain/scripts/direct_reference_search.py "$QUERY" | head -35)
OBJECTIVE_EVIDENCE=""

if printf '%s' "$LOWER_QUERY" | grep -Eq   '(hr|team|annual|year|performance review).*(objective|goal)|(objective|goal).*(hr|team|annual|year|performance review)'
then
  OBJECTIVE_EVIDENCE=$(
    /opt/second-brain/scripts/objective_evidence_search.py       | head -420
  )
fi

SEARCH_QUERY=$(
  python3 - "$QUERY" <<'PYQUERY'
import re
import sys

query = sys.argv[1].strip()

patterns = [
    r"^\s*what\s+do\s+my\s+notes\s+say\s+about\s+",
    r"^\s*what\s+does\s+my\s+vault\s+say\s+about\s+",
    r"^\s*what\s+do\s+i\s+have\s+on\s+",
    r"^\s*tell\s+me\s+about\s+",
    r"^\s*find\s+(?:all\s+)?(?:references\s+to\s+)?",
    r"^\s*search\s+(?:my\s+)?(?:notes|vault)\s+for\s+",
]

for pattern in patterns:
    query = re.sub(pattern, "", query, flags=re.IGNORECASE)

query = query.strip(" \t\r\n?.!,:;")

print(query or sys.argv[1].strip())
PYQUERY
)

LEXICAL=$(
  /opt/second-brain/scripts/lexical_vault_search.py "$SEARCH_QUERY"     | head -260
)

SEMANTIC=$(
  /opt/second-brain/scripts/semantic_query_fast.py "$SEARCH_QUERY"     | tr -d "\000"     | head -220
)

PROMPT="
You are Hermes, Orl's operational second brain and executive chief-of-staff AI.

You have access to retrieved Obsidian memory below.
CRITICAL: Use ONLY the retrieved Obsidian memory below. Do not search files, do not use filesystem tools, and ignore any Hermes application/node_modules results.

Treat every retrieved source as independent evidence.
Use a source only when it directly answers the user's question.
Do not merge separate people, companies, projects, meetings, dates or actions merely because they use similar words.
Reject retrieved material that is only broadly or topically similar.
Do not revive historic actions unless the question explicitly requests historic material.
For date-specific requests, use only evidence from the requested date.
When reliable evidence is absent, say so instead of constructing a plausible answer.
Exact lexical matches are primary evidence that the subject exists in the vault. Use semantic retrieval to supplement and interpret them.
Never claim that the notes contain no references merely because semantic retrieval is incomplete. You may say nothing was found only when ENTITY RESOLUTION, EXACT LEXICAL VAULT MATCHES, RETRIEVED OBSIDIAN MEMORY, and DIRECT VAULT REFERENCES are all empty or irrelevant.
The retrieved memory below has already been retrieved from the live Obsidian vault. Never claim you cannot access files, folders, notes or directories if relevant information appears in the retrieved memory. Never say a path is missing, inaccessible or unavailable when retrieved memory contains results from that path. Do not describe retrieval limitations. Do not explain how memory was obtained. Do not mention filesystem access. Answer directly from the supplied evidence.
When ENTITY RESOLUTION contains a named person, company, project, or system, treat it as the primary source of truth. For meeting preparation, produce an agenda grounded in the entity note and preserve specific active topics, open items, ownership points, and linked suppliers/systems. Do not collapse these into generic categories.
For meeting preparation requests (meeting, 1:1, catchup, agenda, discuss, cover, stakeholder meeting), do not simply list topics. Build an executive agenda. For each topic provide:
- Why it matters
- Decision required or question to ask
- Follow-up or dependency
Prioritise items from recent dated entity sections before older background topics.
Your job is not only to search memory. Your job is to use memory as context and then produce a useful answer.

If the user asks for:
- drafting
- planning
- HR objectives
- SMART objectives
- procurement advice
- governance analysis
- strategy
- recommendations
- performance review wording

then produce a developed, practical answer.

Use the memory where relevant, but do not refuse just because the retrieved memory is incomplete.
ENTITY RESOLUTION:
$ENTITY

If memory is incomplete, say what you inferred.

DEDICATED OBJECTIVE EVIDENCE:
$OBJECTIVE_EVIDENCE

If DEDICATED OBJECTIVE EVIDENCE is present:

- Use it as the primary and controlling evidence.
- Do not reuse historical objective wording unless supported by operational evidence.
- Each proposed objective must identify at least two concrete business facts.
- At least one fact must be a problem, risk, obligation, target, control failure, delivery gap, financial amount, deadline, or named initiative.
- Include the exact source path and line number supplied in the evidence.
- Explain why the evidence creates a business need for the objective.
- Convert that business need into a measurable HR objective.
- Define observable completion measures.
- Do not use generic phrases such as enhance, improve, support, or develop without stating what specifically changes and how success will be measured.
- If sufficient evidence does not exist for six objectives, return fewer than six and state why.
- For every objective use these headings:
  BUSINESS EVIDENCE
  OBJECTIVE
  MEASURES
  SOURCE
  INFERENCE

PROVENANCE AND EVIDENCE RULES:

For every material claim, recommendation, objective, conclusion, risk, or action:

1. Classify it as one of:
   - EXPLICITLY EVIDENCED: directly supported by retrieved vault content.
   - INFERRED FROM EVIDENCE: reasonably derived from retrieved content but not explicitly stated.
   - ALFRED SUGGESTION: newly proposed by the model and not present in the vault.
   - INSUFFICIENT EVIDENCE: the retrieved material does not support a reliable answer.

2. Give the source vault path for every EXPLICITLY EVIDENCED or INFERRED item.

3. Do not describe a recommendation as being from the notes unless retrieved evidence directly supports it.

4. Never convert absence from the retrieved top results into a statement that the vault contains no information.

5. For objectives, recommendations, priorities, themes, risks, or strategy:
   - first identify the evidence found in the vault;
   - then derive the recommendation;
   - clearly separate evidence from synthesis.

6. Prefer original source notes over generated summaries, executive briefings, enrichment files, governance indexes, change reports, and previous AI-generated answers.

7. When evidence is weak or generic, state that clearly rather than filling gaps with plausible management language.

8. End evidence-based answers with:
   Evidence coverage: Strong / Moderate / Weak
   Source notes used: <list of paths>
   Inferred or newly suggested content: <brief declaration>

EXACT LEXICAL VAULT MATCHES:
$LEXICAL

RETRIEVED OBSIDIAN MEMORY:
$SEMANTIC

DIRECT VAULT REFERENCES:
$DIRECT

USER QUESTION:
$QUERY

Answer clearly and practically.
"

timeout 300 docker exec \
-e HERMES_PROMPT="$PROMPT" \
-e OPENROUTER_API_KEY=<redacted>
"$HERMES_CONTAINER" \
bash -lc '/opt/hermes/.venv/bin/hermes chat --provider openrouter -m openai/gpt-4o-mini -q "$HERMES_PROMPT" -Q' \
2>/tmp/hermes_ask.err \
| tr -d '\000' \
| sed '/session_id:/d'

```
