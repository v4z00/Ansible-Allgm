#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
ansible all_linux_systems -i inventory -m ping "$@"
