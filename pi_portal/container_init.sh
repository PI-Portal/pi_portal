#!/bin/bash


DEVELOPMENT() {
  # Support Docker-in-Docker
  sudo chmod g+rw /var/run/docker.sock
  sudo chgrp user /var/run/docker.sock

  pushd "pi_portal" || exit 127
  while true; do sleep 1; done
}

eval "${ENVIRONMENT}"
