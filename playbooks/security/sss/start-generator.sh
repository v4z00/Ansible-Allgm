#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
bash "$script_dir/files/install-voraussetzungen.sh"
printf 'Generator auf dem Ansible-Host starten; Admin-Rechte für /root/rescue erforderlich.\n'
if (( EUID == 0 )); then
  exec /usr/bin/python3 /root/rescue/SSS/bin/generate.py "$@"
elif command -v sudo >/dev/null 2>&1; then
  exec sudo -- /usr/bin/python3 /root/rescue/SSS/bin/generate.py "$@"
elif command -v su >/dev/null 2>&1; then
  printf 'Bitte das root-Passwort eingeben.\n'
  printf -v root_command '%q ' /usr/bin/python3 /root/rescue/SSS/bin/generate.py "$@"
  exec su -s /bin/bash -c "$root_command" root
else
  printf 'Weder sudo noch su vorhanden. Bitte den Administrator hinzuziehen.\n' >&2
  exit 1
fi
