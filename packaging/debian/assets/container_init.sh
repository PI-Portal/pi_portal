#!/bin/bash

set -eo pipefail

DEVELOPMENT() {
  pushd "pi_portal" || exit 127
  while true; do sleep 1; done
}

PACKAGE() {

  build() {
    mkdir -p "${DEBPATH}"
    cp -vr "assets/debian" "${DEBPATH}"
    envsubst < assets/debian/control > "${DEBPATH}/debian/control"
    pushd "${DEBPATH}" || exit 127
    dpkg-buildpackage --build=binary
    popd || exit 127

    mkdir -p "${DISTPATH}"
    mv ./*_"${DEB_BUILD_ARCH}".{buildinfo,changes,deb} "${DISTPATH}"

    uptime -p
  }

  clean() {
    rm -rf "${DEBPATH}"
    rm -rf "${DISTPATH}"
  }

  package() {

    cd packaging/debian || exit 127

    clean
    build
  }

  time package

}

eval "${ENVIRONMENT}"
