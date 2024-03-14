"""StepInstallConfigFile class."""

import logging

from ..bases import base_step
from . import action_copy_config_file, action_create_paths


class StepInstallPiPortalConfigFile(base_step.StepBase):
  """Install the user's pi_portal configuration file.

  :param log: The logging instance for this step.
  :param config_file_path: The path to the configuration file to install.
  """

  actions = [
      action_create_paths.CreatePiPortalPathsAction,
      action_copy_config_file.CopyPiPortalUserConfigAction,
  ]
  logging_begin_message = "Installing the user's configuration file ..."
  logging_end_message = "Done installing the user's configuration file."

  def __init__(
      self,
      log: logging.Logger,
      config_file_path: str,
  ) -> None:
    super().__init__(log)
    action_copy_config_file.CopyPiPortalUserConfigAction.config_file_path = (
        config_file_path
    )
