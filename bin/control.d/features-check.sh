#!/usr/bin/env bash
set -euo pipefail
python3 "${CONTROL_PROJECT_ROOT:?}/scripts/feature_audit.py" --project-root "$CONTROL_PROJECT_ROOT" "$@"
