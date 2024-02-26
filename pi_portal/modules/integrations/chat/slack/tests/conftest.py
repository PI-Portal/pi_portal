"""Test fixtures for the slack modules tests."""
# pylint: disable=redefined-outer-name

from typing import Callable, List
from unittest import mock

import pytest
from pi_portal.modules.integrations.chat.slack import bot, client, config

TypeSlackClientCreator = Callable[[bool], client.SlackClient]


@pytest.fixture
def mocked_handle_command_method() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_handle_event_method() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_os_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_slack_bolt_app() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_slack_web_client(
    mocked_slack_web_client_instances: List[mock.Mock]
) -> mock.Mock:
  return mock.Mock(side_effect=mocked_slack_web_client_instances)


@pytest.fixture
def mocked_slack_web_client_instances(
    mocked_slack_web_client_chat: mock.Mock,
    mocked_slack_web_client_files: mock.Mock,
) -> List[mock.Mock]:
  return [mocked_slack_web_client_chat, mocked_slack_web_client_files]


@pytest.fixture
def mocked_slack_web_client_chat() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_slack_web_client_files() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_slack_bolt_socket_handler() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_slack_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def slack_bot_instance(
    mocked_chat_logger: mock.Mock,
    mocked_os_module: mock.Mock,
    mocked_slack_bolt_app: mock.Mock,
    mocked_slack_bolt_socket_handler: mock.Mock,
    mocked_slack_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> bot.SlackBot:
  monkeypatch.setattr(
      bot.__name__ + ".os",
      mocked_os_module,
  )
  monkeypatch.setattr(
      bot.__name__ + ".App",
      mocked_slack_bolt_app,
  )
  monkeypatch.setattr(
      bot.__name__ + ".SocketModeHandler",
      mocked_slack_bolt_socket_handler,
  )
  monkeypatch.setattr(
      bot.__name__ + ".SlackClient",
      mocked_slack_client,
  )
  instance = bot.SlackBot()
  instance.log = mocked_chat_logger
  return instance


@pytest.fixture
def slack_bot_instance_mocked_handle_command(
    slack_bot_instance: bot.SlackBot,
    mocked_handle_command_method: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> bot.SlackBot:
  monkeypatch.setattr(
      slack_bot_instance,
      "handle_command",
      mocked_handle_command_method,
  )
  return slack_bot_instance


@pytest.fixture
def slack_bot_instance_mocked_handle_event(
    slack_bot_instance: bot.SlackBot,
    mocked_handle_event_method: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> bot.SlackBot:
  monkeypatch.setattr(
      slack_bot_instance,
      "handle_event",
      mocked_handle_event_method,
  )
  return slack_bot_instance


@pytest.fixture
def slack_client_creator(
    mocked_chat_logger: mock.Mock,
    mocked_slack_web_client: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> TypeSlackClientCreator:

  def create(propagate_exceptions: bool) -> client.SlackClient:
    monkeypatch.setattr(
        client.__name__ + ".WebClient",
        mocked_slack_web_client,
    )
    instance = client.SlackClient(propagate_exceptions=propagate_exceptions)
    instance.log = mocked_chat_logger
    return instance

  return create


@pytest.fixture
def slack_configuration_instance() -> config.SlackIntegrationConfiguration:
  return config.SlackIntegrationConfiguration()
