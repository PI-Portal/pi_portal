"""StepInstallConfigFile class."""

import logging
import shutil

from pi_portal import config
from .bases import system_call_step


class StepInstallConfigFile(system_call_step.SystemCallBase):
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
    self._system_call(
        f"chown {config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} "
        f"{config.PATH_USER_CONFIG}"
    )
    self._system_call(f"chmod 600 {config.PATH_USER_CONFIG}")
    self.log.info("Done setting permissions on the user's configuration file.")
