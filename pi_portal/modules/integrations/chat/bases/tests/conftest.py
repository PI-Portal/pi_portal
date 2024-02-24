"""Test fixtures for the chat integration bases modules tests."""
# pylint: disable=redefined-outer-name

import logging
from typing import Mapping, Type
from unittest import mock

import pytest
from .. import bot, client, config


@pytest.fixture
def mocked_chat_bot_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_chat_client() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_chat_client_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_chat_cli_handler(mocked_command_prefix: str,) -> mock.Mock:
  instance = mock.Mock()
  instance.method_prefix = mocked_command_prefix
  instance.return_value.method_prefix = mocked_command_prefix
  return instance


@pytest.fixture
def mocked_chat_config() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_command_prefix() -> str:
  return "mocked_prefix"


@pytest.fixture
def mocked_get_available_commands() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_user_config() -> Mapping[str, str]:
  return {"mocked": "config"}


@pytest.fixture
def concrete_chat_bot_class(
    mocked_chat_bot_implementation: mock.Mock,
    mocked_chat_client: mock.Mock,
    mocked_chat_config: mock.Mock,
) -> Type[bot.TypeChatBot]:

  class ConcreteBot(bot.ChatBotBase[Mapping[str, str]]):

    def start(self) -> None:
      mocked_chat_bot_implementation.start()

    def halt(self) -> None:
      mocked_chat_bot_implementation.halt()

    def __init__(self) -> None:
      super().__init__()
      self.configuration = mocked_chat_config
      self.chat_client = mocked_chat_client

  return ConcreteBot


@pytest.fixture
def concrete_chat_bot_instance(
    concrete_chat_bot_class: Type[bot.TypeChatBot],
    mocked_chat_cli_handler: mock.Mock,
    mocked_chat_logger: logging.Logger,
    mocked_get_available_commands: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> bot.TypeChatBot:

  monkeypatch.setattr(
      bot.__name__ + ".cli.handler.ChatCLICommandHandler",
      mocked_chat_cli_handler,
  )

  monkeypatch.setattr(
      bot.__name__ + ".cli.get_available_commands",
      mocked_get_available_commands,
  )

  instance = concrete_chat_bot_class()
  instance.log = mocked_chat_logger
  return instance


@pytest.fixture
def concrete_chat_client_class(
    mocked_chat_client_implementation: mock.Mock,
    mocked_chat_config: mock.Mock,
) -> Type[client.TypeChatClient]:

  class ConcreteClient(client.ChatClientBase[Mapping[str, str]]):

    def __init__(self) -> None:
      super().__init__()
      self.configuration = mocked_chat_config

    def send_file(self, file_name: str, description: str) -> None:
      mocked_chat_client_implementation.send_file(file_name, description)

    def send_message(self, message: str) -> None:
      mocked_chat_client_implementation.send_message(message)

  return ConcreteClient


@pytest.fixture
def concrete_chat_client_instance(
    concrete_chat_client_class: Type[client.TypeChatClient],
    mocked_chat_logger: logging.Logger,
) -> client.TypeChatClient:
  instance = concrete_chat_client_class()
  instance.log = mocked_chat_logger
  return instance


@pytest.fixture
def concrete_chat_config_base_instance(
    mocked_user_config: Mapping[str, str]
) -> config.TypeChatConfig:

  class ConcreteConfig(config.ChatConfigurationBase[Mapping[str, str]]):

    def __init__(self) -> None:
      super().__init__()
      self.settings = mocked_user_config
      self.emoji_alert = "mocked_emoji_alert"

  return ConcreteConfig()
