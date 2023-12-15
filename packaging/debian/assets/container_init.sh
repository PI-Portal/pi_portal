#!/bin/bash

set -eo pipefail

DEBPATH="build_${PACKAGING_ARCH}_${PACKAGING_DEBIAN_VERSION}"
DISTPATH="dist_${PACKAGING_ARCH}_${PACKAGING_DEBIAN_VERSION}"
PACKAGING_VERSION="$(poetry version -s)-${PACKAGING_ARCH}"

export DEBPATH
export DISTPATH
export PACKAGING_VERSION

DEVELOPMENT() {
  pushd "pi_portal" || exit 127
  while true; do sleep 1; done
}

PACKAGE() {

  build() {
    local FILE

    mkdir -p "${DEBPATH}"
    cp -vr "assets/debian" "${DEBPATH}"
    envsubst < assets/debian/changelog > "${DEBPATH}/debian/changelog"
    envsubst < assets/debian/control > "${DEBPATH}/debian/control"
    pushd "${DEBPATH}" || exit 127
    dpkg-buildpackage --build=binary
    popd || exit 127

    mkdir -p "${DISTPATH}"
    for FILE in ./*-"${PACKAGING_ARCH}_${DEB_ARCH}.deb"; do
      mv "${FILE}" "${DISTPATH}/${FILE/${PACKAGING_ARCH}_${DEB_ARCH}./${PACKAGING_ARCH}_${PACKAGING_DEBIAN_VERSION}.}"
    done
    uptime -p
  }

  clean() {
    rm -rf "${DEBPATH}"
    rm -f "${DISTPATH}"
  }

  package() {
    cd packaging/debian || exit 127

    clean
    build
  }

  time package

}

eval "${ENVIRONMENT}"
