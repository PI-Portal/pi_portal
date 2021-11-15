#!/bin/bash

echo "Building arm binary for filebeat ..."

set -e

main() {
  rm -rf "${HOME}/go/"
  go get github.com/elastic/beats || true
  cd "${HOME}/go/src/github.com/elastic/beats/filebeat"
  git checkout v7.0.0
  GOOS=linux GOARCH=arm GOARM=7 go build
  mkdir -p /app/pi_portal/bin
  mv filebeat /app/pi_portal/bin/filebeat
}

main

