"""Pi Portal Supervisor configuration."""

from enum import Enum


class ProcessList(Enum):
  """Pi Portal Supervisor managed processes."""

  BOT = 'bot'
  CAMERA = 'camera'
  CONTACT_SWITCH_MONITOR = 'contact_switch_monitor'
  FILEBEAT = 'filebeat'
  TASK_SCHEDULER = "task_scheduler"
  TEMP_MONITOR = 'temp_monitor'


class ProcessStatus(Enum):
  """Supervisor process states."""

  FATAL = 'FATAL'
  RESTARTING = 'RESTARTING'
  RUNNING = 'RUNNING'
  SHUTDOWN = 'SHUTDOWN'
  STARTING = 'STARTING'
  STOPPED = 'STOPPED'
  STOPPING = 'STOPPING'
