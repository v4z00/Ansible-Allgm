#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
SCRIPT_JOBS_CALLBACK=0 run_playbook_logged jobs-last playbooks/scripts/show_status.yml "$@"
