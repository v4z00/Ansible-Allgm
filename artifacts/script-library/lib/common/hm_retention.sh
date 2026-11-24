hm_retention() {
    local directory="${1:?directory required}" days="${2:?days required}" pattern="${3:?pattern required}"
    [[ "$directory" == /* && "$directory" != / && -d "$directory" ]] || return 64
    [[ "$days" =~ ^[0-9]+$ && "$pattern" != */* && "$pattern" != '*' && "$pattern" != -* ]] || return 64
    find "$directory" -maxdepth 1 -type f -name "$pattern" -mtime +"$days" -delete
}
