"""Core configuration settings."""

from enum import Enum


class DoorNames(Enum):
  """Names for the doors."""

  FRONT = 1
  BACK = 2


GPIO_SWITCHES = {
    1: 13,
    2: 5
}

GPIO_INITIAL_STATE = {
    1: None,
    2: None
}

LOGFILE_PATH = "/var/log/pi_portal.log"
MOTION_FOLDER = "/var/lib/motion"
SUPERVISOR_SOCKET_PATH = "/var/run/supervisor.sock"
