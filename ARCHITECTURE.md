[English](ARCHITECTURE.md) | [Deutsch](ARCHITECTURE.de.md)

# Controller architecture

A controller starts with Allgm. Add a profile when several controllers share the same setup, a Git add-on when a feature belongs on selected controllers, or a local playbook when a change belongs to just one installation.

```text
1  Allgm core (runtime, registry, shared roles and library) +
                                                            +--> /root/ansible/
2  Optional profile and Git add-ons ------------------------+
                                                                   |
                                                               update-check
                                                                   |
3  /root/ansible-local/  local files and receipts <----------------+

4  Private input: inventory, variables, secrets, script sources
```

## Which layer owns a change?

**Core.** `bin/control` loads command definitions from `bin/control.d/`. Each entry points to its handler. The CLI reads command titles from `descriptions/`. The optional TUI also uses the field definitions and help there. The description contract keeps schema version 1. Its optional `i18n.de` and `i18n.en` sections share field IDs, command arguments and source hashes. Older descriptions use their existing text. Language selection follows `--lang`, `CONTROLLER_LANG`, then `controller_lang` in the controller settings. The default is German.

**Profile and Git add-ons.** A profile such as Homelab declares its name and allowed core replacements in `controller-overlay.json`. An add-on declares its files in `controller-addon.json`. For example, SSS mounts its payload under `playbooks/security/sss/` and exports its command to `bin/control.d/` and its help to `descriptions/commands/`. Each installed path has an owner. A conflicting add-on path blocks installation.

**Local extensions.** Use `tools/local_extension.py` to approve a SHA-256 and install the file under `/root/ansible-local/code/`. The adjacent `register.json` records the approved revision. Its playbook can call shared roles. A one-time task can be archived after a successful run and explicit confirmation of the hash. The archive contains the file, checksum and run receipt. The checker audits this layer separately. Local runs and archiving are operator actions.

**Private data.** The operator maintains `inventory/`, `group_vars/`, `host_vars/`, any `secrets.yml`, and site scripts under `/root/skripte-config/`. A fresh install seeds local files from examples. Git updates manage the shipped code. Keep a separate backup of private data.

## From Git to rollback

1. **Select the sources.** Local `versions.txt` records `module|version|HTTPS-URL|token-file`. Public origins have an empty fourth field. For authenticated access it holds the path to a private token file. Register a Git add-on with both its module row and a `# addon=NAME` line. `bin/control module-versions` reports installed versions.
2. **Preview.** From the controller directory, `bin/control update-check --remote` checks `main`. Use `--staging` instead for staging. The selection applies to every active Git module for that invocation. The checker compares files against SHA-256 manifests and checks settings, the registry and overlapping paths. The manifests are unsigned. Release provenance depends on the trusted Git origin.
3. **Apply.** Run `bin/control update-check --apply`, adding `--staging` for a test controller. Installed version strings use `X.Y.Z` on main and `sX.Y.Z` on staging. The installation receipt `.controller-install.json` records managed file hashes, owners and module revisions. A code change creates a rollback snapshot in `.local/controller-updates/`. A configured cron job uses `--auto` and selects main even after a staging run. It retains snapshots for four days by default and always keeps the newest one.
4. **Roll back.** If you migrated the local register and the target checker requires schema 1, restore the register first. Use `python3 tools/migrate_local_extensions.py --rollback REGISTER_BACKUP` with the backup path printed by that migration. To restore the code, run `bin/control update-check --rollback SNAPSHOT_ID` with the ID printed during the code update.

[Developer guide in the Git repository](EXTENDING.md) · [Installation](descriptions/configurations/installation-allgm.md) · [Update and recovery commands](descriptions/commands/update-check.md)
