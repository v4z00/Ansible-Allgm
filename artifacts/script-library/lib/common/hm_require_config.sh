hm_require_config() {
    local name value failed=0
    for name in "$@"; do
        [[ "$name" =~ ^[A-Z][A-Z0-9_]*$ ]] || return 64
        value=${!name-}
        if [[ -z "$value" || "$value" == REDACTED || "$value" == CHANGEME || "$value" == '<'* ]]; then
            printf 'Missing configuration: %s\n' "$name" >&2
            failed=1
        fi
    done
    (( failed == 0 ))
}
