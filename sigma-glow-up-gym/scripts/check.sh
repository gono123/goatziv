#!/usr/bin/env bash
# Runs every check: format, lint, unit tests, Rojo build. Stops at the first failure.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== stylua =="
stylua --check src tests
echo "== selene =="
selene src
echo "== lune tests =="
lune run tests/run
echo "== rojo build =="
rojo build -o build.rbxl
echo "All checks passed."
