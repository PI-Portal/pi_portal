#!/bin/bash

# Manages the packaging process for the project's binaries on various architectures.

# CI only script.

# BRANCH_OR_TAG                 The branch or tag this build has been triggered for.
# ENV_SECRET_1                  The GitHub authentication token for this build.
# MANIFEST_ANNOTATION           An annotation to add to the multiarch image.
# PACKAGING_IMAGE_NAME          The version of python for this debian distribution.
# PACKAGING_REGISTRY_NAME       The distribution of debian that the package is being built for.

set -eo pipefail

IMAGE_NAME="${PACKAGING_REGISTRY_NAME}/${PACKAGING_IMAGE_NAME}"

read -r -d' ' -a ARCHITECTURES < <(yq -r 'to_entries | sort_by(.keys) | .[].key' packaging/docker/assets/architectures.yml) || true

docker_build() {
  pushd packaging/docker > /dev/null

  python ../utils/generate_compose.py assets/architectures.yml > docker-compose.yml

  docker compose build

  echo "All Docker images have been built successfully!"
  popd > /dev/null
}

docker_login() {
  echo "${ENV_SECRET_1}" | docker login -u USER --password-stdin "${PACKAGING_REGISTRY_NAME}"

  echo "Successful login to Docker registry!"
}

docker_package() {
  local ARCHITECTURE

  declare -a SOURCE_IMAGES

  pushd packaging/docker > /dev/null

  for ARCHITECTURE in "${ARCHITECTURES[@]}"; do
    docker push "${IMAGE_NAME}:${ARCHITECTURE}"
    SOURCE_IMAGES+=("${IMAGE_NAME}:${ARCHITECTURE}")
  done

  # shellcheck disable=SC2068
  docker buildx imagetools create \
    -t \
    "${IMAGE_NAME}:multiarch" \
    ${SOURCE_IMAGES[@]}

  # shellcheck disable=SC2068
  docker buildx imagetools create \
    -t \
    "${IMAGE_NAME}:${BRANCH_OR_TAG}" \
    ${SOURCE_IMAGES[@]}

  # shellcheck disable=SC2068
  docker buildx imagetools create \
    -t \
    "${IMAGE_NAME}:latest" \
    ${SOURCE_IMAGES[@]}

  mkdir -p dist
  docker images "${IMAGE_NAME}" --no-trunc > dist/images.txt

  echo "All Docker images are ready for distribution.!"

  popd > /dev/null
}

main() {
  docker_build
  docker_login
  docker_package
}

main "$@"
