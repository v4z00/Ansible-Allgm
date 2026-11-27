[English](README.md) | [Deutsch](README.de.md)

# Ansible-Allgm

A hardened Ansible controller framework for Debian 12 and 13. The shared core generates inventory from Proxmox, manages Docker stacks, integrates with Checkmk and records jobs in a local SQLite database. One optional site profile and additional add-ons share the same SHA-256 update and rollback process.

## Who is it for?

This is the base I use for repeatable maintenance across a fleet. It fits internal IT teams, service providers and larger Proxmox or Docker homelabs where someone needs to see what ran, which version is installed and how to undo a rollout. For three Raspberry Pis, a single role or a few shell functions will usually be easier to run on their own. [Roles](roles/) · [Script library](artifacts/script-library/) · [Standalone SSS recovery kit](https://github.com/v4z00/Ansible-SSS)

## A first look at the controller

Suppose you want to patch a group of Debian guests. Start in the controller directory and inspect what it knows. These commands can be run before choosing a target:

```sh
bin/control module-versions
bin/control list
bin/control --lang en help
```

The inventory identifies the hosts. The command registry connects each operation to a script or playbook. The catalog describes the parameters, so the same operation can be opened in the TUI. For example, the baseline asks you to supply an inventory limit or explicitly select all targets. [Baseline and target selection](descriptions/commands/base.md)

| Where to look | What lives there |
| --- | --- |
| [playbooks/](playbooks/) and [roles/](roles/) | Operations such as host maintenance, certificate deployment and Docker stack updates. |
| [bin/control.d/](bin/control.d/) and [descriptions/](descriptions/) | Command registrations and the instructions shown to operators. |
| [examples/first_run/](examples/first_run/) | Starter inventory and settings for a new controller. Real host and group variables belong on the controller. |
| [artifacts/script-library/](artifacts/script-library/) | Functions and job reporting shared with local scripts. |

For a release check, `bin/control update-check --remote` compares the installed modules with the stable branch. Review that result before running `--apply`.

## Get started

Use the Debian installer for a fresh controller. On an existing one, follow the migration steps first. From the installed directory, `bin/control list` shows the commands and `bin/control module-versions` lists the installed modules. Existing controllers default to German when no preference is set. For English CLI output, set `CONTROLLER_LANG=en` or use `bin/control --lang en help`. [Installation](descriptions/configurations/installation-allgm.md#install-on-debian) · [Update and rollback](ARCHITECTURE.md#from-git-to-rollback)

Development and testing take place on `staging`. The installer and scheduled updates use `main`. [Architecture](ARCHITECTURE.md) · [Extend the controller](EXTENDING.md) · [Changelog](descriptions/releases/allgm.md) · [GitHub releases](https://github.com/v4z00/Ansible-Allgm/releases)

## Language on an existing controller

No migration is needed to keep German. To try English for a single command, run `bin/control --lang en help`. To save German explicitly, run the [language helper](tools/set-controller-language.py) from the controller directory. It defaults to German, previews with `--check` and backs up the settings file before a change.

```sh
.venv/bin/python tools/set-controller-language.py --check
.venv/bin/python tools/set-controller-language.py
```

## Related projects

- [Ansible-Homelab](https://github.com/v4z00/Ansible-Homelab) adds a site profile with backup, storage and OpenWrt playbooks.
- [Ansible-TUI](https://github.com/v4z00/Ansible-TUI) presents the installed controller’s commands and descriptions in a terminal interface.
- [Ansible-SSS](https://github.com/v4z00/Ansible-SSS) splits recovery material into shares. It runs on its own or as a controller add-on.

I use AI to help write and maintain this project. I do little of the implementation by hand. If a workflow behaves differently on your system, an issue with the command, version and expected result helps me reproduce it. [Issues](https://github.com/v4z00/Ansible-Allgm/issues) · [MIT licence](LICENSE)
