#!/usr/bin/env bash
set -euo pipefail
cd "${CONTROL_PROJECT_ROOT:?}"
exec python3 scripts/setup_windows.py "$@"
