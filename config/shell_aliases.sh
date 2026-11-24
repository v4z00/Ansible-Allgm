#!/usr/bin/env bash
# Ansible Command Center fuer Bash und Zsh.
# Wird von der verwalteten ~/.bashrc geladen.
# Die verwaltete ~/.zshrc laedt anschliessend ebenfalls ~/.bashrc.

export ANSIBLE_PROJECT_ROOT="${ANSIBLE_PROJECT_ROOT:-/root/ansible}"
export ANSIBLE_ALIASES_FILE="${ANSIBLE_ALIASES_FILE:-${ANSIBLE_PROJECT_ROOT}/config/shell_aliases.sh}"

# Alte Definitionen aus der bisherigen ~/.bashrc koennen in Zsh beim Parsen
# gleichnamiger Funktionen expandiert werden (z. B. `alias reload=...`).
# Vor dem erneuten Laden deshalb nur die von dieser Datei verwalteten
# Funktionsnamen als Aliase entfernen. Bereits vorhandene Funktionen werden
# durch die folgenden Definitionen sauber ersetzt.
unalias control ansible-cd ansible-status host-info group-show log-show \
    ansible-run my-help myhelp docker-push audit-crons reload edit-alias git-save \
    2>/dev/null || true

# Benutzerlokale pipx-Programme verfuegbar machen, ohne PATH-Eintraege zu doppeln.
case ":${PATH}:" in
    *:"${HOME}/.local/bin":*) ;;
    *) export PATH="${PATH}:${HOME}/.local/bin" ;;
esac

# help: Zentrale Steuerung aufrufen: control BEFEHL [Optionen]
control() {
    if [[ ! -f "${ANSIBLE_PROJECT_ROOT}/bin/control" ]]; then
        echo "Fehler: ${ANSIBLE_PROJECT_ROOT}/bin/control wurde nicht gefunden." >&2
        return 1
    fi
    bash "${ANSIBLE_PROJECT_ROOT}/bin/control" "$@"
}

_control_commands() { control list; }

# help: In das Ansible-Projekt wechseln
ansible-cd() {
    cd "${ANSIBLE_PROJECT_ROOT}" || return
}

# help: Git-Status des Ansible-Projekts anzeigen
ansible-status() {
    (cd "${ANSIBLE_PROJECT_ROOT}" && git status --short --branch)
}

