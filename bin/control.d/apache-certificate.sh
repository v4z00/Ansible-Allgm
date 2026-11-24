#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
bash scripts/deploy_apache_certificate.sh "$@"
