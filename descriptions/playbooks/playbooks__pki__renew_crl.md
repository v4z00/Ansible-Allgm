# Playbook playbooks/pki/renew_crl.yml

Vorhandener Einstieg: `playbooks/pki/renew_crl.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Step 1: Renew and Convert Root CRL (on the controller)
- CA-Kennwort muss lokal hinterlegt sein
- Generate new CRL (PEM format)
- Convert CRL to DER format (Required for Windows!)
- Display generation status
- Step 2: Deploy CRL to Docker Server
- Ensure destination directory exists
- Copy new Root CRL (DER) with permissions 0774
- Restart Webserver Container
- {{ container_name }}

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/pki/renew_crl.yml",
  "title": "Playbook playbooks/pki/renew_crl.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/pki/renew_crl.yml"
  ],
  "source_hashes": {
    "playbooks/pki/renew_crl.yml": "c95c2b9349f67c35b9e89224ed9054f304b325e5d6d75e0256ae06ba25e5461b"
  }
}
```

## Quellen und Pflege

- `playbooks/pki/renew_crl.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
