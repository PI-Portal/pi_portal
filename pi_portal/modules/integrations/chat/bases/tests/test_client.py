"""Tests for the ChatClientBase class."""

import logging
from unittest import mock

from pi_portal import config
from pi_portal.modules.mixins import write_archived_log_file
from ..client import TypeChatClient


class TestChatClientBase:
  """Tests for the ChatBotBase class."""

  def test_initialize__attributes(
      self,
      concrete_chat_client_instance: TypeChatClient,
      mocked_chat_config: mock.Mock,
      mocked_chat_logger: logging.Logger,
  ) -> None:

    assert concrete_chat_client_instance.configuration == mocked_chat_config
    assert concrete_chat_client_instance.logger_name == "client"
    assert concrete_chat_client_instance.log_file_path == (
        config.LOG_FILE_CHAT_CLIENT
    )
    assert concrete_chat_client_instance.log == mocked_chat_logger

  def test_initialize__inheritance(
      self,
      concrete_chat_client_instance: TypeChatClient,
  ) -> None:

    assert isinstance(
        concrete_chat_client_instance,
        write_archived_log_file.ArchivedLogFileWriter
    )

  def test_send_file__calls_mocked_implementation(
      self,
      concrete_chat_client_instance: TypeChatClient,
      mocked_chat_client_implementation: mock.Mock,
  ) -> None:
    concrete_chat_client_instance.send_file("mock_path", "mock_description")

    mocked_chat_client_implementation.send_file.assert_called_once_with(
        "mock_path", "mock_description"
    )

  def test_send_message__calls_mocked_implementation(
      self,
      concrete_chat_client_instance: TypeChatClient,
      mocked_chat_client_implementation: mock.Mock,
  ) -> None:
    concrete_chat_client_instance.send_message("mock_message")

    mocked_chat_client_implementation.send_message.assert_called_once_with(
        "mock_message"
    )
