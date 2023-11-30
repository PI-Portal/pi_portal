"""Test fixtures for the slack.cli modules tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.slack import bot


@pytest.fixture()
def mocked_slack_bolt_app() -> mock.Mock:
  return mock.Mock()


@pytest.fixture()
def mocked_slack_bolt_socket_handler() -> mock.Mock:
  return mock.Mock()


@pytest.fixture()
def mocked_slack_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture()
def mocked_logger() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def bot_instance(
    monkeypatch: pytest.MonkeyPatch,
    mocked_logger: mock.Mock,
    mocked_slack_bolt_app: mock.Mock,
    mocked_slack_bolt_socket_handler: mock.Mock,
    mocked_slack_client: mock.Mock,
) -> bot.SlackBot:
  monkeypatch.setattr(bot, "App", mocked_slack_bolt_app)
  monkeypatch.setattr(
      bot, "SocketModeHandler", mocked_slack_bolt_socket_handler
  )
  monkeypatch.setattr(bot.client, "SlackClient", mocked_slack_client)
  with mock_state.mock_state_creator():
    slack_bot = bot.SlackBot()
    slack_bot.log = mocked_logger()
  return slack_bot
