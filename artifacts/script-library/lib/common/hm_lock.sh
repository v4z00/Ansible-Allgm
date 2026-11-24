# Call in the script process, not a command substitution; FD 9 holds the lock.
hm_lock() {
    local path="${1:?lock path required}"
    exec 9>"$path" || return
    flock -n 9
}
