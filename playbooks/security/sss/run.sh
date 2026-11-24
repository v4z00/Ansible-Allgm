#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
# Kein Inventory des übrigen Projekts verwenden; nur der lokale Ansible-Host.
bash files/install-voraussetzungen.sh --ansible
become_args=()
if (( EUID != 0 )); then
  if command -v sudo >/dev/null 2>&1; then
    if ! sudo -n true 2>/dev/null; then
      become_args+=(--ask-become-pass)
    fi
  elif command -v su >/dev/null 2>&1; then
    become_args+=(--become-method=su --ask-become-pass)
  else
    printf 'Admin-Rechte erforderlich, aber weder sudo noch su vorhanden.\n' >&2
    exit 1
  fi
fi
ansible-playbook -i localhost, -c local setup.yml "${become_args[@]}" "$@"
printf '\nVorbereitung fertig. Schlüssel werden separat interaktiv erzeugt:\n'
printf 'bash start-generator.sh\n'
