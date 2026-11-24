#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
run_playbook_logged docker-ips playbooks/docker/get_docker_ips.yaml "$@"
