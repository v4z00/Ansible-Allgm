#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

failed=0
check_command() {
  if command -v "$1" >/dev/null 2>&1; then
    printf 'OK   Kommando: %s\n' "$1"
  else
    printf 'FEHLT Kommando: %s\n' "$1" >&2
    failed=1
  fi
}

check_command python3
check_command ansible
check_command ansible-playbook
check_command ansible-inventory
check_command ansible-galaxy

if python3 -c 'import yaml' >/dev/null 2>&1; then
  printf 'OK   Python-Modul: yaml\n'
else
  printf 'FEHLT Python-Modul: yaml (Paket PyYAML/python3-yaml)\n' >&2
  failed=1
fi

for link in inventory/group_vars inventory/host_vars; do
  if [[ -L "${link}" && -e "${link}" ]]; then
    printf 'OK   Variablenpfad: %s -> %s\n' "${link}" "$(readlink "${link}")"
  else
    printf 'FEHLT Variablenpfad: %s\n' "${link}" >&2
    failed=1
  fi
done

if [[ -f group_vars/all/secrets.yml ]]; then
  secret_mode="$(stat -f '%Lp' group_vars/all/secrets.yml 2>/dev/null || stat -c '%a' group_vars/all/secrets.yml)"
  if [[ "${secret_mode}" == 600 ]]; then
    printf 'OK   Secret-Dateimodus: 0600\n'
  else
    printf 'FEHLER Secret-Dateimodus: %s statt 0600\n' "${secret_mode}" >&2
    failed=1
  fi
else
  printf 'HINWEIS group_vars/all/secrets.yml fehlt; ohne benoetigte Secrets ist das zulaessig.\n'
fi

if (( failed != 0 )); then
  exit 1
fi

ansible-inventory -i inventory --playbook-dir "${ROOT_DIR}" --graph
"${ROOT_DIR}/bin/control" syntax
