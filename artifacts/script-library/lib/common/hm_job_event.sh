hm_job_event() {
    [[ -n "${HM_JOB_RUN_ID:-}" && -n "${HM_JOB_HELPER:-}" ]] || return 0
    "${HM_JOB_HELPER}" --db "${HM_JOB_DB:?}" event --run "$HM_JOB_RUN_ID" --message "${1-}" >/dev/null
}
