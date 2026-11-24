# Compatibility transport for legacy direct mail/mailx calls.
hm_mail_command() {
    [[ "${HM_JOB_MANAGED:-0}" != 1 ]] || return 0
    local requested="$1" argument expect_subject=false body binary
    shift
    local -a arguments
    binary=$(type -P "$requested") || binary=''
    if [[ -z "$binary" && "$requested" == mail ]]; then binary=$(type -P mailx) || binary=''; fi
    [[ -n "$binary" ]] || { printf '%s\n' 'Mail command unavailable' >&2; return 69; }
    arguments=()
    for argument in "$@"; do
        if [[ "$expect_subject" == true ]]; then
            argument=$(printf '%s' "$argument" | hm_mail_ascii) || return
            argument=${argument//$'\n'/ }; argument=${argument//$'\r'/ }
            expect_subject=false
        elif [[ "$argument" == -s ]]; then expect_subject=true; fi
        arguments+=("$argument")
    done
    body=$(hm_mail_ascii) || return
    printf '%s\n' "$body" | "$binary" "${arguments[@]}"
}
