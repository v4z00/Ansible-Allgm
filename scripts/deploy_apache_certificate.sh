#!/usr/bin/env bash
set -euo pipefail

project_root="${ANSIBLE_PROJECT_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)}"
if [[ "${EUID}" -ne 0 ]]; then
  echo "Dieses Skript muss als root auf dem Ansible-Controller laufen." >&2
  exit 1
fi
cd -- "${project_root}"
umask 077
exec python3 scripts/apache_certificate_files.py select playbooks/pki/deploy_apache_certificate.yml "$@"
