# Set by entry points after resolving their project directory.
if [[ -x "$ROOT_DIR/.venv/bin/python3" ]]; then
  export PATH="$ROOT_DIR/.venv/bin:$PATH"
fi
if [[ -f "$ROOT_DIR/ansible.cfg" ]]; then
  export ANSIBLE_CONFIG="$ROOT_DIR/ansible.cfg"
fi
