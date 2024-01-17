"""Test the StepInstallConfigFile class."""
import logging
from io import StringIO
from unittest import mock

import pytest
from pi_portal import config
from ..bases import base_step
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

  def test__initialize__inheritance(
      self,
      step_install_config_files_instance: StepInstallConfigFile,
  ) -> None:
    assert isinstance(
        step_install_config_files_instance,
        base_step.StepBase,
    )

  def test__invoke__success(
      self,
      step_install_config_files_instance: StepInstallConfigFile,
      mocked_config_file: str,
      mocked_copy: mock.Mock,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    step_install_config_files_instance.invoke()

    mocked_copy.assert_called_once_with(
        mocked_config_file,
        config.PATH_USER_CONFIG,
    )
    assert mocked_file_system.mock_calls == [
        mock.call(config.PATH_USER_CONFIG),
        mock.call().ownership(
            config.PI_PORTAL_USER,
            config.PI_PORTAL_USER,
        ),
        mock.call().permissions("600"),
    ]
    assert mocked_stream.getvalue() == \
        (
          "test - INFO - Installing the user's configuration file ...\n"
          "test - INFO - Done writing the user's configuration file.\n"
          "test - INFO - Setting permissions on the user's "
          "configuration file ...\n"
          "test - INFO - Done setting permissions on the user's "
          "configuration file.\n"
        )

  def test__invoke__failure(
      self,
      step_install_config_files_instance: StepInstallConfigFile,
      mocked_config_file: str,
      mocked_copy: mock.Mock,
      mocked_file_system: mock.Mock,
      mocked_stream: StringIO,
  ) -> None:
    mocked_file_system.return_value.ownership.side_effect = OSError

    with pytest.raises(OSError):
      step_install_config_files_instance.invoke()

    mocked_copy.assert_called_once_with(
        mocked_config_file,
        config.PATH_USER_CONFIG,
    )
    assert mocked_file_system.mock_calls == [
        mock.call(config.PATH_USER_CONFIG),
        mock.call().ownership(
            config.PI_PORTAL_USER,
            config.PI_PORTAL_USER,
        ),
    ]
    assert mocked_stream.getvalue() == (
        "test - INFO - Installing the user's configuration file ...\n"
        "test - INFO - Done writing the user's configuration file.\n"
        "test - INFO - Setting permissions on the user's "
        "configuration file ...\n"
    )
