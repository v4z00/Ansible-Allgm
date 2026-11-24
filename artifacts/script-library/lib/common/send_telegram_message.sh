send_telegram_message() {
    case "${ENABLE_TELEGRAM_NOTIFICATION:-yes}" in no|false|0) return 0 ;; esac
    local message
    message=$(printf '%b' "${1-}")
    hm_send_telegram "$message"
}
