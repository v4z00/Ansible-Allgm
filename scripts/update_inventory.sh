#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

case "${1:-}" in
  '') mode=update ;;
  --check) mode=check ;;
  *) echo 'Aufruf: scripts/update_inventory.sh [--check]' >&2; exit 2 ;;
esac

args=(--root "${ROOT_DIR}")
[[ "${mode}" == check ]] && args+=(--check)
[[ "${mode}" == update && -t 0 && -t 1 ]] && args+=(--interactive)

python3 scripts/generate_inventory.py "${args[@]}"
ansible-inventory -i inventory --graph

