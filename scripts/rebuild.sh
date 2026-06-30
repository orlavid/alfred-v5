#!/bin/bash
set -e

source .venv/bin/activate

python build_handbook.py
python build_architecture.py

echo
echo "Rebuild complete."
