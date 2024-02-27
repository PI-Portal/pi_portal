"""Test fixtures for the chat CLI commands modules tests."""
# pylint: disable=redefined-outer-name

from typing import Callable
from unittest import mock

import pytest
from .bases import command, process_command


@pytest.fixture
def mocked_cli_notifier() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_chat_bot(mocked_task_scheduler_client: mock.Mock) -> mock.Mock:
  instance = mock.Mock()
  instance.task_scheduler_client = mocked_task_scheduler_client
  return instance


@pytest.fixture
def mocked_task_scheduler_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_process_invoker() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_supervisor_process() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def setup_process_command_mocks(
    monkeypatch: pytest.MonkeyPatch,
    mocked_cli_notifier: mock.Mock,
    mocked_supervisor_process: mock.Mock,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        command.__name__ + ".ChatCLINotifier",
        mocked_cli_notifier,
    )
    monkeypatch.setattr(
        process_command.__name__ + ".SupervisorProcess",
        mocked_supervisor_process,
    )

  return setup
