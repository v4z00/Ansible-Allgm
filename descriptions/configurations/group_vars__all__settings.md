# Konfigurationsreferenz group_vars/all/settings.yml

Diese Angaben beschreiben ausschliesslich die vorliegende Vorlagen-/Beispieldatei, nicht die effektiven Werte eines laufenden Hosts.

Die Datei wird durch diese Dokumentation weder aktiviert noch in bestehende Standortkonfigurationen kopiert.

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

Die optionalen Einstellungen für Berichte, Apache, Docker und Checkmk stehen in `examples/settings/controller_paths.example.yml`.

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "group_vars/all/settings.yml",
  "title": "Konfigurationsreferenz group_vars/all/settings.yml",
  "documented": false,
  "fields": [
    {
      "id": "controller_lang",
      "label": "Controller-Sprache",
      "description": "Sprache für Controllerbefehle und Berichte. Erlaubt sind de und en.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "de"
    },
    {
      "id": "site_id",
      "label": "site_id",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "template"
    },
    {
      "id": "site_name",
      "label": "site_name",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "Musterumgebung"
    },
    {
      "id": "site_managed_by",
      "label": "site_managed_by",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "IT-Administration"
    },
    {
      "id": "motd_show_hap",
      "label": "motd_show_hap",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "motd_hap",
      "label": "motd_hap",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "ansible_auth_mode",
      "label": "ansible_auth_mode",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "key_only"
    },
    {
      "id": "auth_method_description",
      "label": "auth_method_description",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "SSH-Schlüssel"
    },
    {
      "id": "managed_access_default_user",
      "label": "managed_access_default_user",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "root"
    },
    {
      "id": "managed_access_default_port",
      "label": "managed_access_default_port",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 22
    },
    {
      "id": "managed_access_default_become",
      "label": "managed_access_default_become",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "managed_access_default_become_method",
      "label": "managed_access_default_become_method",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "sudo"
    },
    {
      "id": "managed_access_default_become_user",
      "label": "managed_access_default_become_user",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "root"
    },
    {
      "id": "managed_host_access",
      "label": "managed_host_access",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "bootstrap_targets",
      "label": "bootstrap_targets",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "bootstrap_public_key_file",
      "label": "bootstrap_public_key_file",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "bootstrap_disable_password_auth_after_key",
      "label": "bootstrap_disable_password_auth_after_key",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false
    },
    {
      "id": "features.baseline",
      "label": "features.baseline",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "features.chrony",
      "label": "features.chrony",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "features.fail2ban",
      "label": "features.fail2ban",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "features.motd",
      "label": "features.motd",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "features.ssh_hardening",
      "label": "features.ssh_hardening",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "features.security_base",
      "label": "features.security_base",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "features.accounting",
      "label": "features.accounting",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "features.security_tools",
      "label": "features.security_tools",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "features.lynis",
      "label": "features.lynis",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "features.rsyslog",
      "label": "features.rsyslog",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "features.postfix",
      "label": "features.postfix",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "features.checkmk",
      "label": "features.checkmk",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "features.docker",
      "label": "features.docker",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "features.proxmox",
      "label": "features.proxmox",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "features.hyperv",
      "label": "features.hyperv",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "features.kerberos",
      "label": "features.kerberos",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "features.kerberos_keytabs",
      "label": "features.kerberos_keytabs",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false
    },
    {
      "id": "features.telegraf",
      "label": "features.telegraf",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "system_timezone",
      "label": "system_timezone",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "Europe/Berlin"
    },
    {
      "id": "chrony_ntp_servers",
      "label": "chrony_ntp_servers",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "base_packages",
      "label": "base_packages",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "fail2ban_ignoreip",
      "label": "fail2ban_ignoreip",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "fail2ban_bantime",
      "label": "fail2ban_bantime",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "1h"
    },
    {
      "id": "fail2ban_findtime",
      "label": "fail2ban_findtime",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "10m"
    },
    {
      "id": "fail2ban_maxretry",
      "label": "fail2ban_maxretry",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 5
    },
    {
      "id": "fail2ban_ssh_port",
      "label": "fail2ban_ssh_port",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "fail2ban_admin_email",
      "label": "fail2ban_admin_email",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "root@localhost"
    },
    {
      "id": "fail2ban_ticket_email",
      "label": "fail2ban_ticket_email",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "root@localhost"
    },
    {
      "id": "fail2ban_proxmox_ve_hosts",
      "label": "fail2ban_proxmox_ve_hosts",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "fail2ban_proxmox_backup_hosts",
      "label": "fail2ban_proxmox_backup_hosts",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "ssh_max_auth_tries",
      "label": "ssh_max_auth_tries",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 3
    },
    {
      "id": "ssh_max_sessions",
      "label": "ssh_max_sessions",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 10
    },
    {
      "id": "ssh_allow_tcp_forwarding",
      "label": "ssh_allow_tcp_forwarding",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "ssh_permit_root_login",
      "label": "ssh_permit_root_login",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "yes"
    },
    {
      "id": "ssh_client_alive_interval",
      "label": "ssh_client_alive_interval",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 300
    },
    {
      "id": "ssh_client_alive_count_max",
      "label": "ssh_client_alive_count_max",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 2
    },
    {
      "id": "ssh_breakglass_enabled",
      "label": "ssh_breakglass_enabled",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "ssh_breakglass_user",
      "label": "ssh_breakglass_user",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "ansible-rescue"
    },
    {
      "id": "ssh_breakglass_uid",
      "label": "ssh_breakglass_uid",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 3030
    },
    {
      "id": "ssh_breakglass_home",
      "label": "ssh_breakglass_home",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/home/ansible-rescue"
    },
    {
      "id": "ssh_breakglass_excluded_hosts",
      "label": "ssh_breakglass_excluded_hosts",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "ssh_tcp_forwarding_hosts",
      "label": "ssh_tcp_forwarding_hosts",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "hardening_pass_max_days",
      "label": "hardening_pass_max_days",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 9999
    },
    {
      "id": "hardening_pass_min_days",
      "label": "hardening_pass_min_days",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 0
    },
    {
      "id": "hardening_pass_warn_age",
      "label": "hardening_pass_warn_age",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 7
    },
    {
      "id": "hardening_umask",
      "label": "hardening_umask",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "027"
    },
    {
      "id": "hardening_autoremove",
      "label": "hardening_autoremove",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "rsyslog_target_host",
      "label": "rsyslog_target_host",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "rsyslog_target_port",
      "label": "rsyslog_target_port",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 514
    },
    {
      "id": "postfix_relay_host",
      "label": "postfix_relay_host",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "postfix_relay_port",
      "label": "postfix_relay_port",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 587
    },
    {
      "id": "postfix_mail_domain",
      "label": "postfix_mail_domain",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "example.invalid"
    },
    {
      "id": "postfix_sender_aliases",
      "label": "postfix_sender_aliases",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "victoriametrics_url",
      "label": "victoriametrics_url",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "victoriametrics_database",
      "label": "victoriametrics_database",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "victoriametrics_insecure_skip_verify",
      "label": "victoriametrics_insecure_skip_verify",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "influx_repository_url",
      "label": "influx_repository_url",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "https://repos.influxdata.com/debian"
    },
    {
      "id": "influx_repository_suite",
      "label": "influx_repository_suite",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "stable"
    },
    {
      "id": "influx_repository_component",
      "label": "influx_repository_component",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "main"
    },
    {
      "id": "influx_key_url",
      "label": "influx_key_url",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "https://repos.influxdata.com/influxdata-archive.key"
    },
    {
      "id": "influx_key_fpr",
      "label": "influx_key_fpr",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "24C975CBA61A024EE1B631787C3D57159FC2F927"
    },
    {
      "id": "docker_local_base_dir",
      "label": "docker_local_base_dir",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/root/docker-configs"
    },
    {
      "id": "docker_remote_base_dir",
      "label": "docker_remote_base_dir",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/srv/docker-configs"
    },
    {
      "id": "docker_compose_file_patterns",
      "label": "docker_compose_file_patterns",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "docker_compose_timeout",
      "label": "docker_compose_timeout",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 120
    },
    {
      "id": "docker_wait_retry_delay",
      "label": "docker_wait_retry_delay",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 10
    },
    {
      "id": "docker_wait_retries",
      "label": "docker_wait_retries",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 6
    },
    {
      "id": "docker_critical_stacks",
      "label": "docker_critical_stacks",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "docker_macvlan_config_networks",
      "label": "docker_macvlan_config_networks",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "local_base_dir",
      "label": "local_base_dir",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "remote_base_dir",
      "label": "remote_base_dir",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "compose_file_patterns",
      "label": "compose_file_patterns",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "compose_timeout",
      "label": "compose_timeout",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "wait_retry_delay",
      "label": "wait_retry_delay",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "wait_retries",
      "label": "wait_retries",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "checkmk_server",
      "label": "checkmk_server",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "checkmk.example.invalid:8000"
    },
    {
      "id": "checkmk_server_url",
      "label": "checkmk_server_url",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "https://checkmk.example.invalid"
    },
    {
      "id": "checkmk_site",
      "label": "checkmk_site",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "example"
    },
    {
      "id": "checkmk_registration_user",
      "label": "checkmk_registration_user",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "automation"
    },
    {
      "id": "checkmk_api_user",
      "label": "checkmk_api_user",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "automation"
    },
    {
      "id": "checkmk_agent_download_url",
      "label": "checkmk_agent_download_url",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "checkmk_agent_package_src",
      "label": "checkmk_agent_package_src",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "checkmk_plugins_src_dir",
      "label": "checkmk_plugins_src_dir",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "checkmk_default_folder",
      "label": "checkmk_default_folder",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/managed/unassigned"
    },
    {
      "id": "checkmk_enable_base_plugins",
      "label": "checkmk_enable_base_plugins",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "checkmk_migration_plan",
      "label": "checkmk_migration_plan",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "checkmk_backup_target_host",
      "label": "checkmk_backup_target_host",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "checkmk_container_name",
      "label": "checkmk_container_name",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "checkmk"
    },
    {
      "id": "checkmk_backup_dir",
      "label": "checkmk_backup_dir",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/backup"
    },
    {
      "id": "checkmk_folders",
      "label": "checkmk_folders",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "kerberos_realm",
      "label": "kerberos_realm",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "kerberos_kdcs",
      "label": "kerberos_kdcs",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "kerberos_admin_server",
      "label": "kerberos_admin_server",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "kerberos_dns_lookup_realm",
      "label": "kerberos_dns_lookup_realm",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "kerberos_dns_lookup_kdc",
      "label": "kerberos_dns_lookup_kdc",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "kerberos_force_tcp",
      "label": "kerberos_force_tcp",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "kerberos_fix_cifs_upcall",
      "label": "kerberos_fix_cifs_upcall",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "controller_report_dir",
      "label": "controller_report_dir",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "strukturierter oder dynamischer Wert; keine Kopie von Standortdaten"
    },
    {
      "id": "ca_dir",
      "label": "ca_dir",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/root/ca"
    },
    {
      "id": "crl_docker_target_dir",
      "label": "crl_docker_target_dir",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/srv/crl/"
    },
    {
      "id": "crl_container_name",
      "label": "crl_container_name",
      "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "crl-web"
    },
    {
      "id": "tls_validate_certs_default",
      "label": "TLS-Standortstandard",
      "description": "Standard fuer die einzeln beschriebenen HTTPS-Aufgaben. Ohne Eintrag true. Telegram hat einen eigenen Default true. Ein Task-Override unter tls_validate_certs hat Vorrang.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "portainer_check_enabled",
      "label": "portainer_check_enabled",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "description": "Zusätzlichen TCP-Test für Portainer nach dem Pflichtcheck aktivieren."
    },
    {
      "id": "portainer_check_host",
      "label": "portainer_check_host",
      "type": "string",
      "required": false,
      "sensitive": false,
      "description": "Optionales TCP-Ziel. Ohne Eintrag gilt die Ansible-Adresse des Docker-Hosts."
    },
    {
      "id": "portainer_check_port",
      "label": "portainer_check_port",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "description": "TCP-Port für den optionalen Portainer-Test."
    },
    {
      "id": "portainer_check_timeout",
      "label": "portainer_check_timeout",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "description": "Wartezeit für den Portainer-TCP-Test in Sekunden."
    },
    {
      "id": "controller_reports_dir",
      "label": "Berichtsverzeichnis",
      "description": "Ziel für Docker-, Checkmk- und fstab-Berichte. Relative Pfade beginnen im Controllerprojekt.",
      "type": "string",
      "required": false,
      "sensitive": false
    },
    {
      "id": "docker_deploy_pause_summary",
      "label": "Docker-Abschlusspause",
      "description": "Nach der Zusammenfassung auf eine Taste warten. Eine Löschung verwaister Stacks erfordert weiterhin eine Bestätigung.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "checkmk_backup_mode",
      "label": "Checkmk-Sicherungsmodus",
      "description": "docker führt OMD im Container aus, native direkt auf dem Sicherungshost.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "docker"
    },
    {
      "id": "apache_certificate_filename",
      "label": "Zertifikatsdateiname",
      "description": "Name des Zertifikats im Quellverzeichnis.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "certificate.crt"
    },
    {
      "id": "apache_intermediate_filename",
      "label": "Dateiname der Zwischenzertifikate",
      "description": "Name der Zertifikatskette im Quellverzeichnis.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "intermediate1.crt"
    },
    {
      "id": "apache_encrypted_key_filename",
      "label": "Verschlüsselter Schlüssel",
      "description": "Name der verschlüsselten Eingabedatei für das Vorbereitungsskript.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "wildcard_example_org.key"
    },
    {
      "id": "apache_private_key_filename",
      "label": "Vorbereiteter Schlüssel",
      "description": "Name der vom Playbook verteilten Schlüsseldatei.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "wildcard_example_org_unencrypted.key"
    },
    {
      "id": "apache_certificate_target_filename",
      "label": "Zertifikatsname am Ziel",
      "description": "Dateiname des Zertifikats im Zielverzeichnis.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "cert.cert"
    },
    {
      "id": "apache_private_key_target_filename",
      "label": "Schlüsselname am Ziel",
      "description": "Dateiname des Schlüssels im Zielverzeichnis.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "key.key"
    },
    {
      "id": "apache_certificate_directory",
      "label": "Apache-Zielverzeichnis",
      "description": "Verzeichnis auf dem Webserver für Zertifikat und Schlüssel.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/cert"
    },
    {
      "id": "apache_certificate_source_directory",
      "label": "Apache-Quellverzeichnis",
      "description": "Optionaler absoluter Pfad zum PEM-Verzeichnis auf dem Controller.",
      "type": "string",
      "required": false,
      "sensitive": false
    },
    {
      "id": "apache_certificate_source",
      "label": "Quelldatei Zertifikat",
      "description": "Optionaler absoluter Pfad zur Zertifikatsdatei.",
      "type": "string",
      "required": false,
      "sensitive": false
    },
    {
      "id": "apache_intermediate_source",
      "label": "Quelldatei Zwischenzertifikat",
      "description": "Optionaler absoluter Pfad zur Zwischenzertifikatsdatei.",
      "type": "string",
      "required": false,
      "sensitive": false
    },
    {
      "id": "apache_private_key_source",
      "label": "Quelldatei Schlüssel",
      "description": "Optionaler absoluter Dateipfad des vorbereiteten Schlüssels.",
      "type": "string",
      "required": false,
      "sensitive": false
    },
    {
      "id": "apache_certificate_target",
      "label": "Zielpfad Zertifikat",
      "description": "Optionaler absoluter Dateipfad des Zertifikats auf dem Webserver.",
      "type": "string",
      "required": false,
      "sensitive": false
    },
    {
      "id": "apache_private_key_target",
      "label": "Zielpfad Schlüssel",
      "description": "Optionaler absoluter Dateipfad des Schlüssels auf dem Webserver.",
      "type": "string",
      "required": false,
      "sensitive": false
    }
  ],
  "constraints": [],
  "sources": [
    "examples/settings/all_settings.example.yml",
    "examples/settings/controller_paths.example.yml"
  ],
  "source_hashes": {
    "examples/settings/all_settings.example.yml": "de813875024c9a4a77bbe7cd827533bc7b8d429c9a3ba8747f0b42b49dfcba9d",
    "examples/settings/controller_paths.example.yml": "5221bdc30a837a0ec4af252ba47b37d791605bcac9f4023bb3039b9b1013490f"
  },
  "i18n": {
    "de": {
      "title": "Konfigurationsreferenz group_vars/all/settings.yml",
      "description": "# Konfigurationsreferenz group_vars/all/settings.yml\n\nDiese Angaben beschreiben ausschliesslich die vorliegende Vorlagen-/Beispieldatei, nicht die effektiven Werte eines laufenden Hosts.\n\nDie Datei wird durch diese Dokumentation weder aktiviert noch in bestehende Standortkonfigurationen kopiert.\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `examples/settings/all_settings.example.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n\n## TLS-Schalter pro Aufgabe (1.1.0)\n\n`tls_validate_certs_default` ist der optionale Standortstandard (ohne Eintrag true).\n`tls_validate_certs` ist eine YAML-Zuordnung mit optionalen booleschen Aufgabenschaltern.\nTelegram-Defaults bleiben true. Beispiele und vollstaendige Zuordnung: `examples/tls/settings.example.yml`.\n\nDie optionalen Einstellungen für Berichte, Apache, Docker und Checkmk stehen in `examples/settings/controller_paths.example.yml`.",
      "fields": {
        "controller_lang": {
          "label": "Controller-Sprache",
          "description": "Sprache für Controllerbefehle und Berichte. Erlaubt sind de und en."
        },
        "site_id": {
          "label": "site_id",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "site_name": {
          "label": "site_name",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "site_managed_by": {
          "label": "site_managed_by",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "motd_show_hap": {
          "label": "motd_show_hap",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "motd_hap": {
          "label": "motd_hap",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ansible_auth_mode": {
          "label": "ansible_auth_mode",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "auth_method_description": {
          "label": "auth_method_description",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "managed_access_default_user": {
          "label": "managed_access_default_user",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "managed_access_default_port": {
          "label": "managed_access_default_port",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "managed_access_default_become": {
          "label": "managed_access_default_become",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "managed_access_default_become_method": {
          "label": "managed_access_default_become_method",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "managed_access_default_become_user": {
          "label": "managed_access_default_become_user",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "managed_host_access": {
          "label": "managed_host_access",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "bootstrap_targets": {
          "label": "bootstrap_targets",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "bootstrap_public_key_file": {
          "label": "bootstrap_public_key_file",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "bootstrap_disable_password_auth_after_key": {
          "label": "bootstrap_disable_password_auth_after_key",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.baseline": {
          "label": "features.baseline",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.chrony": {
          "label": "features.chrony",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.fail2ban": {
          "label": "features.fail2ban",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.motd": {
          "label": "features.motd",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.ssh_hardening": {
          "label": "features.ssh_hardening",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.security_base": {
          "label": "features.security_base",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.accounting": {
          "label": "features.accounting",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.security_tools": {
          "label": "features.security_tools",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.lynis": {
          "label": "features.lynis",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.rsyslog": {
          "label": "features.rsyslog",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.postfix": {
          "label": "features.postfix",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.checkmk": {
          "label": "features.checkmk",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.docker": {
          "label": "features.docker",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.proxmox": {
          "label": "features.proxmox",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.hyperv": {
          "label": "features.hyperv",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.kerberos": {
          "label": "features.kerberos",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.kerberos_keytabs": {
          "label": "features.kerberos_keytabs",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "features.telegraf": {
          "label": "features.telegraf",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "system_timezone": {
          "label": "system_timezone",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "chrony_ntp_servers": {
          "label": "chrony_ntp_servers",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "base_packages": {
          "label": "base_packages",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "fail2ban_ignoreip": {
          "label": "fail2ban_ignoreip",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "fail2ban_bantime": {
          "label": "fail2ban_bantime",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "fail2ban_findtime": {
          "label": "fail2ban_findtime",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "fail2ban_maxretry": {
          "label": "fail2ban_maxretry",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "fail2ban_ssh_port": {
          "label": "fail2ban_ssh_port",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "fail2ban_admin_email": {
          "label": "fail2ban_admin_email",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "fail2ban_ticket_email": {
          "label": "fail2ban_ticket_email",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "fail2ban_proxmox_ve_hosts": {
          "label": "fail2ban_proxmox_ve_hosts",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "fail2ban_proxmox_backup_hosts": {
          "label": "fail2ban_proxmox_backup_hosts",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_max_auth_tries": {
          "label": "ssh_max_auth_tries",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_max_sessions": {
          "label": "ssh_max_sessions",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_allow_tcp_forwarding": {
          "label": "ssh_allow_tcp_forwarding",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_permit_root_login": {
          "label": "ssh_permit_root_login",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_client_alive_interval": {
          "label": "ssh_client_alive_interval",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_client_alive_count_max": {
          "label": "ssh_client_alive_count_max",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_breakglass_enabled": {
          "label": "ssh_breakglass_enabled",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_breakglass_user": {
          "label": "ssh_breakglass_user",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_breakglass_uid": {
          "label": "ssh_breakglass_uid",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_breakglass_home": {
          "label": "ssh_breakglass_home",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_breakglass_excluded_hosts": {
          "label": "ssh_breakglass_excluded_hosts",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ssh_tcp_forwarding_hosts": {
          "label": "ssh_tcp_forwarding_hosts",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "hardening_pass_max_days": {
          "label": "hardening_pass_max_days",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "hardening_pass_min_days": {
          "label": "hardening_pass_min_days",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "hardening_pass_warn_age": {
          "label": "hardening_pass_warn_age",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "hardening_umask": {
          "label": "hardening_umask",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "hardening_autoremove": {
          "label": "hardening_autoremove",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "rsyslog_target_host": {
          "label": "rsyslog_target_host",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "rsyslog_target_port": {
          "label": "rsyslog_target_port",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "postfix_relay_host": {
          "label": "postfix_relay_host",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "postfix_relay_port": {
          "label": "postfix_relay_port",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "postfix_mail_domain": {
          "label": "postfix_mail_domain",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "postfix_sender_aliases": {
          "label": "postfix_sender_aliases",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "victoriametrics_url": {
          "label": "victoriametrics_url",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "victoriametrics_database": {
          "label": "victoriametrics_database",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "victoriametrics_insecure_skip_verify": {
          "label": "victoriametrics_insecure_skip_verify",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "influx_repository_url": {
          "label": "influx_repository_url",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "influx_repository_suite": {
          "label": "influx_repository_suite",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "influx_repository_component": {
          "label": "influx_repository_component",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "influx_key_url": {
          "label": "influx_key_url",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "influx_key_fpr": {
          "label": "influx_key_fpr",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "docker_local_base_dir": {
          "label": "docker_local_base_dir",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "docker_remote_base_dir": {
          "label": "docker_remote_base_dir",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "docker_compose_file_patterns": {
          "label": "docker_compose_file_patterns",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "docker_compose_timeout": {
          "label": "docker_compose_timeout",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "docker_wait_retry_delay": {
          "label": "docker_wait_retry_delay",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "docker_wait_retries": {
          "label": "docker_wait_retries",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "docker_critical_stacks": {
          "label": "docker_critical_stacks",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "docker_macvlan_config_networks": {
          "label": "docker_macvlan_config_networks",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "local_base_dir": {
          "label": "local_base_dir",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "remote_base_dir": {
          "label": "remote_base_dir",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "compose_file_patterns": {
          "label": "compose_file_patterns",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "compose_timeout": {
          "label": "compose_timeout",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "wait_retry_delay": {
          "label": "wait_retry_delay",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "wait_retries": {
          "label": "wait_retries",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_server": {
          "label": "checkmk_server",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_server_url": {
          "label": "checkmk_server_url",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_site": {
          "label": "checkmk_site",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_registration_user": {
          "label": "checkmk_registration_user",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_api_user": {
          "label": "checkmk_api_user",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_agent_download_url": {
          "label": "checkmk_agent_download_url",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_agent_package_src": {
          "label": "checkmk_agent_package_src",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_plugins_src_dir": {
          "label": "checkmk_plugins_src_dir",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_default_folder": {
          "label": "checkmk_default_folder",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_enable_base_plugins": {
          "label": "checkmk_enable_base_plugins",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_migration_plan": {
          "label": "checkmk_migration_plan",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_backup_target_host": {
          "label": "checkmk_backup_target_host",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_container_name": {
          "label": "checkmk_container_name",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_backup_dir": {
          "label": "checkmk_backup_dir",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "checkmk_folders": {
          "label": "checkmk_folders",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "kerberos_realm": {
          "label": "kerberos_realm",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "kerberos_kdcs": {
          "label": "kerberos_kdcs",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "kerberos_admin_server": {
          "label": "kerberos_admin_server",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "kerberos_dns_lookup_realm": {
          "label": "kerberos_dns_lookup_realm",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "kerberos_dns_lookup_kdc": {
          "label": "kerberos_dns_lookup_kdc",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "kerberos_force_tcp": {
          "label": "kerberos_force_tcp",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "kerberos_fix_cifs_upcall": {
          "label": "kerberos_fix_cifs_upcall",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "controller_report_dir": {
          "label": "controller_report_dir",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "ca_dir": {
          "label": "ca_dir",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "crl_docker_target_dir": {
          "label": "crl_docker_target_dir",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "crl_container_name": {
          "label": "crl_container_name",
          "description": "Vorhandene Konfigurationsoption aus group_vars/all/settings.yml. Standortwerte bleiben lokal; kein automatisches Setzen."
        },
        "tls_validate_certs_default": {
          "label": "TLS-Standortstandard",
          "description": "Standard fuer die einzeln beschriebenen HTTPS-Aufgaben. Ohne Eintrag true. Telegram hat einen eigenen Default true. Ein Task-Override unter tls_validate_certs hat Vorrang."
        },
        "portainer_check_enabled": {
          "label": "portainer_check_enabled",
          "description": "Zusätzlichen TCP-Test für Portainer nach dem Pflichtcheck aktivieren."
        },
        "portainer_check_host": {
          "label": "portainer_check_host",
          "description": "Optionales TCP-Ziel. Ohne Eintrag gilt die Ansible-Adresse des Docker-Hosts."
        },
        "portainer_check_port": {
          "label": "portainer_check_port",
          "description": "TCP-Port für den optionalen Portainer-Test."
        },
        "portainer_check_timeout": {
          "label": "portainer_check_timeout",
          "description": "Wartezeit für den Portainer-TCP-Test in Sekunden."
        },
        "controller_reports_dir": {
          "label": "Berichtsverzeichnis",
          "description": "Ziel für Docker-, Checkmk- und fstab-Berichte. Relative Pfade beginnen im Controllerprojekt."
        },
        "docker_deploy_pause_summary": {
          "label": "Docker-Abschlusspause",
          "description": "Nach der Zusammenfassung auf eine Taste warten. Eine Löschung verwaister Stacks erfordert weiterhin eine Bestätigung."
        },
        "checkmk_backup_mode": {
          "label": "Checkmk-Sicherungsmodus",
          "description": "docker führt OMD im Container aus, native direkt auf dem Sicherungshost."
        },
        "apache_certificate_filename": {
          "label": "Zertifikatsdateiname",
          "description": "Name des Zertifikats im Quellverzeichnis."
        },
        "apache_intermediate_filename": {
          "label": "Dateiname der Zwischenzertifikate",
          "description": "Name der Zertifikatskette im Quellverzeichnis."
        },
        "apache_encrypted_key_filename": {
          "label": "Verschlüsselter Schlüssel",
          "description": "Name der verschlüsselten Eingabedatei für das Vorbereitungsskript."
        },
        "apache_private_key_filename": {
          "label": "Vorbereiteter Schlüssel",
          "description": "Name der vom Playbook verteilten Schlüsseldatei."
        },
        "apache_certificate_target_filename": {
          "label": "Zertifikatsname am Ziel",
          "description": "Dateiname des Zertifikats im Zielverzeichnis."
        },
        "apache_private_key_target_filename": {
          "label": "Schlüsselname am Ziel",
          "description": "Dateiname des Schlüssels im Zielverzeichnis."
        },
        "apache_certificate_directory": {
          "label": "Apache-Zielverzeichnis",
          "description": "Verzeichnis auf dem Webserver für Zertifikat und Schlüssel."
        },
        "apache_certificate_source_directory": {
          "label": "Apache-Quellverzeichnis",
          "description": "Optionaler absoluter Pfad zum PEM-Verzeichnis auf dem Controller."
        },
        "apache_certificate_source": {
          "label": "Quelldatei Zertifikat",
          "description": "Optionaler absoluter Pfad zur Zertifikatsdatei."
        },
        "apache_intermediate_source": {
          "label": "Quelldatei Zwischenzertifikat",
          "description": "Optionaler absoluter Pfad zur Zwischenzertifikatsdatei."
        },
        "apache_private_key_source": {
          "label": "Quelldatei Schlüssel",
          "description": "Optionaler absoluter Dateipfad des vorbereiteten Schlüssels."
        },
        "apache_certificate_target": {
          "label": "Zielpfad Zertifikat",
          "description": "Optionaler absoluter Dateipfad des Zertifikats auf dem Webserver."
        },
        "apache_private_key_target": {
          "label": "Zielpfad Schlüssel",
          "description": "Optionaler absoluter Dateipfad des Schlüssels auf dem Webserver."
        }
      }
    },
    "en": {
      "title": "Configuration reference for group_vars/all/settings.yml",
      "description": "# Configuration reference for group_vars/all/settings.yml\n\nThis reference describes the example file. Effective host values depend on local settings.\n\nThis reference does not activate the example or copy it into an existing site configuration.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `examples/settings/all_settings.example.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## TLS settings per task (1.1.0)\n\n`tls_validate_certs_default` sets the optional site default, normally true. `tls_validate_certs` maps individual tasks to optional Boolean overrides. Telegram tasks independently default to true. See `examples/tls/settings.example.yml` for examples and the complete mapping.\n\nOptional report, Apache, Docker and Checkmk settings are listed in `examples/settings/controller_paths.example.yml`.",
      "fields": {
        "controller_lang": {
          "label": "Controller language",
          "description": "Language for controller commands and reports. Choose de or en."
        },
        "site_id": {
          "label": "site_id",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "site_name": {
          "label": "site_name",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "site_managed_by": {
          "label": "site_managed_by",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "motd_show_hap": {
          "label": "motd_show_hap",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "motd_hap": {
          "label": "motd_hap",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ansible_auth_mode": {
          "label": "ansible_auth_mode",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "auth_method_description": {
          "label": "auth_method_description",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "managed_access_default_user": {
          "label": "managed_access_default_user",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "managed_access_default_port": {
          "label": "managed_access_default_port",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "managed_access_default_become": {
          "label": "managed_access_default_become",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "managed_access_default_become_method": {
          "label": "managed_access_default_become_method",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "managed_access_default_become_user": {
          "label": "managed_access_default_become_user",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "managed_host_access": {
          "label": "managed_host_access",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "bootstrap_targets": {
          "label": "bootstrap_targets",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "bootstrap_public_key_file": {
          "label": "bootstrap_public_key_file",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "bootstrap_disable_password_auth_after_key": {
          "label": "bootstrap_disable_password_auth_after_key",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.baseline": {
          "label": "features.baseline",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.chrony": {
          "label": "features.chrony",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.fail2ban": {
          "label": "features.fail2ban",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.motd": {
          "label": "features.motd",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.ssh_hardening": {
          "label": "features.ssh_hardening",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.security_base": {
          "label": "features.security_base",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.accounting": {
          "label": "features.accounting",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.security_tools": {
          "label": "features.security_tools",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.lynis": {
          "label": "features.lynis",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.rsyslog": {
          "label": "features.rsyslog",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.postfix": {
          "label": "features.postfix",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.checkmk": {
          "label": "features.checkmk",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.docker": {
          "label": "features.docker",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.proxmox": {
          "label": "features.proxmox",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.hyperv": {
          "label": "features.hyperv",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.kerberos": {
          "label": "features.kerberos",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.kerberos_keytabs": {
          "label": "features.kerberos_keytabs",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "features.telegraf": {
          "label": "features.telegraf",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "system_timezone": {
          "label": "system_timezone",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "chrony_ntp_servers": {
          "label": "chrony_ntp_servers",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "base_packages": {
          "label": "base_packages",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "fail2ban_ignoreip": {
          "label": "fail2ban_ignoreip",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "fail2ban_bantime": {
          "label": "fail2ban_bantime",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "fail2ban_findtime": {
          "label": "fail2ban_findtime",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "fail2ban_maxretry": {
          "label": "fail2ban_maxretry",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "fail2ban_ssh_port": {
          "label": "fail2ban_ssh_port",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "fail2ban_admin_email": {
          "label": "fail2ban_admin_email",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "fail2ban_ticket_email": {
          "label": "fail2ban_ticket_email",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "fail2ban_proxmox_ve_hosts": {
          "label": "fail2ban_proxmox_ve_hosts",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "fail2ban_proxmox_backup_hosts": {
          "label": "fail2ban_proxmox_backup_hosts",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_max_auth_tries": {
          "label": "ssh_max_auth_tries",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_max_sessions": {
          "label": "ssh_max_sessions",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_allow_tcp_forwarding": {
          "label": "ssh_allow_tcp_forwarding",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_permit_root_login": {
          "label": "ssh_permit_root_login",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_client_alive_interval": {
          "label": "ssh_client_alive_interval",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_client_alive_count_max": {
          "label": "ssh_client_alive_count_max",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_breakglass_enabled": {
          "label": "ssh_breakglass_enabled",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_breakglass_user": {
          "label": "ssh_breakglass_user",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_breakglass_uid": {
          "label": "ssh_breakglass_uid",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_breakglass_home": {
          "label": "ssh_breakglass_home",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_breakglass_excluded_hosts": {
          "label": "ssh_breakglass_excluded_hosts",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ssh_tcp_forwarding_hosts": {
          "label": "ssh_tcp_forwarding_hosts",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "hardening_pass_max_days": {
          "label": "hardening_pass_max_days",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "hardening_pass_min_days": {
          "label": "hardening_pass_min_days",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "hardening_pass_warn_age": {
          "label": "hardening_pass_warn_age",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "hardening_umask": {
          "label": "hardening_umask",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "hardening_autoremove": {
          "label": "hardening_autoremove",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "rsyslog_target_host": {
          "label": "rsyslog_target_host",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "rsyslog_target_port": {
          "label": "rsyslog_target_port",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "postfix_relay_host": {
          "label": "postfix_relay_host",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "postfix_relay_port": {
          "label": "postfix_relay_port",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "postfix_mail_domain": {
          "label": "postfix_mail_domain",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "postfix_sender_aliases": {
          "label": "postfix_sender_aliases",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "victoriametrics_url": {
          "label": "victoriametrics_url",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "victoriametrics_database": {
          "label": "victoriametrics_database",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "victoriametrics_insecure_skip_verify": {
          "label": "victoriametrics_insecure_skip_verify",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "influx_repository_url": {
          "label": "influx_repository_url",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "influx_repository_suite": {
          "label": "influx_repository_suite",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "influx_repository_component": {
          "label": "influx_repository_component",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "influx_key_url": {
          "label": "influx_key_url",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "influx_key_fpr": {
          "label": "influx_key_fpr",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "docker_local_base_dir": {
          "label": "docker_local_base_dir",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "docker_remote_base_dir": {
          "label": "docker_remote_base_dir",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "docker_compose_file_patterns": {
          "label": "docker_compose_file_patterns",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "docker_compose_timeout": {
          "label": "docker_compose_timeout",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "docker_wait_retry_delay": {
          "label": "docker_wait_retry_delay",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "docker_wait_retries": {
          "label": "docker_wait_retries",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "docker_critical_stacks": {
          "label": "docker_critical_stacks",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "docker_macvlan_config_networks": {
          "label": "docker_macvlan_config_networks",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "local_base_dir": {
          "label": "local_base_dir",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "remote_base_dir": {
          "label": "remote_base_dir",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "compose_file_patterns": {
          "label": "compose_file_patterns",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "compose_timeout": {
          "label": "compose_timeout",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "wait_retry_delay": {
          "label": "wait_retry_delay",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "wait_retries": {
          "label": "wait_retries",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_server": {
          "label": "checkmk_server",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_server_url": {
          "label": "checkmk_server_url",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_site": {
          "label": "checkmk_site",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_registration_user": {
          "label": "checkmk_registration_user",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_api_user": {
          "label": "checkmk_api_user",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_agent_download_url": {
          "label": "checkmk_agent_download_url",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_agent_package_src": {
          "label": "checkmk_agent_package_src",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_plugins_src_dir": {
          "label": "checkmk_plugins_src_dir",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_default_folder": {
          "label": "checkmk_default_folder",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_enable_base_plugins": {
          "label": "checkmk_enable_base_plugins",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_migration_plan": {
          "label": "checkmk_migration_plan",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_backup_target_host": {
          "label": "checkmk_backup_target_host",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_container_name": {
          "label": "checkmk_container_name",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_backup_dir": {
          "label": "checkmk_backup_dir",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "checkmk_folders": {
          "label": "checkmk_folders",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "kerberos_realm": {
          "label": "kerberos_realm",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "kerberos_kdcs": {
          "label": "kerberos_kdcs",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "kerberos_admin_server": {
          "label": "kerberos_admin_server",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "kerberos_dns_lookup_realm": {
          "label": "kerberos_dns_lookup_realm",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "kerberos_dns_lookup_kdc": {
          "label": "kerberos_dns_lookup_kdc",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "kerberos_force_tcp": {
          "label": "kerberos_force_tcp",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "kerberos_fix_cifs_upcall": {
          "label": "kerberos_fix_cifs_upcall",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "controller_report_dir": {
          "label": "controller_report_dir",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "ca_dir": {
          "label": "ca_dir",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "crl_docker_target_dir": {
          "label": "crl_docker_target_dir",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "crl_container_name": {
          "label": "crl_container_name",
          "description": "Configuration option from group_vars/all/settings.yml. The site sets the actual value locally."
        },
        "tls_validate_certs_default": {
          "label": "Site TLS default",
          "description": "Default for the documented HTTPS tasks. Defaults to true. Telegram has its own true default. The individual task’s tls_validate_certs takes precedence."
        },
        "portainer_check_enabled": {
          "label": "portainer_check_enabled",
          "description": "Enable an additional TCP check for Portainer after the mandatory container checks."
        },
        "portainer_check_host": {
          "label": "portainer_check_host",
          "description": "Optional TCP target. Defaults to the Docker host’s Ansible address."
        },
        "portainer_check_port": {
          "label": "portainer_check_port",
          "description": "TCP port for the optional Portainer check."
        },
        "portainer_check_timeout": {
          "label": "portainer_check_timeout",
          "description": "Timeout for the Portainer TCP check, in seconds."
        },
        "controller_reports_dir": {
          "label": "Report directory",
          "description": "Report directory for Checkmk, Docker and fstab audits. Relative paths start at the controller project."
        },
        "docker_deploy_pause_summary": {
          "label": "Docker summary pause",
          "description": "Pause after the deployment summary. The orphan-stack confirmation is independent."
        },
        "checkmk_backup_mode": {
          "label": "Checkmk backup mode",
          "description": "Run the pre-migration OMD backup in Docker or directly on the backup host with native."
        },
        "apache_certificate_filename": {
          "label": "Certificate file name",
          "description": "Certificate file name inside the certificate source directory."
        },
        "apache_intermediate_filename": {
          "label": "Intermediate certificate file name",
          "description": "Intermediate certificate file name inside the source directory."
        },
        "apache_encrypted_key_filename": {
          "label": "Encrypted key file name",
          "description": "Encrypted input key file name used by the preparation script."
        },
        "apache_private_key_filename": {
          "label": "Prepared key file name",
          "description": "Prepared key file name in the source directory."
        },
        "apache_certificate_target_filename": {
          "label": "Target certificate file name",
          "description": "Certificate file name in the destination directory."
        },
        "apache_private_key_target_filename": {
          "label": "Target key file name",
          "description": "Private key file name in the destination directory."
        },
        "apache_certificate_directory": {
          "label": "Apache target directory",
          "description": "Remote Apache certificate directory."
        },
        "apache_certificate_source_directory": {
          "label": "Apache source directory",
          "description": "Optional absolute certificate source directory."
        },
        "apache_certificate_source": {
          "label": "Source certificate path",
          "description": "Optional absolute certificate source file."
        },
        "apache_intermediate_source": {
          "label": "Intermediate certificate path",
          "description": "Optional absolute intermediate source file."
        },
        "apache_private_key_source": {
          "label": "Prepared key path",
          "description": "Optional absolute prepared key source file."
        },
        "apache_certificate_target": {
          "label": "Target certificate path",
          "description": "Optional absolute certificate destination file."
        },
        "apache_private_key_target": {
          "label": "Target key path",
          "description": "Optional absolute key destination file."
        }
      }
    }
  }
}
```
