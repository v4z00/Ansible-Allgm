send_email() {
    case "${ENABLE_EMAIL_NOTIFICATION:-yes}" in no|false|0) return 0 ;; esac
    local body
    body=$(printf '%b' "${2-}")
    hm_send_mail "${1:-Status}" "$body" "${EMAIL:-${MAIL_TO:-}}"
}
