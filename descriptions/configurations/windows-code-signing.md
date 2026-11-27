# Sign Windows code on a configured central host

Set `windows_script_signing.enabled: true` in private environment settings. Configure
host, public_certificate_src, store_location, work_root and optional timestamp_server.
No environment host, domain, subject or private key is embedded in the shared code.
Other environments can disable the signing integration. An existing AllSigned policy
still blocks unsigned deployment; the switch does not weaken Windows policy.

Provision the selected signer first with `ansible-playbook playbooks/windows/setup_signing.yml
--limit signer-example`. An optional pfx_src/pfx_password imports the existing key only
on that host, under SYSTEM/runas, with key_exportable false. An existing key can be used
without a PFX source. The one-use PFX transport is removed even on failure. No key or
password is exported to execution hosts, SYSVOL, drop-ins, Git or SQLite.

The public certificate selects the exact thumbprint. Setup checks code-signing EKU,
validity/private-key availability and signs a temporary probe. The configured store is
LocalMachine by default; CurrentUser under SYSTEM means SYSTEM's user store. Prepare
that context deliberately. Existing keys are not silently migrated between stores.

Execution hosts receive the public publisher certificate. Root trust is separate:
trust_self_signed_certificate is an explicit self-issued leaf exception; otherwise
trusted_root_certificates contains explicitly supplied CA roots. Certificate files are
validated as public X.509 before transport. No PFX is accepted by the artifact builder.

Library rollout prepares an explicit code manifest, signs on the chosen host under a
per-batch mutex, fetches the signed bytes, and checks source-to-signed SHA mappings.
Authenticode is checked on the signer and again on the execution host before import.
PS1, PSM1, PSD1 and PS1XML are covered. Unchanged valid batches are reused; source changes,
certificate rotation or timestamp-service changes produce a different batch identity.
No recursive signing of unknown host files occurs. All environment values remain variables.

The central task calls the same Set-AuthenticodeSignature mechanism as a local signer.
Timestamping is optional and explicit. Signatures without a timestamp need certificate
lifetime/rotation planning. A check-mode run performs no key import or signing. Portable
tests mock Authenticode; the native Windows test script uses only a synthetic certificate. Automated
CI publication is not configured with the current GitHub access. Real WinRM/runas/PFX and the environment trust chain still need a pilot.

<details>
<summary>Deutsch</summary>

# Windows-Code auf einem konfigurierten zentralen Host signieren

`windows_script_signing.enabled: true` schaltet die verpflichtende Signierstrecke für
das Deployment ein. Signierhost, öffentlicher CER, Store, Arbeits-/Cachepfade und
Zeitstempelserver stehen in privaten Variablen. Andere Umgebungen können abschalten;
eine bestehende AllSigned-Richtlinie wird dadurch nicht umgangen oder verändert.

Zuerst `playbooks/windows/setup_signing.yml --limit signer-example` ausführen. Optional
werden vorhandener PFX und Passwort lokal in den Settings angegeben. Import nur auf
dem ausgewählten Host unter SYSTEM/runas, ohne Exportierbarkeit anzufordern. Die PFX-
Transportdatei wird auch bei Fehlern entfernt. Bestehende Schlüssel können ohne erneuten
PFX-Import verwendet werden. Private Schlüssel/Passwörter kommen nicht auf andere Hosts,
nicht in SYSVOL, Drop-ins, Git oder SQLite.

Der öffentliche CER bestimmt den exakten Thumbprint statt eines festen Subject-Namens.
Setup prüft EKU, Gültigkeit und Schlüsselzugriff und signiert eine temporäre Probe.
Standard ist LocalMachine. CurrentUser unter SYSTEM ist dessen Benutzerstore, nicht
unbemerkt der Store eines interaktiv angemeldeten Administrators. Vorhandene Schlüssel
werden nicht still zwischen Stores verschoben.

Ausführungsziele erhalten nur den öffentlichen Publisher. Root-Vertrauen ist getrennt:
Die selbst-ausgestellte Zertifikatsausnahme ist ausdrücklich schaltbar; andere CA-Roots
werden einzeln angegeben. Vor Transport wird öffentliches X.509 geprüft. Der Artefakt-
bauer akzeptiert keinen PFX. Die Library wird anhand eines festen Manifests auf dem
konfigurierten Host signiert, per Mutex gegen parallele Änderungen geschützt und mit
getrennten Quell-/Signatur-SHA zurückgeholt. Native Signaturprüfung vor Import auch auf
dem Ausführungsziel. PS1, PSM1, PSD1 und PS1XML werden signiert, unbekannte Hostdateien
nicht rekursiv übernommen. Unveränderte gültige Batches werden wiederverwendet.

