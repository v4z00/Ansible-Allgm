[English](README.md) | [Deutsch](README.de.md)

# Ansible-Allgm

A hardened Ansible controller framework for Debian 12 and 13. The shared core generates inventory from Proxmox, manages Docker stacks, integrates with Checkmk and records jobs in a local SQLite database. One optional site profile and additional add-ons share the same SHA-256 update and rollback process.

## Who is it for?

This is the base I use for repeatable maintenance across a fleet. It fits internal IT teams, service providers and larger Proxmox or Docker homelabs where someone needs to see what ran, which version is installed and how to undo a rollout. For three Raspberry Pis, a single role or a few shell functions will usually be easier to run on their own. [Roles](roles/) · [Script library](artifacts/script-library/) · [Standalone SSS recovery kit](https://github.com/v4z00/Ansible-SSS)

## Get started

Use the Debian installer for a fresh controller. On an existing one, follow the migration steps first. From the installed directory, `bin/control list` shows the commands and `bin/control module-versions` lists the installed modules. For English CLI output, set `CONTROLLER_LANG=en` or use `bin/control --lang en help`. [Installation](descriptions/configurations/installation-allgm.md#install-on-debian) · [Update and rollback](ARCHITECTURE.md#from-git-to-rollback)

Development and testing take place on `staging`. The installer and scheduled updates use `main`. [Architecture](ARCHITECTURE.md) · [Extend the controller](EXTENDING.md) · [Changelog](descriptions/releases/allgm.md) · [GitHub releases](https://github.com/v4z00/Ansible-Allgm/releases)

## Related projects

- [Ansible-Homelab](https://github.com/v4z00/Ansible-Homelab) adds a site profile with backup, storage and OpenWrt playbooks.
- [Ansible-TUI](https://github.com/v4z00/Ansible-TUI) presents the installed controller’s commands and descriptions in a terminal interface.
- [Ansible-SSS](https://github.com/v4z00/Ansible-SSS) splits recovery material into shares. It runs on its own or as a controller add-on.

I use AI to help write and maintain this project. I do little of the implementation by hand. If a workflow behaves differently on your system, an issue with the command, version and expected result helps me reproduce it. [Issues](https://github.com/v4z00/Ansible-Allgm/issues) · [MIT licence](LICENSE)
