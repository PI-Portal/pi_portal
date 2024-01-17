"""StepInitializeEtc class."""

import os

from pi_portal.modules.system.file_system import FileSystem
from .bases import base_step


class StepInitializeEtc(base_step.StepBase):
  """Initialize etc paths for configuration."""

  etc_paths = [
      "/etc/filebeat",
      "/etc/motion",
      "/etc/pi_portal",
      "/etc/pki/tls/certs",
  ]

  def invoke(self) -> None:
    """Initialize etc paths for configuration."""

    self.log.info("Initializing etc paths ...")

    for etc_path in self.etc_paths:
      fs = FileSystem(etc_path)

      self.log.info("Creating '%s' ...", etc_path)
      if not os.path.exists(etc_path):
        fs.create(directory=True)
      else:
        self.log.info("Found existing '%s' ...", etc_path)

      self.log.info("Setting permissions on '%s' ...", etc_path)
      fs.ownership("root", "root")
      fs.permissions("755")

    self.log.info("Done initializing etc paths.")
