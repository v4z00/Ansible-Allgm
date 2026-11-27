# Optional credentials

Examples are under `examples/access`. No example is loaded automatically in `group_vars/all`. Keep existing settings and secrets when reviewing examples.

<details>
<summary>Deutsch</summary>

# Optionale Zugaenge

Beispiele unter examples/access; keine automatisch geladene Beispieldatei in group_vars/all.
Bestehende Settings/Secrets niemals mit Beispielwerten ersetzen.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
  },
  "i18n": {
    "de": {
      "title": "Optionale lokale Zugaenge – Nachschlagebeispiel",
      "description": "# Optionale Zugaenge\n\nBeispiele unter examples/access; keine automatisch geladene Beispieldatei in group_vars/all.\nBestehende Settings/Secrets niemals mit Beispielwerten ersetzen.",
      "fields": {
        "checkmk_api_password": {
          "label": "Checkmk API-Secret",
          "description": "Nur lokal in Secrets pflegen, Beispiel leer lassen."
        },
        "checkmk_registration_password": {
          "label": "Agentregistrierungs-Secret",
          "description": "Nur lokal in Secrets pflegen, Beispiel leer lassen."
        }
      }
    },
    "en": {
      "title": "Optional local credentials reference",
      "description": "# Optional credentials\n\nExamples are under `examples/access`. No example is loaded automatically in `group_vars/all`. Keep existing settings and secrets when reviewing examples.",
      "fields": {
        "checkmk_api_password": {
          "label": "Checkmk API secret",
          "description": "Maintain this value in local secrets. Leave the example empty."
        },
        "checkmk_registration_password": {
          "label": "Agent registration secret",
          "description": "Maintain this value in local secrets. Leave the example empty."
        }
      }
    }
  }
}
```

</details>
