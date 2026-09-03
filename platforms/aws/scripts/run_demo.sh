#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 -m src.cli --case-id CASE-2026-0917
python3 -m unittest discover -s tests -p "test_*.py" -v
