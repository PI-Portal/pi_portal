"""Test fixtures for the commands mixins tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import require_task_scheduler, state


@pytest.fixture
def mocked_click() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_file_system() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_state() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def command_managed_state_mixin_instance(
    mocked_state: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> state.CommandManagedStateMixin:
  monkeypatch.setattr(
      state.__name__ + ".state.State",
      mocked_state,
  )
  return state.CommandManagedStateMixin()


@pytest.fixture(name="command_scheduler_mixin_instance")
def command_require_task_scheduler_mixin_instance(
    mocked_click: mock.Mock,
    mocked_file_system: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> require_task_scheduler.CommandTaskSchedulerMixin:
  monkeypatch.setattr(
      require_task_scheduler.__name__ + ".click",
      mocked_click,
  )
  monkeypatch.setattr(
      require_task_scheduler.__name__ + ".file_system.FileSystem",
      mocked_file_system,
  )
  return require_task_scheduler.CommandTaskSchedulerMixin()
