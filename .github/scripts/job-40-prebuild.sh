#!/bin/bash

# Prepares the GitHub Action runner to build the project's containers.

# 1:    The python version of the container to pre-pull for docker.

# CI only script.

set -eo pipefail

config_mocks() {
  echo | ssh-keygen
  touch "${HOME}/.gitconfig"
  touch "${HOME}/.gitconfig_global"
}

dind() {
  sudo chmod o+rwx /var/run/docker.sock
}

pull() {
  # 1:  The python version of the container to pre-pull for docker.

  docker pull "python:${1}-slim"
}

main() {
  # 1:  The python version of the container to pre-pull for docker.

  config_mocks
  dind
  pull "${1}"

}

main "$@"
