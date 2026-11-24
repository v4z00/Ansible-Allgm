# Rolle fail2ban

Rolle: `roles/fail2ban`.

Im Bestand definierte Aufgaben:

- Fail2ban installieren
- fail2ban
- Mailziele fuer aktivierte Benachrichtigungen validieren
- Stille Mailaction fuer Ticketsysteme installieren
- Stille Mailaction bei deaktivierten Ticketbenachrichtigungen entfernen
- Proxmox-VE-Filter installieren
- Proxmox-Backup-Filter installieren
- Fail2ban-Konfiguration verteilen
- Fail2ban aktivieren

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/fail2ban",
  "title": "Rolle fail2ban",
  "documented": false,
  "fields": [
    {
      "id": "fail2ban_enable_notifications",
      "label": "fail2ban_enable_notifications",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "fail2ban_enable_ticket_notifications",
      "label": "fail2ban_enable_ticket_notifications",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "fail2ban_enable_postfix_jail",
      "label": "fail2ban_enable_postfix_jail",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    }
  ],
  "constraints": [],
  "sources": [
    "roles/fail2ban/tasks/main.yml",
    "roles/fail2ban/defaults/main.yml"
  ],
  "source_hashes": {
    "roles/fail2ban/defaults/main.yml": "5bb52f807b33493ab59615b1f8dbae46f3b7c3dce54c959e213a5fc58c098f86",
    "roles/fail2ban/tasks/main.yml": "6e0fe6271ca3ee60fefe88b201facbab079ef460193497baaa9f943ba98491e0"
  }
}
```

## Quellen und Pflege

- `roles/fail2ban/tasks/main.yml`
- `roles/fail2ban/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
