#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${CONTROL_PROJECT_ROOT:?}"
cd "${ROOT_DIR}"
LOG_DIR="${ROOT_DIR}/logs"

run_playbook_logged() {
  local category=$1
  local playbook=$2
  shift 2
  local log_file
  mkdir -p "${LOG_DIR}"
  log_file="${LOG_DIR}/${category}-$(date -u +'%Y%m%dT%H%M%SZ').log"
  printf 'Log: %s\n' "${log_file}"
  ANSIBLE_LOG_PATH="${log_file}" ansible-playbook "${playbook}" "$@"
}

run_playbook_notified() {
  local category=$1
  local label=$2
  local playbook=$3
  shift 3
  local log_file notification_file status result

  mkdir -p "${LOG_DIR}"
  log_file="${LOG_DIR}/${category}-$(date -u +'%Y%m%dT%H%M%SZ').log"
  notification_file=$(mktemp)
  printf 'Log: %s\n' "${log_file}"

  if ANSIBLE_LOG_PATH="${log_file}" ansible-playbook "${playbook}" "$@"; then
    status=0
    result=ERFOLGREICH
  else
    status=$?
    result="FEHLERHAFT (Exit ${status})"
  fi

  printf '%s\nStatus: %s\nLog: %s\n' "${label}" "${result}" "${log_file}" > "${notification_file}"
  if [[ -f playbooks/maintenance/notify.yml ]] && ! ansible-playbook playbooks/maintenance/notify.yml \
      -e "notification_file=${notification_file}"; then
    [[ ${status} -ne 0 ]] || status=1
  fi
  rm -f "${notification_file}"
  return "${status}"
}

run_base() {
  local explicit_all=false has_limit=false
  local -a playbook_args=()

  while (($#)); do
    case "$1" in
      --all)
        explicit_all=true
        ;;
      --limit|-l)
        has_limit=true
        playbook_args+=("$1")
        shift
        [[ $# -gt 0 ]] || {
          echo 'Fehler: Hinter --limit/-l fehlt das Ziel.' >&2
          return 2
        }
        playbook_args+=("$1")
        ;;
      --limit=*)
        has_limit=true
        playbook_args+=("$1")
        ;;
      *)
        playbook_args+=("$1")
        ;;
    esac
    shift
  done

  if [[ "${explicit_all}" == true && "${has_limit}" == true ]]; then
    echo 'Fehler: Fuer base entweder --limit ZIEL oder --all verwenden, nicht beides.' >&2
    return 2
  fi
  if [[ "${explicit_all}" == false && "${has_limit}" == false ]]; then
    cat >&2 <<'EOF'
Sicherheitsstopp: base benoetigt ein ausdrueckliches Ziel.
  Einzelner Host: bin/control base --limit example-host
  Hostgruppe:      bin/control base --limit all_linux_systems
  Bewusst alle:    bin/control base --all
EOF
    return 2
  fi

  run_playbook_logged base playbooks/base.yml "${playbook_args[@]}"
}

ask_yes_no() {
  local prompt=$1 answer
  read -r -p "${prompt} [y/N]: " answer
  [[ "${answer}" =~ ^([yY]|[yY][eE][sS])$ ]]
}

docker_deploy() {
  local deploy_all=false deploy_networks=false deploy_users=false
  if [[ "${1:-}" == "--all" ]]; then
    deploy_all=true
    shift
  elif [[ ! -t 0 ]]; then
    deploy_all=true
  fi
  if [[ "${deploy_all}" == true ]]; then
    deploy_networks=true
    deploy_users=true
  else
    ask_yes_no 'Neue Netzwerke oder Host-Konfigurationen ausrollen?' && deploy_networks=true
    ask_yes_no 'Docker-Service-Accounts erstellen oder aktualisieren?' && deploy_users=true
  fi

  run_playbook_logged docker-prepare playbooks/docker/prepare_deployment.yml "$@"
  [[ "${deploy_users}" == false ]] || run_playbook_logged docker-users playbooks/docker/deploy_docker_users.yml "$@"
  [[ "${deploy_networks}" == false ]] || run_playbook_logged docker-networks playbooks/docker/deploy_docker_networks.yaml "$@"
  run_playbook_logged docker-stacks playbooks/docker/deploy_docker_stacks.yml "$@"
}

show_last_log() {
  local pattern="${1:-*}"
  local latest
  [[ -d "${LOG_DIR}" ]] || { echo "Noch kein Logverzeichnis vorhanden." >&2; return 1; }
  latest=$(find "${LOG_DIR}" -maxdepth 1 -type f -name "${pattern}*.log" -exec ls -1t {} + 2>/dev/null | awk 'NR == 1 { first = $0 } END { print first }')
  [[ -n "${latest}" ]] || { echo "Kein passendes Log gefunden." >&2; return 1; }
  cat "${latest}"
}

