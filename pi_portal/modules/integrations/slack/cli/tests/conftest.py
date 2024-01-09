"""Test fixtures for the slack.cli modules tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import handler, notifier


@pytest.fixture()
def mocked_handler() -> mock.Mock:
  return mock.Mock()


@pytest.fixture()
def mocked_slack_bot() -> mock.Mock:
  return mock.Mock()


@pytest.fixture()
def mocked_slack_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_cli_command_handler_instance(
    mocked_handler: mock.Mock,
    mocked_slack_bot: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> handler.SlackCLICommandHandler:
  monkeypatch.setattr(handler.SlackCLICommandHandler, "handle", mocked_handler)
  return handler.SlackCLICommandHandler(mocked_slack_bot)


@pytest.fixture
def cli_command_handler_instance(
    mocked_slack_bot: mock.Mock,
) -> handler.SlackCLICommandHandler:
  return handler.SlackCLICommandHandler(mocked_slack_bot)


@pytest.fixture
def cli_notifier_instance(
    mocked_slack_client: mock.Mock,
) -> notifier.SlackCLINotifier:
  return notifier.SlackCLINotifier(mocked_slack_client)
