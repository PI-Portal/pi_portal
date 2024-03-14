"""Test the CopyPiPortalUserConfigAction class."""
from io import StringIO
from shutil import SameFileError
from typing import Optional
from unittest import mock

import pytest
from pi_portal import config
from ..action_copy_config_file import CopyPiPortalUserConfigAction


class TestCopyPiPortalUserConfigAction:
  """Test the CopyPiPortalUserConfigAction class."""

  def test_initialize__attributes(
      self,
      copy_config_file_action_instance: CopyPiPortalUserConfigAction,
  ) -> None:
    assert not hasattr(copy_config_file_action_instance, "config_file_path")

  def test_invoke__without_config_file__raises_attribute_error(
      self,
      copy_config_file_action_instance: CopyPiPortalUserConfigAction,
  ) -> None:
    with pytest.raises(AttributeError):
      copy_config_file_action_instance.invoke()

  @pytest.mark.parametrize("optional_exception", [None, SameFileError])
  def test_invoke__with_config_file__calls_shutil_copy(
      self,
      copy_config_file_action_instance: CopyPiPortalUserConfigAction,
      mocked_shutil_copy: mock.Mock,
      optional_exception: Optional[Exception],
  ) -> None:
    mocked_config_file_path = "/path/to/config_file.json"
    copy_config_file_action_instance.config_file_path = (
        mocked_config_file_path
    )
    mocked_shutil_copy.side_effect = optional_exception

    copy_config_file_action_instance.invoke()

    mocked_shutil_copy.assert_called_once_with(
        mocked_config_file_path, config.PATH_USER_CONFIG
    )

  @pytest.mark.parametrize("optional_exception", [None, SameFileError])
  def test_invoke__with_config_file__calls_file_system(
      self,
      copy_config_file_action_instance: CopyPiPortalUserConfigAction,
      mocked_file_system: mock.Mock,
      mocked_shutil_copy: mock.Mock,
      optional_exception: Optional[Exception],
  ) -> None:
    mocked_config_file_path = "/path/to/config_file.json"
    copy_config_file_action_instance.config_file_path = (
        mocked_config_file_path
    )
    mocked_shutil_copy.side_effect = optional_exception

    copy_config_file_action_instance.invoke()

    assert mocked_file_system.mock_calls == [
        mock.call(config.PATH_USER_CONFIG),
        mock.call().ownership(
            config.PI_PORTAL_USER,
            config.PI_PORTAL_USER,
        ),
        mock.call().permissions("600"),
    ]

  @pytest.mark.parametrize("optional_exception", [None, SameFileError])
  def test_invoke__with_config_file__logging(
      self,
      copy_config_file_action_instance: CopyPiPortalUserConfigAction,
      mocked_shutil_copy: mock.Mock,
      mocked_stream: StringIO,
      optional_exception: Optional[Exception],
  ) -> None:
    mocked_config_file_path = "/path/to/config_file.json"
    copy_config_file_action_instance.config_file_path = (
        mocked_config_file_path
    )
    mocked_shutil_copy.side_effect = optional_exception

    copy_config_file_action_instance.invoke()

    assert mocked_stream.getvalue() == (
        "INFO - Setting permissions on the user's configuration file ...\n"
        "INFO - Done setting permissions on the user's configuration file.\n"
    )
