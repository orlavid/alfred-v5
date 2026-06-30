#!/usr/bin/env bash
set -Eeuo pipefail

export PYTHONPATH="/opt/second-brain${PYTHONPATH:+:$PYTHONPATH}"

exec python3 -m retrieval.alfred_router "$@"
