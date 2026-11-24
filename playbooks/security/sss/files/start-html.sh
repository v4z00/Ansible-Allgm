#!/usr/bin/env bash
# Zusammen mit recover.py und notfall_entschluesselung.html aufbewahren.
set -euo pipefail
umask 077
if [[ "$(uname -s)" == Darwin ]]; then
  export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
fi

case "${1:-}" in
  -h|--help)
    printf 'Start: bash start-html.sh [--no-browser]\nBeenden: Strg+C im geöffneten Terminal.\n'
    exit 0
    ;;
  ''|--no-browser) ;;
  *) printf 'Unbekannte Option. Hilfe: bash start-html.sh --help\n' >&2; exit 2 ;;
esac
if (( $# > 1 )); then
  printf 'Zu viele Argumente. Hilfe: bash start-html.sh --help\n' >&2
  exit 2
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
for filename in recover.py notfall_entschluesselung.html install-voraussetzungen.sh; do
  if [[ ! -r "$script_dir/$filename" ]]; then
    printf 'Datei fehlt oder ist nicht lesbar: %s\n' "$script_dir/$filename" >&2
    printf 'Alle vier Werkzeugdateien müssen im selben Ordner liegen.\n' >&2
    exit 1
  fi
done
bash "$script_dir/install-voraussetzungen.sh"

printf 'SSS-Notfallhilfe: Infrastruktur (2 Personen) / Vaultwarden-Master (3 Personen)\n'
printf 'Dieses Terminal geöffnet lassen. Beenden mit Strg+C.\n\n'
if [[ "${1:-}" == '--no-browser' ]]; then
  exec python3 "$script_dir/recover.py" --web
fi
exec python3 "$script_dir/recover.py" --web --open-browser
