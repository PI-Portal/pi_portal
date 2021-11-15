#!/bin/bash

set -eo pipefail

main() {

  shellcheck ./.github/scripts/*.sh
  shellcheck ./"pi_portal"/*.sh
  shellcheck ./scripts/*.sh
  shellcheck ./scripts/hooks/*

}

main "$@"
