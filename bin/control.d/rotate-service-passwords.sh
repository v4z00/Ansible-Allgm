#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
run_playbook_logged rotate-service-passwords playbooks/maintenance/rotate_service_user_passwords.yml "$@"
