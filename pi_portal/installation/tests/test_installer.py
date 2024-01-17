"""Test the Installer class."""

import logging
from io import StringIO
from typing import List
from unittest import mock

from pi_portal.installation.templates import config_file
from .. import installer

INSTALL_MODULE = installer.__name__
CONFIG_FILE_MODULE = config_file.__name__


class TestInstaller:
  """Test the Installer class."""

  def test_instantiate__attrs(
      self,
      installer_instance: installer.Installer,
      mocked_config_file_path: str,
  ) -> None:
    assert installer_instance.config_file_path == mocked_config_file_path
    assert installer_instance.logger_name == "Installer"
    assert installer_instance.logger_level == logging.INFO
    assert isinstance(installer_instance.log, logging.Logger)

  def test_install__initializes_all_steps(
      self,
      installer_instance: installer.Installer,
      mocked_steps: List[mock.Mock],
  ) -> None:
    installer_instance.install()

    mocked_steps[0].assert_called_once_with(installer_instance.log)
    mocked_steps[1].assert_called_once_with(installer_instance.log)
    mocked_steps[2].assert_called_once_with(installer_instance.log)
    mocked_steps[3].assert_called_once_with(installer_instance.log)
    mocked_steps[4].assert_called_once_with(installer_instance.log)
    mocked_steps[5].assert_called_once_with(installer_instance.log)
    mocked_steps[6].assert_called_once_with(installer_instance.log)
    mocked_steps[7].assert_called_once_with(installer_instance.log)
    mocked_steps[8].assert_called_once_with(
        installer_instance.log,
        installer_instance.config_file_path,
    )
    mocked_steps[9].assert_called_once_with(installer_instance.log)
    mocked_steps[10].assert_called_once_with(installer_instance.log)

  def test_install__invokes_all_steps(
      self,
      installer_instance: installer.Installer,
      mocked_steps: List[mock.Mock],
  ) -> None:
    installer_instance.install()

    for step in mocked_steps:
      step_instance = step.return_value
      step_instance.invoke.assert_called_once_with()

  def test_install__logs_beginning_and_end(
      self,
      installer_instance: installer.Installer,
      mocked_stream: StringIO,
  ) -> None:
    installer_instance.install()

    assert mocked_stream.getvalue() == \
           (
            "Installer - INFO - Beginning installation ...\n"
            "Installer - INFO - Installation complete.\n"
           )
