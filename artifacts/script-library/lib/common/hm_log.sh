hm_log() {
    local level="${1:-INFO}" message="${2-}" file="${LOG_FILE:-${LOGFILE:-}}" line
    line="[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
    hm_job_event "$level: $message" || return
    if [[ -n "$file" ]]; then
        printf '%s\n' "$line" | tee -a "$file"
    else printf '%s\n' "$line"; fi
}
