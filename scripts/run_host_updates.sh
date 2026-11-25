#!/usr/bin/env bash
# Host-update starter 1.0.1; requires explicit inventory host names.
set -euo pipefail
umask 077
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="${PATH:-/usr/local/bin:/usr/bin:/bin}:/usr/local/bin:/usr/local/sbin:/usr/sbin:/sbin"
export ANSIBLE_CONFIG="${ROOT_DIR}/ansible.cfg"
export ANSIBLE_NOCOLOR=1
cd "${ROOT_DIR}"

if [[ $# -ne 2 || "$1" != --limit || ! "$2" =~ ^[A-Za-z0-9_][A-Za-z0-9_.-]*(,[A-Za-z0-9_][A-Za-z0-9_.-]*)*$ ]]; then
  echo 'Aufruf: scripts/run_host_updates.sh --limit HOST[,HOST...] (Inventory-Hostnamen, keine Gruppen/Muster)' >&2
  exit 2
fi
target_limit=$2
for dependency in ansible-playbook flock awk sort; do
  command -v "${dependency}" >/dev/null || { echo "Fehlt: ${dependency}" >&2; exit 2; }
done
for required in ansible.cfg lib/control/helpers.sh playbooks/maintenance/update_hosts.yaml playbooks/maintenance/notify.yml; do
  [[ -r "${required}" ]] || { echo "Fehlt: ${required}" >&2; exit 2; }
done
mkdir -p logs
exec 9>"${ROOT_DIR}/logs/host-updates.lock"
flock -n 9 || { echo 'Host-Update laeuft bereits; dieser Aufruf wird abgebrochen.' >&2; exit 75; }
export CONTROL_PROJECT_ROOT="${ROOT_DIR}"
source "${ROOT_DIR}/lib/control/helpers.sh"

# Verify exact resolution inside the existing playbook's all_linux_systems scope.
# Ansible otherwise reports success even if a requested host does not exist.
if host_listing=$(ansible-playbook playbooks/maintenance/update_hosts.yaml --limit "${target_limit}" --list-hosts </dev/null); then
  resolved=$(printf '%s\n' "${host_listing}" | awk '/^    hosts \([0-9]+\):/ {active=1; next} active && /^      [^ ]/ {print $1}')
  requested=$(printf '%s\n' "${target_limit//,/$'\n'}" | sort -u)
  actual=$(printf '%s\n' "${resolved}" | sort -u)
  if [[ -n "${resolved}" && "${requested}" == "${actual}" ]]; then
    # Existing helper retains Ansible's exit status and sends the existing
    # Telegram notification without passing the host limit to localhost.
    run_playbook_notified host-updates "Systemupdate: ${target_limit}" \
      playbooks/maintenance/update_hosts.yaml --limit "${target_limit}" \
      --extra-vars '{"host_updates_reboot": true}' </dev/null
    exit $?
  fi
  echo 'Zielauswahl stimmt nicht exakt mit den Linux-Hosts im Inventory ueberein.' >&2
else
  echo 'Inventory-/Playbook-Vorpruefung fehlgeschlagen.' >&2
fi

notification_file=$(mktemp)
trap 'rm -f "${notification_file}"' EXIT
printf 'Systemupdate: %s\nStatus: ❌ FEHLER bei Zielpruefung; kein Update gestartet.\nController-Ausgabe/Cronlog pruefen.\n' "${target_limit}" > "${notification_file}"
if [[ -f config/script_jobs_controller.json ]]; then
  record_control_failure ansible:host-updates Zielauswahl 'Inventory- oder Zielpruefung fehlgeschlagen; kein Update gestartet.'
else
  ansible-playbook playbooks/maintenance/notify.yml -e "notification_file=${notification_file}" </dev/null || true
fi
exit 2
