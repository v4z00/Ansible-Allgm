hm_job_query() {
    local helper="${HM_JOB_HELPER:-${HM_LIB_DIR:?}/../bin/script-jobs}"
    "$helper" --db "${HM_JOB_DB:-/var/lib/script-jobs/jobs.sqlite3}" "$@"
}
