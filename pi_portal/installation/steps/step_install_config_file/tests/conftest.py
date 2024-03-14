"""Fixtures for the step_install_config_file action classes tests."""
# pylint: disable=redefined-outer-name
import logging
from unittest import mock

import pytest
from .. import action_copy_config_file


@pytest.fixture
def mocked_file_system() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_shutil_copy() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def copy_config_file_action_instance(
    installer_logger_stdout: logging.Logger,
    mocked_file_system: mock.Mock,
    mocked_shutil_copy: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> action_copy_config_file.CopyPiPortalUserConfigAction:
  monkeypatch.setattr(
      action_copy_config_file.__name__ + ".file_system.FileSystem",
      mocked_file_system
  )
  monkeypatch.setattr(
      action_copy_config_file.__name__ + ".shutil.copy", mocked_shutil_copy
  )

  return action_copy_config_file.CopyPiPortalUserConfigAction(
      installer_logger_stdout
  )
