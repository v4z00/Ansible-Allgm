#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
run_playbook_logged docker-auto-update-stop playbooks/docker/stop_auto_upgrade_docker.yaml "$@"
