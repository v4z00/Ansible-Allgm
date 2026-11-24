hm_send_mail() {
    [[ "${HM_JOB_MANAGED:-0}" != 1 ]] || return 0
    local subject="${1:?subject required}" body="${2-}" recipient="${3:-${EMAIL:-${MAIL_TO:-}}}"
    local ascii_subject ascii_body mail_cmd
    [[ -n "$recipient" ]] || return 0
    case "$recipient" in -*|*$'\n'*|*$'\r'*) printf '%s\n' 'Invalid mail recipient' >&2; return 64 ;; esac
    ascii_subject=$(printf '%s' "$subject" | hm_mail_ascii) || return
    ascii_subject=${ascii_subject//$'\n'/ }
    ascii_subject=${ascii_subject//$'\r'/ }
    ascii_body=$(printf '%s' "$body" | hm_mail_ascii) || return
    if mail_cmd=$(type -P mail); then :
    elif mail_cmd=$(type -P mailx); then :
    else printf '%s\n' 'Mail command unavailable' >&2; return 69; fi
    printf '%s\n' "$ascii_body" | "$mail_cmd" -s "$ascii_subject" "$recipient"
}
