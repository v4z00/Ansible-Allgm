#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from pathlib import Path
import subprocess
import yaml

for file in sorted(Path("playbooks").rglob("*")):
    if file.suffix not in (".yaml", ".yml") or {"tasks", "vars"}.intersection(file.parts):
        continue
    data = yaml.safe_load(file.read_text())
    if not isinstance(data, list):
        continue
    if any(isinstance(item, dict) and {"hosts", "import_playbook", "ansible.builtin.import_playbook"}.intersection(item) for item in data):
        subprocess.run(["ansible-playbook", "--syntax-check", str(file)], check=True)
PY
