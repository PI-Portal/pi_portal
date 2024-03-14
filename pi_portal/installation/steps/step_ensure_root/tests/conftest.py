"""Fixtures for the step_ensure_root action classes tests."""
# pylint: disable=redefined-outer-name
import logging
from unittest import mock

import pytest
from .. import action_ensure_root


@pytest.fixture
def mocked_os_geteuid() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def ensure_root_action_instance(
    installer_logger_stdout: logging.Logger,
    mocked_os_geteuid: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> action_ensure_root.EnsureRootAction:
  monkeypatch.setattr(
      action_ensure_root.__name__ + ".os.geteuid", mocked_os_geteuid
  )

  return action_ensure_root.EnsureRootAction(installer_logger_stdout)