# help: Sichere Kerninformationen eines Inventory-Hosts anzeigen: host-info HOST
host-info() {
    local host=${1:-}
    [[ -n "${host}" ]] || { echo "Aufruf: host-info HOST" >&2; return 2; }
    command -v jq >/dev/null 2>&1 || { echo "Fehler: jq wird fuer die sichere Ausgabe benoetigt." >&2; return 1; }
    (
        cd "${ANSIBLE_PROJECT_ROOT}" || exit
        ansible-inventory -i inventory --list | jq --arg host "${host}" '
            . as $inventory
            | ($inventory._meta.hostvars[$host] // error("Host nicht gefunden: " + $host)) as $v
            | {
                inventory_hostname: $host,
                ansible_host: $v.ansible_host,
                ansible_user: $v.ansible_user,
                ansible_port: $v.ansible_port,
                inventory_os_family: $v.inventory_os_family,
                inventory_ip_source: $v.inventory_ip_source,
                proxmox_source: $v.proxmox_source,
                proxmox_node: $v.proxmox_node,
                proxmox_type: $v.proxmox_type,
                proxmox_vmid: $v.proxmox_vmid,
                proxmox_status: $v.proxmox_status,
                proxmox_tags: $v.proxmox_tags,
                script_path: $v.script_path,
                checkmk_hostname: $v.checkmk_hostname,
                checkmk_target_folder: $v.checkmk_target_folder,
                checkmk_device_type: $v.checkmk_device_type,
                groups: [
                    $inventory
                    | to_entries[]
                    | select(.key != "_meta")
                    | select((.value.hosts // []) | index($host))
                    | .key
                ]
            }
        '
    )
}

# help: Inventory oder einzelne Gruppe anzeigen: group-show [GRUPPE]
group-show() {
    local group=${1:-}
    if [[ -n "${group}" ]]; then
        (cd "${ANSIBLE_PROJECT_ROOT}" && ansible-inventory -i inventory --graph "${group}")
    else
        control graph
    fi
}

# help: Letztes Ausfuehrungslog anzeigen: log-show [MUSTER]
log-show() {
    control last-log "${1:-*}"
}

# help: Playbook per Pfad oder Namen starten: ansible-run PLAYBOOK [Optionen]
ansible-run() {
    local requested=${1:-}
    local playbook
    [[ -n "${requested}" ]] || { echo "Fehler: Bitte ein Playbook angeben." >&2; return 2; }
    shift

    if [[ -f "${requested}" ]]; then
        playbook="${requested}"
    elif [[ -f "${ANSIBLE_PROJECT_ROOT}/playbooks/maintenance/${requested}" ]]; then
        playbook="playbooks/maintenance/${requested}"
    elif [[ -f "${ANSIBLE_PROJECT_ROOT}/playbooks/${requested}" ]]; then
        playbook="playbooks/${requested}"
    else
        echo "Fehler: Playbook '${requested}' nicht gefunden." >&2
        return 1
    fi

    (cd "${ANSIBLE_PROJECT_ROOT}" && ansible-playbook "${playbook}" "$@")
}


# help: Kurzform fuer my-help
myhelp() {
    my-help
}


# help: Gesicherte Root-Crontabs nach Host gruppiert anzeigen
audit-crons() {
    local audit_dir=${1:-.}
    local file found=false
    while IFS= read -r file; do
        found=true
        printf '\n\033[1;33m=== HOST: %s ===\033[0m\n' "$(basename "$(dirname "${file}")")"
        cat "${file}"
    done < <(find "${audit_dir}" -mindepth 2 -maxdepth 2 -type f -name '*-root-crontab' -print 2>/dev/null | sort)
    [[ "${found}" == true ]] || echo "Keine gesicherten Root-Crontabs unter ${audit_dir} gefunden."
}

# help: Aliasdatei nach einer Aenderung neu laden
reload() {
    # shellcheck disable=SC1090
    source "${ANSIBLE_ALIASES_FILE}"
}

# help: Zentrale Ansible-Aliasdatei im Editor oeffnen
edit-alias() {
    "${EDITOR:-nano}" "${ANSIBLE_ALIASES_FILE}"
}

# help: Projektaenderungen interaktiv committen und pushen
git-save() {
    local message
    (cd "${ANSIBLE_PROJECT_ROOT}" && git add .) || return
    if [[ -z "$(cd "${ANSIBLE_PROJECT_ROOT}" && git status --porcelain)" ]]; then
        echo "Nichts zu tun."
        return 0
    fi
    (cd "${ANSIBLE_PROJECT_ROOT}" && git status --short)
    read -r -p "Commit-Nachricht: " message
    [[ -n "${message}" ]] || { echo "Abbruch: Keine Nachricht." >&2; return 1; }
    (cd "${ANSIBLE_PROJECT_ROOT}" && git commit -m "${message}" && git push)
}

# help: Verwaltete Bashrc installieren und aktuelle Shell neu laden
alias bashrc-install='install -m 0644 /root/ansible/config/bashrc /root/.bashrc && source /root/.bashrc'


# control-modules-v1: generated aliases from the command registry.
# help: Dynamische Hilfe aus der Befehlsregistry
my-help() {
    printf '\nAnsible Command Center\nProjekt: %s\n\nLokale Helfer\n' "$ANSIBLE_PROJECT_ROOT"
    control local-help || return
    printf '\nBefehle und Shortcuts\n'
    control help
    printf '\nAlle registrierten Befehle: control help-all\nModulstatus: control modules-check\n'
}
# Compute first: a malformed registry must not partially replace working aliases.
if _control_new_alias_code="$(control shell-init)"; then
    while IFS= read -r _control_old_alias; do
        [[ -z "$_control_old_alias" ]] || unalias "$_control_old_alias" 2>/dev/null || true
    done <<< "${_CONTROL_MANAGED_ALIASES:-}"
    while IFS= read -r _control_old_alias; do
        [[ -z "$_control_old_alias" ]] || unalias "$_control_old_alias" 2>/dev/null || true
    done < <(control alias-names)
    # The former docker-push wrapper is now a registered alias.
    unset -f docker-push 2>/dev/null || true
    eval "$_control_new_alias_code"
    _CONTROL_MANAGED_ALIASES="$(control alias-names)"
else
    printf 'Control-Module konnten nicht geladen werden.\n' >&2
fi
unset _control_old_alias _control_new_alias_code
