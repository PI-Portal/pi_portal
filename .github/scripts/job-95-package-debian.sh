#!/bin/bash

# Manages the packaging process for the project's binaries on various architectures.
# (Requires a fresh sdist created with `poetry build`.)

# CI only script.

# PACKAGING_DEBIAN_VERSION      The distribution of debian that the package is being built for.
# PACKAGING_PYTHON_VERSION      The version of python for this debian distribution.

set -eo pipefail

BUILD_USER="$(whoami)"
BUILD_GROUP="${BUILD_USER}"
DOCKER_USER_UID="$(id -u)"
BUILD_PYTHON_VERSION="3.9"

read -r -d' ' -a ARCHITECTURES < <(yq -r 'to_entries | sort_by(.keys) | .[].key' packaging/debian/assets/architectures.yml) || true
read -r -d' ' -a PLATFORMS < <(yq -r 'to_entries | sort_by(.keys) | .[].value.PLATFORM' packaging/debian/assets/architectures.yml) || true

export DOCKER_USER_UID
export BUILD_PYTHON_VERSION

debian_build() {
  local ARCHITECTURE

  pushd packaging/debian > /dev/null

  python ../utils/generate_compose.py assets/architectures.yml > docker-compose.yml

  # shellcheck disable=SC2046
  docker compose build $(get_services prebuild)
  # shellcheck disable=SC2046
  docker compose build $(get_services package)
  # shellcheck disable=SC2046
  docker compose up $(get_services package)

  for ARCHITECTURE in "${ARCHITECTURES[@]}"; do
    validate_debian_build "${ARCHITECTURE}"
  done

  echo "All Debian packages have been built successfully!"
  popd > /dev/null
}

debian_package() {
  local ARCHITECTURE

  pushd packaging/debian > /dev/null

  sudo chown "${BUILD_USER}":"${BUILD_GROUP}" -R dist*

  mkdir -p dist

  for ARCHITECTURE in "${ARCHITECTURES[@]}"; do
    validate_debian_build "${ARCHITECTURE}"
    debian_package_architecture "${ARCHITECTURE}"
  done

  ls dist/* || fail "Aggregate Debian distribution build failed!"

  echo "Debian packages are ready for distribution."

  popd > /dev/null
}

debian_package_architecture() {
  # $1 distribution arch

  cp "dist_${1}_${PACKAGING_DEBIAN_VERSION}"/* dist
}

debian_test() {
  local ARCHITECTURE
  local INDEX=0

  pushd packaging/debian > /dev/null

  for ARCHITECTURE in "${ARCHITECTURES[@]}"; do
    echo "${PLATFORMS[${INDEX}]}"
    echo "" > "result_${ARCHITECTURE}"
    multiarch_to_specific "${PLATFORMS[${INDEX}]}" "test:${PACKAGING_DEBIAN_VERSION}-${ARCHITECTURE}" "${PACKAGING_DEBIAN_VERSION}"
    ((INDEX++)) || true
  done

  docker images

  # shellcheck disable=SC2046
  docker compose up $(get_services test)

  for ARCHITECTURE in "${ARCHITECTURES[@]}"; do
    validate_debian_test "${ARCHITECTURE}"
  done

  echo "All Debian packages have passed an install test!"

  popd > /dev/null
}

fail() {
  echo "ERROR: $1"
  exit 127
}

get_services() {
  # $1 - Substring filter

  docker compose config --services |
    grep "${1}"
}

multiarch_to_specific() {
  # $1  Platform
  # $2  New Tag
  # $3  Debian Version

  docker pull --platform "${1}" "debian:${3}"
  docker tag "debian:${3}" "${2}"
  docker rmi "debian:${3}"
}

osx_support() {
  if [[ "$(uname -s)" == "Darwin" ]]; then
    BUILD_GROUP="staff"
  fi
}

unpack_filebeat() {
  pushd packaging/filebeat/dist > /dev/null

  mkdir -p ../bin

  for ARCHITECTURE in "${ARCHITECTURES[@]}"; do
    tar xvzf "filebeat-linux-"*"-${ARCHITECTURE}.tar.gz"
    mv filebeat "../bin/filebeat-${ARCHITECTURE}"
  done

  ls -la ../bin/* || fail "Filebeat distributions could not be unpacked!"

  echo "All Filebeat distributions have been unpacked!"

  popd > /dev/null
}

validate_debian_build() {
  # $1 distribution arch

  ls "dist_${1}_${PACKAGING_DEBIAN_VERSION}"/* || fail "${1} Debian package build failed!"
}

validate_debian_test() {
  # $1 distribution arch

  local RESULT
  RESULT="$(cat "result_${1}")"

  echo "result_${1}: ${RESULT}"
  [[ -n "${RESULT}" ]] || fail "${1} Debian package install test failed!"
}

main() {
  osx_support
  unpack_filebeat
  debian_build
  debian_test
  debian_package
}

main "$@"
