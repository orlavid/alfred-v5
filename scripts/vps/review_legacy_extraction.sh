#!/usr/bin/env bash
set -euo pipefail

TARGETS=(
  "/opt/second-brain"
  "/opt/alfred-v2"
  "/opt/alfred-v2-prod"
  "/docker/hermes-semantic"
  "/root"
)

PATTERNS=(
  "objectives"
  "projects"
  "follow[- ]?ups?"
  "open loops?"
  "daily logs?"
  "rglob"
  "recursive"
  "vault"
  "obsidian"
  "briefing"
  "entity extraction"
  "semantic"
)

echo "# Legacy Extraction Review"
echo
for target in "${TARGETS[@]}"; do
  if [ ! -d "$target" ]; then
    echo "## $target"
    echo "- missing"
    echo
    continue
  fi

  echo "## $target"
  echo "- present"
  echo
  for pattern in "${PATTERNS[@]}"; do
    echo "### pattern: $pattern"
    rg -n -i --glob '*.py' --glob '*.sh' --glob '*.md' --glob '*.yml' --glob '*.yaml' --glob '*.json' "$pattern" "$target" || true
    echo
  done
done
