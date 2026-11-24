#!/usr/bin/env bash
set -euo pipefail
CHECK_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONDONTWRITEBYTECODE=1
exec python3 "$CHECK_DIR/check.py" "$@"
