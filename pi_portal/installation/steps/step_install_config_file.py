"""StepInstallConfigFile class."""

import logging
import shutil

from pi_portal import config
from pi_portal.modules.system.file_system import FileSystem
from .bases import base_step


class StepInstallConfigFile(base_step.StepBase):
  """Install the user's configuration file.

  :param config_file_path: The path to the configuration file to install.
  :param log: The logging instance for this step.
  """

  config_file_path: str

  def __init__(
      self,
      log: logging.Logger,
      config_file_path: str,
  ) -> None:
    super().__init__(log)
    self.config_file_path = config_file_path

  def invoke(self) -> None:
    """Install the user's configuration file."""

    self.log.info("Installing the user's configuration file ...")
    shutil.copy(self.config_file_path, config.PATH_USER_CONFIG)
    self.log.info("Done writing the user's configuration file.")

    self.log.info("Setting permissions on the user's configuration file ...")
    fs = FileSystem(config.PATH_USER_CONFIG)
    fs.ownership(config.PI_PORTAL_USER, config.PI_PORTAL_USER)
    fs.permissions("600")
    self.log.info("Done setting permissions on the user's configuration file.")
