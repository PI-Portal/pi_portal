#!/bin/bash

DEVELOPMENT() {
  pushd "pi_portal" || exit 127
  while true; do sleep 1; done
}

PRODUCTION() {
  pi_portal
}

eval "${ENVIRONMENT}"
