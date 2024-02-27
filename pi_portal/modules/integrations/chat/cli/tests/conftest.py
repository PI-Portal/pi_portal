"""Test fixtures for the chat cli modules tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import handler, notifier


@pytest.fixture
def mocked_handler() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_chat_bot() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_task_scheduler_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_cli_command_handler_instance(
    mocked_handler: mock.Mock,
    mocked_chat_bot: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> handler.ChatCLICommandHandler:
  monkeypatch.setattr(handler.ChatCLICommandHandler, "handle", mocked_handler)
  return handler.ChatCLICommandHandler(mocked_chat_bot)


@pytest.fixture
def cli_command_handler_instance(
    mocked_chat_bot: mock.Mock,
) -> handler.ChatCLICommandHandler:
  return handler.ChatCLICommandHandler(mocked_chat_bot)


@pytest.fixture
def cli_notifier_instance(
    mocked_task_scheduler_client: mock.Mock,
) -> notifier.ChatCLINotifier:
  return notifier.ChatCLINotifier(mocked_task_scheduler_client)