Verwendet wird Set-AuthenticodeSignature wie im bisherigen Signer. Zeitstempelserver
sind optional; ohne Zeitstempel die Zertifikatslaufzeit/Rotation beachten. Checkmode
importiert keinen Schlüssel und signiert nicht. Portable Tests verwenden Cmdlet-Doubles;
das native Windows-Testskript nutzt nur ein synthetisches Zertifikat. Ein automatischer
CI-Workflow ist mit dem derzeitigen GitHub-Zugang nicht veröffentlicht. WinRM/runas/PFX
und die echte Vertrauenskette dieser Umgebung müssen noch im Pilot bestätigt werden.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "playbooks/windows/setup_signing.yml",
  "title": "Windows-Code auf einem konfigurierten zentralen Host signieren",
  "documented": true,
  "fields": [],
  "constraints": [],
  "sources": [
    "scripts/windows_signing_bundle.py",
    "playbooks/windows/setup_signing.yml",
    "roles/windows_code_signing/tasks/import_key.yml",
    "roles/windows_code_signing/tasks/trust.yml",
    "roles/windows_code_signing/tasks/validate.yml",
    "roles/windows_code_signing/tasks/library.yml",
    "roles/windows_code_signing/tasks/main.yml",
    "roles/windows_code_signing/defaults/main.yml",
    "roles/windows_code_signing/templates/setup-probe.ps1.j2",
    "roles/windows_code_signing/templates/sign-bundle.ps1.j2"
  ],
  "source_hashes": {
    "scripts/windows_signing_bundle.py": "3b19e106845668b800c40349ba449430cf2023bc351e4b61ca0b46b539564d8e",
    "playbooks/windows/setup_signing.yml": "0a93ad178f50e1b83c7517cb288792d8bb3ec78940611f785e19a5d213c84152",
    "roles/windows_code_signing/tasks/import_key.yml": "56d61a10e6cd9460d903cd87266c9daad3ee319bfef847ed287cd605227ff527",
    "roles/windows_code_signing/tasks/trust.yml": "ccc08ce7cca2d4d7d9a95b8506d56fcb10589ec268cd97ff56b939cbd9255ef5",
    "roles/windows_code_signing/tasks/validate.yml": "5be4f9f3e025759c01bdbafeb2f5615a961e40e911e7fcd597850660cfa268f8",
    "roles/windows_code_signing/tasks/library.yml": "51d3c2d29eac9238cc4dcec0d9250663eefd6dadf01fca79091c07efbd554c77",
    "roles/windows_code_signing/tasks/main.yml": "c915df95c8ae0caef55b6d4761636b3d278d8709a3f69b3934d4c631f41e9400",
    "roles/windows_code_signing/defaults/main.yml": "92d0cdbf367bd8cb656fae8c1fa1290feda6f6839b507e37ea700b3a53b2b5d3",
    "roles/windows_code_signing/templates/setup-probe.ps1.j2": "f91f0e18a978f0aa02b8ae5c5470ed702c74d8013597a4e128350957b6743a25",
    "roles/windows_code_signing/templates/sign-bundle.ps1.j2": "1e877235ae59edbeb06b3d198d97b3afa6e9106f8656252b42dfec9e45b574e3"
  },
  "i18n": {
    "en": {
      "title": "Sign Windows code on a configured central host",
      "description": "# Sign Windows code on a configured central host\n\nSet `windows_script_signing.enabled: true` in private environment settings. Configure\nhost, public_certificate_src, store_location, work_root and optional timestamp_server.\nNo environment host, domain, subject or private key is embedded in the shared code.\nOther environments can disable the signing integration. An existing AllSigned policy\nstill blocks unsigned deployment; the switch does not weaken Windows policy.\n\nProvision the selected signer first with `ansible-playbook playbooks/windows/setup_signing.yml\n--limit signer-example`. An optional pfx_src/pfx_password imports the existing key only\non that host, under SYSTEM/runas, with key_exportable false. An existing key can be used\nwithout a PFX source. The one-use PFX transport is removed even on failure. No key or\npassword is exported to execution hosts, SYSVOL, drop-ins, Git or SQLite.\n\nThe public certificate selects the exact thumbprint. Setup checks code-signing EKU,\nvalidity/private-key availability and signs a temporary probe. The configured store is\nLocalMachine by default; CurrentUser under SYSTEM means SYSTEM's user store. Prepare\nthat context deliberately. Existing keys are not silently migrated between stores.\n\nExecution hosts receive the public publisher certificate. Root trust is separate:\ntrust_self_signed_certificate is an explicit self-issued leaf exception; otherwise\ntrusted_root_certificates contains explicitly supplied CA roots. Certificate files are\nvalidated as public X.509 before transport. No PFX is accepted by the artifact builder.\n\nLibrary rollout prepares an explicit code manifest, signs on the chosen host under a\nper-batch mutex, fetches the signed bytes, and checks source-to-signed SHA mappings.\nAuthenticode is checked on the signer and again on the execution host before import.\nPS1, PSM1, PSD1 and PS1XML are covered. Unchanged valid batches are reused; source changes,\ncertificate rotation or timestamp-service changes produce a different batch identity.\nNo recursive signing of unknown host files occurs. All environment values remain variables.\n\nThe central task calls the same Set-AuthenticodeSignature mechanism as a local signer.\nTimestamping is optional and explicit. Signatures without a timestamp need certificate\nlifetime/rotation planning. A check-mode run performs no key import or signing. Portable\ntests mock Authenticode; the native Windows test script uses only a synthetic certificate. Automated\nCI publication is not configured with the current GitHub access. Real WinRM/runas/PFX and the environment trust chain still need a pilot.",
      "fields": {}
    },
    "de": {
      "title": "Windows-Code auf einem konfigurierten zentralen Host signieren",
      "description": "# Windows-Code auf einem konfigurierten zentralen Host signieren\n\n`windows_script_signing.enabled: true` schaltet die verpflichtende Signierstrecke für\ndas Deployment ein. Signierhost, öffentlicher CER, Store, Arbeits-/Cachepfade und\nZeitstempelserver stehen in privaten Variablen. Andere Umgebungen können abschalten;\neine bestehende AllSigned-Richtlinie wird dadurch nicht umgangen oder verändert.\n\nZuerst `playbooks/windows/setup_signing.yml --limit signer-example` ausführen. Optional\nwerden vorhandener PFX und Passwort lokal in den Settings angegeben. Import nur auf\ndem ausgewählten Host unter SYSTEM/runas, ohne Exportierbarkeit anzufordern. Die PFX-\nTransportdatei wird auch bei Fehlern entfernt. Bestehende Schlüssel können ohne erneuten\nPFX-Import verwendet werden. Private Schlüssel/Passwörter kommen nicht auf andere Hosts,\nnicht in SYSVOL, Drop-ins, Git oder SQLite.\n\nDer öffentliche CER bestimmt den exakten Thumbprint statt eines festen Subject-Namens.\nSetup prüft EKU, Gültigkeit und Schlüsselzugriff und signiert eine temporäre Probe.\nStandard ist LocalMachine. CurrentUser unter SYSTEM ist dessen Benutzerstore, nicht\nunbemerkt der Store eines interaktiv angemeldeten Administrators. Vorhandene Schlüssel\nwerden nicht still zwischen Stores verschoben.\n\nAusführungsziele erhalten nur den öffentlichen Publisher. Root-Vertrauen ist getrennt:\nDie selbst-ausgestellte Zertifikatsausnahme ist ausdrücklich schaltbar; andere CA-Roots\nwerden einzeln angegeben. Vor Transport wird öffentliches X.509 geprüft. Der Artefakt-\nbauer akzeptiert keinen PFX. Die Library wird anhand eines festen Manifests auf dem\nkonfigurierten Host signiert, per Mutex gegen parallele Änderungen geschützt und mit\ngetrennten Quell-/Signatur-SHA zurückgeholt. Native Signaturprüfung vor Import auch auf\ndem Ausführungsziel. PS1, PSM1, PSD1 und PS1XML werden signiert, unbekannte Hostdateien\nnicht rekursiv übernommen. Unveränderte gültige Batches werden wiederverwendet.\n\nVerwendet wird Set-AuthenticodeSignature wie im bisherigen Signer. Zeitstempelserver\nsind optional; ohne Zeitstempel die Zertifikatslaufzeit/Rotation beachten. Checkmode\nimportiert keinen Schlüssel und signiert nicht. Portable Tests verwenden Cmdlet-Doubles;\ndas native Windows-Testskript nutzt nur ein synthetisches Zertifikat. Ein automatischer\nCI-Workflow ist mit dem derzeitigen GitHub-Zugang nicht veröffentlicht. WinRM/runas/PFX\nund die echte Vertrauenskette dieser Umgebung müssen noch im Pilot bestätigt werden.",
      "fields": {}
    }
  }
}
```

</details>
