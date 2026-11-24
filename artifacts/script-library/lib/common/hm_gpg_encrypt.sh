hm_gpg_encrypt() {
    local source="${1:?source required}" destination="${2:?destination required}" keyfile="${3:-}"
    [[ -f "$source" ]] || return 1
    if [[ -z "$keyfile" ]]; then
        [[ -n "${ENCRYPTION_PASSWORD:-${GPG_PASSWORD:-}}" ]] || return 78
        gpg --batch --yes --pinentry-mode loopback --passphrase-fd 3 \
            3<<<"${ENCRYPTION_PASSWORD:-$GPG_PASSWORD}" --symmetric --cipher-algo AES256 --output "$destination" "$source"
        return $?
    fi
    [[ -s "$keyfile" ]] || return 1
    gpg --batch --yes --pinentry-mode loopback --passphrase-file "$keyfile" \
        --symmetric --cipher-algo AES256 --output "$destination" "$source"
}
