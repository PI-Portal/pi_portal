"""StepInitializeLogging class."""

import os

from pi_portal import config
from pi_portal.modules.system.file_system import FileSystem
from .bases import base_step


class StepInitializeLogging(base_step.StepBase):
  """Initialize logging files for supervisor."""

  log_files = [
      config.LOG_FILE_CRON_SCHEDULER,
      config.LOG_FILE_DOOR_MONITOR,
      config.LOG_FILE_MOTION,
      config.LOG_FILE_SLACK_BOT,
      config.LOG_FILE_SLACK_CLIENT,
      config.LOG_FILE_TEMPERATURE_MONITOR,
  ]

  def invoke(self) -> None:
    """Initialize logging files for supervisor."""

    self.log.info("Initializing logging ...")

    self._create_logging_base_folder()

    for log_file in self.log_files:
      self.log.info("Creating '%s' ...", log_file)
      fs = FileSystem(log_file)

      if not os.path.exists(log_file):
        fs.create()
      else:
        self.log.info("Found existing '%s' ...", log_file)

      self.log.info("Setting permissions on '%s' ...", log_file)
      fs.ownership(config.PI_PORTAL_USER, config.PI_PORTAL_USER)
      fs.permissions("600")

    self.log.info("Done initializing logging.")

  def _create_logging_base_folder(self) -> None:
    self.log.info("Creating '%s' ...", config.LOG_FILE_BASE_FOLDER)
    fs = FileSystem(config.LOG_FILE_BASE_FOLDER)

    if not os.path.exists(config.LOG_FILE_BASE_FOLDER):
      fs.create(directory=True)
    else:
      self.log.info("Found existing '%s' ...", config.LOG_FILE_BASE_FOLDER)

    self.log.info(
        "Setting permissions on '%s' ...",
        config.LOG_FILE_BASE_FOLDER,
    )
    fs.ownership(config.PI_PORTAL_USER, config.PI_PORTAL_USER)
    fs.permissions("750")
