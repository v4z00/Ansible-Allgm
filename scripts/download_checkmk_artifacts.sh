#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

read_settings_json() {
  python3 - <<'PY'
import json, os, yaml
with open('group_vars/all/settings.yml', encoding='utf-8') as handle:
    data = yaml.safe_load(handle)
tls = data.get('tls_validate_certs', {})
if not isinstance(tls, dict):
    raise SystemExit('tls_validate_certs muss eine YAML-Zuordnung sein.')
for key in ('checkmk_agent_download', 'checkmk_plugin_download'):
    if key in tls and not isinstance(tls[key], bool):
        raise SystemExit('tls_validate_certs.' + key + ' muss true oder false sein.')
default_validate = data.get('tls_validate_certs_default', True)
if not isinstance(default_validate, bool):
    raise SystemExit('tls_validate_certs_default muss true oder false sein.')
legacy = os.environ.get('CHECKMK_DOWNLOAD_INSECURE', '0')
if legacy not in ('0', '1'):
    raise SystemExit('CHECKMK_DOWNLOAD_INSECURE muss 0 oder 1 sein.')
print(json.dumps({
    'base': data.get('checkmk_download_base_url', '').rstrip('/'),
    'version': data.get('checkmk_agent_version', ''),
    'plugins': data.get('checkmk_linux_plugins', []),
    'agent_validate': tls.get('checkmk_agent_download', False if legacy == '1' else default_validate),
    'plugin_validate': tls.get('checkmk_plugin_download', False if legacy == '1' else default_validate),
}))
PY
}

settings_json=$(read_settings_json)
base_url=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["base"])' <<<"${settings_json}")
version=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["version"])' <<<"${settings_json}")

[[ -n "${base_url}" ]] || { echo 'checkmk_download_base_url fehlt.' >&2; exit 1; }
[[ -n "${version}" ]] || { echo 'checkmk_agent_version fehlt.' >&2; exit 1; }

agent_curl_args=(--fail --location --show-error)
plugin_curl_args=(--fail --location --show-error)
agent_validate=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["agent_validate"])' <<<"${settings_json}")
plugin_validate=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["plugin_validate"])' <<<"${settings_json}")
if [[ "${agent_validate}" == False ]]; then
  agent_curl_args+=(--insecure)
  echo 'Hinweis: TLS-Zertifikatspruefung fuer Agent-Download deaktiviert.' >&2
fi
if [[ "${plugin_validate}" == False ]]; then
  plugin_curl_args+=(--insecure)
  echo 'Hinweis: TLS-Zertifikatspruefung fuer Plugin-Downloads deaktiviert.' >&2
fi

mkdir -p artifacts/checkmk/plugins
agent_name="check-mk-agent_${version}-1_all.deb"
curl "${agent_curl_args[@]}" \
  "${base_url}/${agent_name}" \
  -o artifacts/checkmk/check-mk-agent.deb
chmod 0600 artifacts/checkmk/check-mk-agent.deb

while IFS= read -r plugin; do
  [[ -n "${plugin}" ]] || continue
  curl "${plugin_curl_args[@]}" \
    "${base_url}/plugins/${plugin}" \
    -o "artifacts/checkmk/plugins/${plugin}"
  chmod 0755 "artifacts/checkmk/plugins/${plugin}"
done < <(python3 -c 'import json,sys; print("\n".join(json.load(sys.stdin)["plugins"]))' <<<"${settings_json}")

echo "CheckMK-Agent und Plugins wurden unter ${ROOT_DIR}/artifacts/checkmk gespeichert."
