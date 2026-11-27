# Read a structured JSON alert from stdin. Never pass notification text as arguments.
hm_security_alert() {
    local event_key=${1:?stable event key required}
    local configuration=${2:-${HM_SECURITY_CONFIG:-${HM_JOB_DB%/*}/config/security.json}}
    "${HM_JOB_HELPER:?job helper required}" --db "${HM_JOB_DB:?job database required}" \
        security-alert --event-id "$event_key" --config "$configuration"
}
