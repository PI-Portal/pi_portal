"""StepInitializeLogging class."""

import os

from pi_portal import config
from .bases import system_call_step


class StepInitializeLogging(system_call_step.SystemCallBase):
  """Initialize logging files for supervisor."""

  log_files = [
      config.LOG_FILE_DOOR_MONITOR,
      config.LOG_FILE_MOTION,
      config.LOG_FILE_SLACK_BOT,
      config.LOG_FILE_SLACK_CLIENT,
      config.LOG_FILE_TEMPERATURE_MONITOR,
      config.LOG_FILE_VIDEO_UPLOAD_CRON,
  ]

  def invoke(self) -> None:
    """Initialize logging files for supervisor."""

    self.log.info("Initializing logging ...")

    for log_file in self.log_files:

      self.log.info("Creating '%s' ...", log_file)
      if not os.path.exists(log_file):
        self._system_call(f"touch {log_file}")
      else:
        self.log.info("Found existing '%s' ...", log_file)

      self.log.info("Setting permissions on '%s' ...", log_file)
      self._system_call(
          f"chown {config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} "
          f"{log_file}"
      )
      self._system_call(f"chmod 600 {log_file}")

    self.log.info("Done initializing logging.")
