hm_job_item() {
    [[ -n "${HM_JOB_RUN_ID:-}" && -n "${HM_JOB_HELPER:-}" ]] || return 0
    "${HM_JOB_HELPER}" --db "${HM_JOB_DB:?}" item --run "$HM_JOB_RUN_ID" --item "${1:?item required}" \
        --status "${2:?status required}" --message "${3-}" >/dev/null
}
