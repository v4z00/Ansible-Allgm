#!/usr/bin/env bash
# Installiert nur fehlende Voraussetzungen über die Paketquellen des Systems.
set -euo pipefail
umask 077
# Finder-Terminals enthalten Homebrew nicht immer im PATH.
if [[ "$(uname -s)" == Darwin ]]; then
  export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
fi
case "${1:-}" in
  '') ;;
  --ansible) ;;
  -h|--help)
    printf 'bash install-voraussetzungen.sh [--ansible]\nFehlende Pakete: python3, ssss; optional ansible-core.\n'
    exit 0 ;;
  *) printf 'Unbekannte Option. --help zeigt die Hilfe.\n' >&2; exit 2 ;;
esac
(( $# <= 1 )) || { printf 'Zu viele Argumente.\n' >&2; exit 2; }

packages=()
command -v python3 >/dev/null 2>&1 || packages+=(python3)
if ! command -v ssss-combine >/dev/null 2>&1 || ! command -v ssss-split >/dev/null 2>&1; then
  packages+=(ssss)
fi
if [[ "${1:-}" == '--ansible' ]] && ! command -v ansible-playbook >/dev/null 2>&1; then
  packages+=(ansible-core)
fi
if (( ${#packages[@]} == 0 )); then
  printf 'Alle Voraussetzungen sind vorhanden.\n'
  exit 0
fi
if [[ "$(uname -s)" == Darwin ]]; then
  if (( EUID == 0 )); then
    printf 'macOS: Bitte den Starter als normaler Benutzer ohne sudo ausführen. Homebrew fragt nötige Rechte selbst ab.\n' >&2
    exit 1
  fi
  if ! command -v brew >/dev/null 2>&1; then
    printf 'Homebrew fehlt. Der offizielle Installer wird geladen und fragt nötige Admin-Rechte ab.\n'
    brew_installer="$(mktemp -t sss-homebrew)"
    trap 'rm -f -- "$brew_installer"' EXIT
    curl --fail --silent --show-error --location https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh -o "$brew_installer"
    /bin/bash "$brew_installer"
  fi
  command -v brew >/dev/null 2>&1 || { printf 'Homebrew-Installation nicht abgeschlossen.\n' >&2; exit 1; }
  brew_packages=()
  for package in "${packages[@]}"; do
    case "$package" in
      python3) brew_packages+=(python) ;;
      ansible-core) brew_packages+=(ansible) ;;
      *) brew_packages+=("$package") ;;
    esac
  done
  brew install "${brew_packages[@]}"
  printf 'macOS-Voraussetzungen installiert.\n'
  exit 0
fi
if [[ ! -r /etc/os-release ]]; then
  printf 'Automatische Installation wird nur auf Debian/Ubuntu unterstützt.\n' >&2
  exit 1
fi
. /etc/os-release
case " ${ID:-} ${ID_LIKE:-} " in
  *' debian '*|*' ubuntu '*) ;;
  *) printf 'Bitte die Voraussetzungen auf diesem System manuell installieren; automatisch unterstützt: Debian/Ubuntu.\n' >&2; exit 1 ;;
esac
command -v apt-get >/dev/null 2>&1 || { printf 'apt-get fehlt.\n' >&2; exit 1; }
printf 'Fehlende Pakete werden installiert: %s\n' "${packages[*]}"
printf 'Dafür werden erreichbare Paketquellen und Admin-Rechte benötigt.\n'
script_path="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)/$(basename -- "${BASH_SOURCE[0]}")"
if (( EUID != 0 )); then
  if command -v sudo >/dev/null 2>&1; then
    exec sudo -- /bin/bash "$script_path" "$@"
  elif command -v su >/dev/null 2>&1; then
    printf 'sudo fehlt. Bitte im folgenden Dialog das root-Passwort eingeben.\n'
    printf -v root_command '%q ' /bin/bash "$script_path" "$@"
    exec su -s /bin/bash -c "$root_command" root
  else
    printf 'Weder sudo noch su vorhanden. Installation durch Administrator erforderlich.\n' >&2
    exit 1
  fi
fi
apt-get update
apt-get install -y -- "${packages[@]}"
printf 'Voraussetzungen installiert.\n'
