#!/bin/bash

set -eo pipefail

PIB_PROJECT_ROOT="$(git rev-parse --show-toplevel)"
export PIB_PROJECT_ROOT

install_git_hooks() {
  pushd "${PIB_PROJECT_ROOT}"  > /dev/null
    set +e
      cd .git/hooks
      ln -sf ../../scripts/hooks/pre-commit pre-commit
    set -e
  popd  > /dev/null
}

pib_setup_hostmachine() {
  poetry install -E docs

  # shellcheck disable=SC2139
  alias dev="PROJECT_NAME=\"pi_portal\" PIB_CONFIG_FILE_LOCATION=\"${PIB_PROJECT_ROOT}/assets/cli.yml\" poetry run dev"
}
