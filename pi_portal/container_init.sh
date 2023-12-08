#!/bin/bash


DEVELOPMENT() {
  pushd "pi_portal" || exit 127
  while true; do sleep 1; done
}

eval "${ENVIRONMENT}"
