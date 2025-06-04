#!/bin/bash

# Manages the packaging process for the project's binaries on various architectures.

# CI only script.

set -eo pipefail

FILEBEAT_VERSION="8.11.0"

read -r -d' ' -a ARCHITECTURES < <(yq -r 'to_entries | sort_by(.keys) | .[].key' packaging/filebeat/assets/architectures.yml) || true

export FILEBEAT_VERSION

FILEBEAT_PERMISSIONS="root:root"
FILEBEAT_TAR_BINARY="tar"

fail() {
  echo "ERROR: $1"
  exit 127
}

filebeat_build() {
  pushd packaging/filebeat > /dev/null

  python ../utils/generate_compose.py assets/architectures.yml > docker-compose.yml

  docker compose up

  ls bin/* || fail "filebeat build failed!"

  echo "Filebeat has been built successfully!"

  popd > /dev/null
}

filebeat_package() {
  local ARCHITECTURE

  pushd packaging/filebeat/bin > /dev/null

  echo "Packaging filebeat for distribution ..."

  mkdir -p ../dist

  sudo chown "${FILEBEAT_PERMISSIONS}" ./*

  for ARCHITECTURE in "${ARCHITECTURES[@]}"; do
    "${FILEBEAT_TAR_BINARY}" --transform "s|filebeat-${ARCHITECTURE}|filebeat|" -cvzf ../dist/"filebeat-linux-${FILEBEAT_VERSION}-${ARCHITECTURE}.tar.gz" "filebeat-${ARCHITECTURE}"
  done

  ls -la ../dist/*

  echo "Filebeat is ready for distribution."

  popd > /dev/null
}

osx_support() {
  if [[ "$(uname -s)" == "Darwin" ]]; then
    FILEBEAT_PERMISSIONS="root:wheel"
    FILEBEAT_TAR_BINARY="/usr/local/opt/gnu-tar/libexec/gnubin/tar"
  fi
}

main() {
  osx_support
  filebeat_build
  filebeat_package
}

main "$@"
