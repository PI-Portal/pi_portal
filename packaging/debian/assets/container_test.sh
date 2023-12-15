#!/bin/bash

set -eo pipefail

main() {
  apt-get update
  apt-get install -yf "/mnt/dist_${PACKAGING_ARCH}_${PACKAGING_DEBIAN_VERSION}/pi-portal_"*"-${PACKAGING_ARCH}_${PACKAGING_DEBIAN_VERSION}.deb"
  portal version > "/mnt/result_${PACKAGING_ARCH}"
}

main "$@"
