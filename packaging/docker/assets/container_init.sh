#!/bin/bash

set -eo pipefail

ERROR() {
  # 1   The error message.

  echo "${1}"
  exit 127
}

PRODUCTION() {
  [[ ! -e "/dev/gpiomem" ]] && ERROR "The gpiomem device is not mounted!"
  [[ -z "$(ls /dev/video*)" ]] && ERROR "No video device has been mounted!"
  [[ ! -f "/config.json" ]] && ERROR "No pi_portal configuration has been mounted!"

  if ! grep -q gpio /etc/group; then
    groupadd -g "$(stat -c '%g' /dev/gpiomem)" gpio
    usermod -a -G gpio pi_portal
  fi

  portal install_config -y /config.json

  while true; do sleep 1; done
}

eval "${ENVIRONMENT}"
