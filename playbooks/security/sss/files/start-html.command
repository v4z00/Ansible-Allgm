#!/bin/bash
# macOS: Doppelklick im Finder oder bash start-html.command
set -uo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)" || exit 1
bash "$script_dir/start-html.sh" "$@"
result=$?
if (( result != 0 && result != 130 )); then
  printf '\nStart fehlgeschlagen. Hinweise oben lesen. Enter schließt dieses Fenster.\n'
  read -r _
fi
exit "$result"
