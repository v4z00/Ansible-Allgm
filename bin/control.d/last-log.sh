#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
show_last_log "${1:-*}"
