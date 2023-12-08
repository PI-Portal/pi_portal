#!/bin/bash

set -eo pipefail

PYTHON_VERSION="3.9"
TESTING_IMAGE="debian:sid-slim"

build_filebeat() {
 pushd packaging/filebeat > /dev/null

 docker-compose up
 echo "Filebeat has been built successfully!"

 popd > /dev/null
}

build_debian() {
  pushd packaging/debian > /dev/null

  docker-compose build --build-arg BUILD_ARG_PYTHON_VERSION="${PYTHON_VERSION}" arm64-prebuild armv7-prebuild
  docker-compose build arm64 armv7

  docker-compose up arm64 armv7

  echo "Debian packages have been built successfully!"

  popd > /dev/null
}

test_debian_32() {

  docker rmi -f "${TESTING_IMAGE}" || true

  docker run                                      \
    --platform linux/arm/v7                       \
    --rm                                          \
    -it                                           \
    -e PI_PORTAL_MOCK_GPIO=1                      \
    -v "$(pwd)/packaging/debian/dist_armhf:/dist" \
    "${TESTING_IMAGE}" bash -c "
      cd /dist &&
      apt-get update &&
      apt-get install -yf ./pi-portal_*_armhf.deb &&
      portal version
    "
  echo "32 bit install completed successfully!"

}

test_debian_64() {

  docker rmi -f "${TESTING_IMAGE}" || true

  docker run                                      \
    --platform linux/arm64                        \
    --rm                                          \
    -it                                           \
    -e PI_PORTAL_MOCK_GPIO=1                      \
    -v "$(pwd)/packaging/debian/dist_arm64:/dist" \
    "${TESTING_IMAGE}" bash -c "
      cd /dist &&
      apt-get update &&
      apt-get install -yf ./pi-portal_*_arm64.deb &&
      portal version
    "
  echo "64 bit install completed successfully!"

}

main() {

  build_filebeat
  build_debian

  test_debian_32
  test_debian_64

}

main "$@"

