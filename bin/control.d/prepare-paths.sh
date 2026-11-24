#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
run_playbook_logged prepare-paths playbooks/maintenance/prepare_paths.yml "$@"
