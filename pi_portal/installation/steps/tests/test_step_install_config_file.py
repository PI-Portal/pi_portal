"""Test the StepInstallConfigFile class."""
import logging
from io import StringIO
from unittest import mock

import pytest
from pi_portal import config
from ..bases import system_call_step
from ..step_install_config_file import StepInstallConfigFile


class TestStepInstallConfigFile:
  """Test the StepInstallConfigFile class."""

  def test__initialize__attrs(
      self,
      step_install_config_files_instance: StepInstallConfigFile,
      mocked_config_file: str,
  ) -> None:
    assert isinstance(step_install_config_files_instance.log, logging.Logger)
    assert step_install_config_files_instance.config_file_path == \
           mocked_config_file

  def test__invoke__success(
      self,
      step_install_config_files_instance: StepInstallConfigFile,
      mocked_config_file: str,
      mocked_copy: mock.Mock,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 0

    step_install_config_files_instance.invoke()

    mocked_copy.assert_called_once_with(
        mocked_config_file,
        config.PATH_USER_CONFIG,
    )
    assert mocked_system.mock_calls == \
           [
             mock.call(
               f"chown {config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} "
               f"{config.PATH_USER_CONFIG}"
             ),
             mock.call(f"chmod 600 {config.PATH_USER_CONFIG}"),
           ]
    assert mocked_stream.getvalue() == \
        (
          "test - INFO - Installing the user's configuration file ...\n"
          "test - INFO - Done writing the user's configuration file.\n"
          "test - INFO - Setting permissions on the user's "
          "configuration file ...\n"
          "test - INFO - Executing: 'chown "
          f"{config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} "
          f"{config.PATH_USER_CONFIG}' ...\n"
          "test - INFO - Executing: "
          f"'chmod 600 {config.PATH_USER_CONFIG}' ...\n"
          "test - INFO - Done setting permissions on the user's "
          "configuration file.\n"
        )

  def test__invoke__failure(
      self,
      step_install_config_files_instance: StepInstallConfigFile,
      mocked_config_file: str,
      mocked_copy: mock.Mock,
      mocked_stream: StringIO,
      mocked_system: mock.Mock,
  ) -> None:
    mocked_system.return_value = 127

    with pytest.raises(system_call_step.SystemCallError) as exc:
      step_install_config_files_instance.invoke()

    mocked_copy.assert_called_once_with(
        mocked_config_file,
        config.PATH_USER_CONFIG,
    )
    mocked_system.assert_called_once_with(
        f"chown {config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} "
        f"{config.PATH_USER_CONFIG}"
    )
    assert mocked_stream.getvalue() == \
           (
             "test - INFO - Installing the user's configuration file ...\n"
             "test - INFO - Done writing the user's configuration file.\n"
             "test - INFO - Setting permissions on the user's "
             "configuration file ...\n"
             "test - INFO - Executing: 'chown "
             f"{config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} "
             f"{config.PATH_USER_CONFIG}' ...\n"
             "test - ERROR - Command: 'chown "
             f"{config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} "
             f"{config.PATH_USER_CONFIG}' failed!\n"
           )
    assert str(exc.value) == (
        f"Command: 'chown {config.PI_PORTAL_USER}:{config.PI_PORTAL_USER} "
        f"{config.PATH_USER_CONFIG}' failed!"
    )
