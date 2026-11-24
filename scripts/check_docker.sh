#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
ansible-playbook playbooks/docker/deploy_docker_networks.yaml --syntax-check "$@"
ansible-playbook playbooks/docker/check_docker.yml --syntax-check "$@"
selection=$(ANSIBLE_NOCOLOR=1 ansible-playbook playbooks/docker/check_docker.yml --list-hosts "$@")
if ! grep -Eq 'hosts \([1-9][0-9]*\):' <<< "$selection"; then
  echo 'FEHLER: Keine Docker-Zielhosts ausgewaehlt. Inventory, Gruppe und Limit pruefen.' >&2
  exit 2
fi
exec ansible-playbook playbooks/docker/check_docker.yml "$@"
