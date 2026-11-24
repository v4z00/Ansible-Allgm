#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
run_playbook_logged rsyslog-disable playbooks/maintenance/disable_syslog_forwarding.yml "$@"
