#!/bin/bash

DEVELOPMENT() {
  # Support Docker-in-Docker
  sudo chmod g+rw /var/run/docker.sock
  sudo chgrp user /var/run/docker.sock

  # Symlink the Default Configuration
  sudo ln -sf /app/config.json /etc/pi_portal/config.json

  pushd "pi_portal" || exit 127
  while true; do sleep 1; done
}

eval "${ENVIRONMENT}"
