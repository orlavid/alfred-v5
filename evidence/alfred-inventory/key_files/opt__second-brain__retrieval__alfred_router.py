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
