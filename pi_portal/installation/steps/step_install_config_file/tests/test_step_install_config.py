"""Test the StepInstallPiPortalConfigFile class."""
import logging

from ...utility.generate_step_test import GenericStepTest
from .. import (
    StepInstallPiPortalConfigFile,
    action_copy_config_file,
    action_create_paths,
)


class TestStepInstallPiPortalConfigFile(GenericStepTest):
  """Test the StepInstallPiPortalConfigFile class."""

  step_class = StepInstallPiPortalConfigFile
  action_classes = [
      action_create_paths.CreatePiPortalPathsAction,
      action_copy_config_file.CopyPiPortalUserConfigAction
  ]

  def test_initialize__attributes(self,) -> None:
    assert self.step_class.logging_begin_message == (
        "Installing the user's configuration file ..."
    )
    assert self.step_class.logging_end_message == (
        "Done installing the user's configuration file."
    )

  def test_initialize__sets_config_file(
      self,
      installer_logger_stdout: logging.Logger,
  ) -> None:
    mock_config_file = "/path/to/mock_config.json"

    self.step_class(installer_logger_stdout, mock_config_file)

    assert (
        action_copy_config_file.CopyPiPortalUserConfigAction.config_file_path ==
        mock_config_file
    )
