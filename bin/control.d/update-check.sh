#!/usr/bin/env bash
set -euo pipefail
exec bash "${CONTROL_PROJECT_ROOT:?}/update_check/check.sh" "$@"
