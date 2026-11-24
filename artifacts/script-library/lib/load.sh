# Source this loader from a path relative to the entry script, never the cwd.
HM_LIB_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)" || return
for hm_function_file in "$HM_LIB_DIR"/common/*.sh; do
    . "$hm_function_file" || return
 done
unset hm_function_file
