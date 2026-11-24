#!/usr/bin/env bash
set -euo pipefail
source "${CONTROL_PROJECT_ROOT:?}/lib/control/helpers.sh"
run_playbook_notified crl-renew 'PKI-CRL-Erneuerung' playbooks/pki/renew_crl.yml "$@"
