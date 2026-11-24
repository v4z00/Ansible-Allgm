# Compatibility for both old log_message MESSAGE and log_message LEVEL MESSAGE.
log_message() {
    local level=INFO message
    if (( $# > 1 )); then level=$1; message=$2; else message=${1-}; fi
    hm_log "$level" "$message" || return
    if [[ "${LOG_NOTIFY_ERRORS:-false}" == true && ( "$level" == ERROR || "$level" == CRITICAL ) ]]; then
        send_telegram_message "$message" || true
        send_email "${HOSTNAME:-Host} - $level" "$message" || true
    fi
}
