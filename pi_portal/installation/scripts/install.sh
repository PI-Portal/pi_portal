#!/bin/bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


configure_log_file() {
  touch "$1"
  chown pi_portal:pi_portal "$1"
}

configure_motion() {
  service motion stop
  update-rc.d -f motion remove
  cp ./installation/motion/motion.conf /etc/motion/motion.conf
  mkdir -p /var/lib/motion
  chown root:pi_portal /var/lib/motion
  chmod 750 /var/lib/motion
}

configure_pi_portal() {
  mkdir -p /opt/pi_portal

  cp ./installation/scripts/portal.sh /opt/pi_portal/portal.sh
  cp "${CONFIG_FILE}" /opt/pi_portal/config.json

  chmod +x /opt/pi_portal/portal.sh
  chown -R pi_portal:pi_portal /opt/pi_portal
  chmod 700 /opt/pi_portal/config.json
}

configure_supervisor() {
  cp ./installation/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
}

help() {
  echo "You must run this command as root, with three arguments."
  echo "USAGE: sudo installer.sh [LOGZ_IO_CODE] [SUPERVISOR_SOCKET_PATH] [CONFIG_FILE_PATH]"
  exit 127
}

install_filebeat() {
  mkdir -p /etc/filebeat
  curl https://raw.githubusercontent.com/logzio/public-certificates/master/AAACertificateServices.crt --create-dirs -o /etc/pki/tls/certs/COMODORSADomainValidationSecureServerCA.crt

  cp ./installation/filebeat/filebeat.yml /etc/filebeat/filebeat.yml
  cp ./bin/filebeat /usr/bin/filebeat

  chmod +x /usr/bin/filebeat
  chown root:root /etc/filebeat/filebeat.yml
  sed -i "s/<<LOGZ_IO_CODE>>/${LOGZ_IO_CODE}/g" /etc/filebeat/filebeat.yml
}

safely_start_supervisor() {
  if [[ -S "${SUPERVISOR_SOCKET_PATH}" ]]; then
    service supervisor stop
    sleep 7
  fi

  service supervisor start
}

main() {
  pushd "${SCRIPT_DIR}" || exit 127
    cd ../..

    adduser --disabled-login --gecos "" --shell /bin/false --no-create-home pi_portal

    install_filebeat

    configure_log_file "/var/log/pi_portal.door.log"
    configure_log_file "/var/log/pi_portal.slack_bot.log"
    configure_log_file "/var/log/pi_portal.slack_client.log"
    configure_log_file "/var/log/pi_portal.temperature.log"

    configure_supervisor
    configure_pi_portal
    configure_motion

    safely_start_supervisor

  popd || exit 127
}

[[ "$(id -u)" -ne 0 ]] && help
[[ -z "${1}" ]] || [[ -z "${2}" ]] || [[ -z "${3}" ]] && help

LOGZ_IO_CODE="${1}"
SUPERVISOR_SOCKET_PATH="${2}"
CONFIG_FILE="${3}"

main "$@"
