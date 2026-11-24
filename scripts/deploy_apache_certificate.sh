#!/usr/bin/env bash
set -euo pipefail

project_root="${ANSIBLE_PROJECT_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)}"
certificate_root="${APACHE_CERTIFICATE_ROOT:?Bitte das lokale Zertifikatsverzeichnis angeben}"
playbook="${project_root}/playbooks/pki/deploy_apache_certificate.yml"

if [[ "${EUID}" -ne 0 ]]; then
  echo "Dieses Skript muss als root auf dem Ansible-Controller laufen." >&2
  exit 1
fi

if [[ ! -f "${playbook}" ]]; then
  echo "Playbook nicht gefunden: ${playbook}" >&2
  exit 1
fi

if [[ ! -d "${certificate_root}" ]]; then
  echo "Zertifikatsroot nicht gefunden: ${certificate_root}" >&2
  exit 1
fi

certificate_directories=()
while IFS= read -r -d '' record; do
  directory="${record#* }"
  [[ -f "${directory}/intermediate1.crt" ]] || continue
  [[ -f "${directory}/wildcard_example_org.key" ]] || continue
  certificate_directories+=("${directory}")
done < <(
  find "${certificate_root}" -mindepth 2 -maxdepth 2 \
    -type f -name certificate.crt -printf '%T@ %h\0' \
    | sort -z -nr
)

if [[ "${#certificate_directories[@]}" -eq 0 ]]; then
  echo "Keine vollstaendigen Zertifikatssaetze unter ${certificate_root} gefunden." >&2
  exit 1
fi

echo "Verfuegbare Zertifikatssaetze, neuestes certificate.crt zuerst:"
for index in "${!certificate_directories[@]}"; do
  directory="${certificate_directories[$index]}"
  changed="$(stat -c '%y' "${directory}/certificate.crt")"
  printf '  [%d] %s | %s\n' "$((index + 1))" "${changed}" "${directory}"
done

read -r -p "Auswahl [1-${#certificate_directories[@]}]: " selection
if [[ ! "${selection}" =~ ^[0-9]+$ ]] \
  || (( selection < 1 || selection > ${#certificate_directories[@]} )); then
  echo "Ungueltige Auswahl." >&2
  exit 1
fi

selected_directory="${certificate_directories[$((selection - 1))]}"
certificate_year="$(basename "${selected_directory}")"
encrypted_key="${selected_directory}/wildcard_example_org.key"
decrypted_key="${selected_directory}/wildcard_example_org_unencrypted.key"

echo "Ausgewaehlt: ${selected_directory}"

if [[ ! -f "${decrypted_key}" || "${encrypted_key}" -nt "${decrypted_key}" ]]; then
  temporary_key="${decrypted_key}.tmp"
  trap 'rm -f "${temporary_key:-}"' EXIT
  umask 077
  echo "Der private Schluessel wird einmalig entschluesselt."
  openssl pkey -in "${encrypted_key}" -out "${temporary_key}"
  openssl pkey -in "${temporary_key}" -noout -check
  chown root:root "${temporary_key}"
  chmod 0600 "${temporary_key}"
  mv "${temporary_key}" "${decrypted_key}"
  trap - EXIT
else
  echo "Vorhandener entschluesselter Schluessel wird verwendet: ${decrypted_key}"
fi

cd "${project_root}"
exec ansible-playbook "${playbook}" \
  --extra-vars "apache_certificate_root=${certificate_root}" \
  --extra-vars "apache_certificate_year=${certificate_year}" \
  "$@"
