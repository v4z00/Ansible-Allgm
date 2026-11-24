hm_check_mount() {
    local path="${1:?path required}" target
    [[ -d "$path" ]] || return 1
    target=$(findmnt --noheadings --raw --output TARGET --target "$path" 2>/dev/null) || return 1
    [[ -n "$target" && "$target" != / ]]
}
