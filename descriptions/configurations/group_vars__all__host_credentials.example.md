# Optionale Zugaenge

Beispiele unter examples/access; keine automatisch geladene Beispieldatei in group_vars/all.
Bestehende Settings/Secrets niemals mit Beispielwerten ersetzen.

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "examples/access/credentials.example.yml",
  "title": "Optionale lokale Zugaenge – Nachschlagebeispiel",
  "documented": true,
  "fields": [
    {
      "id": "checkmk_api_password",
      "label": "Checkmk API-Secret",
      "description": "Nur lokal in Secrets pflegen, Beispiel leer lassen.",
      "type": "string",
      "required": false,
      "sensitive": true
    },
    {
      "id": "checkmk_registration_password",
      "label": "Agentregistrierungs-Secret",
      "description": "Nur lokal in Secrets pflegen, Beispiel leer lassen.",
      "type": "string",
      "required": false,
      "sensitive": true
    }
  ],
  "constraints": [],
  "sources": [
    "examples/access/credentials.example.yml",
    "group_vars/all/access.yml"
  ],
  "source_hashes": {
    "examples/access/credentials.example.yml": "8d8306f1b8aaad5f1805478edd993ffd18bd7f8ff6d294bbe6b9c00ad1889ad6"
  }
}
```
