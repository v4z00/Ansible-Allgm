#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
run_playbook_logged lynis playbooks/lynis.yml "$@"
    run_playbook_logged lynis-summary playbooks/reporting/lynis_summary.yml
