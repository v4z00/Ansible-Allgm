# ROOT_DIR points to the installed controller. Arguments after KEY are name=value.
controller_tr() {
  "${CONTROLLER_PYTHON:-python3}" -B "$ROOT_DIR/scripts/controller_i18n.py" "$@"
}
