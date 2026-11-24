hm_send_telegram() {
    local message="${1-}" token="${BOT_TOKEN:-${TELEGRAM_BOT_TOKEN:-${TELEGRAM_TOKEN:-}}}"
    local chat="${CHAT_ID:-${TELEGRAM_CHAT_ID:-}}" result rc
    local -a options
    [[ -n "$token" || -n "$chat" ]] || return 0
    [[ -n "$token" && -n "$chat" ]] || { printf '%s\n' 'Incomplete Telegram configuration' >&2; return 78; }
    [[ "$token" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]] || { printf '%s\n' 'Invalid Telegram token format' >&2; return 64; }
    [[ "$chat" != *$'\n'* && "$chat" != *$'\r'* ]] || return 64
    # curl reads the URL/token from stdin, not from its process arguments.
    options=(--fail --silent --show-error --connect-timeout 10 --max-time 30
        --request POST --config - --data-urlencode "chat_id=$chat" --data-urlencode "text=$message")
    [[ -z "${TELEGRAM_PARSE_MODE:-}" ]] || options+=(--data-urlencode "parse_mode=$TELEGRAM_PARSE_MODE")
    result=$(printf 'url = "https://api.telegram.org/bot%s/sendMessage"\n' "$token" | curl "${options[@]}" 2>/dev/null)
    rc=$?
    if (( rc != 0 )); then printf '%s\n' 'Telegram transport failed' >&2; return "$rc"; fi
    printf '%s' "$result" | python3 -c 'import json,sys
try: ok=json.load(sys.stdin).get("ok") is True
except (ValueError,AttributeError): ok=False
sys.exit(0 if ok else 1)' || { printf '%s\n' 'Telegram API rejected message' >&2; return 1; }
}
