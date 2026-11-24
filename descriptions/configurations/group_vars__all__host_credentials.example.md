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
    "examples/first_run/access.yml.example"
  ],
  "source_hashes": {
    "examples/access/credentials.example.yml": "8d8306f1b8aaad5f1805478edd993ffd18bd7f8ff6d294bbe6b9c00ad1889ad6",
    "examples/first_run/access.yml.example": "40a524f20980bb08fde157744cffc62b7533b5c8c5952aafc2dabbc9a9b2447a"
  }
}
```
