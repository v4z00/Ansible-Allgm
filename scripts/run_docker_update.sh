#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"
mkdir -p logs

timestamp=$(date -u +'%Y%m%dT%H%M%SZ')
log_file="${ROOT_DIR}/logs/docker-update-${timestamp}.log"
notification_file=$(mktemp)
trap 'rm -f "${notification_file}"' EXIT

if ANSIBLE_LOG_PATH="${log_file}" ansible-playbook \
    playbooks/docker/update_containers.yml "$@"; then
  status=0
  result=ERFOLGREICH
else
  status=$?
  result="FEHLERHAFT (Exit ${status})"
fi

printf 'Docker-Update %s\nStatus: %s\nLog: %s\n' \
  "${timestamp}" "${result}" "${log_file}" > "${notification_file}"

if ! ansible-playbook playbooks/maintenance/notify.yml \
    -e "notification_file=${notification_file}"; then
  status=1
fi

exit "${status}"
