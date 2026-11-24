#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
run_playbook_logged fstab-audit playbooks/maintenance/audit_fstab.yml "$@"
