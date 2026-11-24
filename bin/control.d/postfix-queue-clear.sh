#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
run_playbook_logged postfix-queue-clear playbooks/maintenance/clear_postfix_que.yaml "$@"
