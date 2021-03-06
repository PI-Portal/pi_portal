"""Pi Portal Supervisor configuration."""

from enum import Enum


class ProcessList(Enum):
  """Pi Portal Supervisor managed processes."""

  BOT = 'bot'
  CAMERA = 'camera'
  DOOR_MONITOR = 'door_monitor'
  FILEBEAT = 'filebeat'
  TEMP_MONITOR = 'temp_monitor'


class ProcessStatus(Enum):
  """Supervisor process states."""

  FATAL = 'FATAL'
  RESTARTING = 'RESTARTING'
  RUNNING = 'RUNNING'
  SHUTDOWN = 'SHUTDOWN'
  STOPPED = 'STOPPED'
