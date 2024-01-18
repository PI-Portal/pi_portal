"""Test fixtures for the commands tests."""
# pylint: disable=redefined-outer-name,duplicate-code

from unittest import mock

import pytest
from .. import task_scheduler


@pytest.fixture
def mocked_uvicorn() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def task_scheduler_command_instance(
    mocked_uvicorn: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> task_scheduler.TaskSchedulerCommand:
  monkeypatch.setattr(
      task_scheduler.__name__ + ".uvicorn",
      mocked_uvicorn,
  )
  return task_scheduler.TaskSchedulerCommand()
