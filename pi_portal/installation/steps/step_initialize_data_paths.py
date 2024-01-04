"""StepInitializeDataPaths class."""

import os

from pi_portal import config
from .bases import system_call_step


class StepInitializeDataPaths(system_call_step.SystemCallBase):
  """Initialize data storage directories."""

  data_paths = [config.PATH_VIDEO_UPLOAD_QUEUE]

  def invoke(self) -> None:
    """Initialize data storage directories."""

    self.log.info("Initializing data paths ...")

    for path in self.data_paths:

      self.log.info("Creating '%s' ...", path)
      if not os.path.exists(path):
        self._system_call(f"mkdir -p {path}")
      else:
        self.log.info("Found existing '%s' ...", path)

      self.log.info("Setting permissions on '%s' ...", path)
      self._system_call(
          f"chown {config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} {path}"
      )
      self._system_call(f"chmod 750 {path}")

    self.log.info("Done initializing data paths.")
