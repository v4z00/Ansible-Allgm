#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"
export CONTROL_PROJECT_ROOT="${ROOT_DIR}"
source "${ROOT_DIR}/lib/control/helpers.sh"
playbook=playbooks/docker/update_containers.yml
for argument in "$@"; do
  case "$argument" in
    --list-hosts|--list-tags|--list-tasks|--syntax-check|-C|--check|-h|--help|--version)
      exec ansible-playbook "$playbook" "$@"
      ;;
  esac
done
for argument in "$@"; do
  case "$argument" in
    --tags|--tags=*|-t|-t?*|--skip-tags|--skip-tags=*|--start-at-task|--start-at-task=*|--step)
      echo "Docker-Update: Eine Teilausführung würde den Pflichtcheck umgehen. Hosts mit --limit auswählen." >&2
      exit 2
      ;;
  esac
done
# A configured tag filter must not silently skip the mandatory container checks.
export ANSIBLE_RUN_TAGS=all ANSIBLE_SKIP_TAGS=''
mkdir -p logs

timestamp=$(date -u +'%Y%m%dT%H%M%SZ')
log_file="${ROOT_DIR}/logs/docker-update-${timestamp}.log"
notification_file=$(mktemp)
trap 'rm -f "${notification_file}"' EXIT

if selection=$(ANSIBLE_NOCOLOR=1 ansible-playbook "$playbook" --list-hosts "$@"); then :
else
  selection_status=$?
  record_control_failure ansible:docker-update Zielauswahl 'Inventory- oder Playbookpruefung fehlgeschlagen; kein Update gestartet.'
  exit "$selection_status"
fi
if ! grep -Eq 'hosts \([1-9][0-9]*\):' <<< "$selection"; then
  echo "Docker-Update: Keine Docker-Zielhosts für den Pflichtcheck ausgewählt." >&2
  record_control_failure ansible:docker-update Zielauswahl 'Keine Docker-Zielhosts ausgewaehlt; kein Update gestartet.'
  exit 2
fi

if ANSIBLE_LOG_PATH="${log_file}" run_playbook_with_jobs \
    "$playbook" "$@"; then
  status=0
  result="✅ ERFOLGREICH"
else
  status=$?
  result="❌ FEHLERHAFT (Exit ${status})"
fi

printf 'Docker-Update %s\nStatus: %s\nLog: %s\n' \
  "${timestamp}" "${result}" "${log_file}" > "${notification_file}"

if [[ ! -f config/script_jobs_controller.json ]] && ! ansible-playbook playbooks/maintenance/notify.yml \
    -e "notification_file=${notification_file}"; then
  status=1
fi

exit "${status}"
