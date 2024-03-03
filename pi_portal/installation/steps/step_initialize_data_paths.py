"""StepInitializeDataPaths class."""

import os

from pi_portal import config
from pi_portal.modules.system.file_system import FileSystem
from .bases import base_step


class StepInitializeDataPaths(base_step.StepBase):
  """Initialize data storage directories."""

  data_paths = [
      config.PATH_ARCHIVAL_QUEUE_LOG_UPLOAD,
      config.PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD,
      config.PATH_CAMERA_CONTENT,
      config.PATH_FILEBEAT_CONTENT,
      config.PATH_TASKS_SERVICE_DATABASES,
  ]

  def invoke(self) -> None:
    """Initialize data storage directories."""

    self.log.info("Initializing data paths ...")

    for path in self.data_paths:
      fs = FileSystem(path)
      self.log.info("Creating '%s' ...", path)
      if not os.path.exists(path):
        fs.create(directory=True)
      else:
        self.log.info("Found existing '%s' ...", path)

      self.log.info("Setting permissions on '%s' ...", path)
      fs.ownership(config.PI_PORTAL_USER, config.PI_PORTAL_USER)
      fs.permissions("750")

    self.log.info("Done initializing data paths.")
