"""Tests for the ChatBotBase class."""
import logging
from io import StringIO
from unittest import mock

import pytest
from pi_portal import config
from pi_portal.modules.mixins import write_archived_log_file
from ..bot import TypeChatBot


class TestChatBotBase:
  """Tests for the ChatBotBase class."""

  def test_initialize__attributes(
      self,
      concrete_chat_bot_instance: TypeChatBot,
      mocked_chat_config: mock.Mock,
      mocked_chat_logger: logging.Logger,
  ) -> None:
    assert concrete_chat_bot_instance.configuration == mocked_chat_config
    assert concrete_chat_bot_instance.logger_name == "bot"
    assert concrete_chat_bot_instance.log_file_path == config.LOG_FILE_CHAT_BOT
    assert concrete_chat_bot_instance.log == mocked_chat_logger

  def test_initialize__command_list(
      self,
      concrete_chat_bot_instance: TypeChatBot,
      mocked_get_available_commands: mock.Mock,
  ) -> None:
    assert concrete_chat_bot_instance.command_list == (
        mocked_get_available_commands.return_value
    )

  def test_initialize__task_scheduler_client(
      self,
      concrete_chat_bot_instance: TypeChatBot,
      mocked_task_scheduler: mock.Mock,
  ) -> None:
    assert concrete_chat_bot_instance.task_scheduler_client == (
        mocked_task_scheduler.return_value
    )
    mocked_task_scheduler.assert_called_once_with()

  def test_initialize__inheritance(
      self,
      concrete_chat_bot_instance: TypeChatBot,
  ) -> None:
    assert isinstance(
        concrete_chat_bot_instance,
        write_archived_log_file.ArchivedLogFileWriter
    )

  def test_halt__calls_mocked_implementation(
      self,
      concrete_chat_bot_instance: TypeChatBot,
      mocked_chat_bot_implementation: mock.Mock,
  ) -> None:
    concrete_chat_bot_instance.halt()

    mocked_chat_bot_implementation.halt.assert_called_once_with()

  def test_start__calls_mocked_implementation(
      self,
      concrete_chat_bot_instance: TypeChatBot,
      mocked_chat_bot_implementation: mock.Mock,
  ) -> None:
    concrete_chat_bot_instance.start()

    mocked_chat_bot_implementation.start.assert_called_once_with()

  @pytest.mark.parametrize("valid_command", ["id", "help"])
  def test_handle__vary_command__command_is_valid__calls_handler_method(
      self,
      concrete_chat_bot_instance: TypeChatBot,
      mocked_chat_cli_handler: mock.Mock,
      mocked_command_prefix: str,
      valid_command: str,
  ) -> None:
    concrete_chat_bot_instance.command_list = [valid_command]
    expected_mocked_method = getattr(
        mocked_chat_cli_handler.return_value,
        mocked_command_prefix + valid_command
    )

    concrete_chat_bot_instance.handle_command(valid_command)

    mocked_chat_cli_handler.assert_called_once_with(
        bot=concrete_chat_bot_instance
    )
    expected_mocked_method.assert_called_once_with()

  @pytest.mark.parametrize("valid_command", ["id", "help"])
  def test_handle__vary_command__command_is_valid__logging(
      self,
      concrete_chat_bot_instance: TypeChatBot,
      mocked_stream: StringIO,
      valid_command: str,
  ) -> None:
    concrete_chat_bot_instance.command_list = [valid_command]
    concrete_chat_bot_instance.handle_command(valid_command)

    assert mocked_stream.getvalue() == (
        f"DEBUG - None - Received command: '{valid_command}'\n"
        f"INFO - None - Executing valid command: '{valid_command}'\n"
    )

  @pytest.mark.parametrize("invalid_command", ["id", "help"])
  def test_handle__invalid_command__does_not_call_handler_method(
      self,
      concrete_chat_bot_instance: TypeChatBot,
      mocked_chat_cli_handler: mock.Mock,
      mocked_command_prefix: str,
      invalid_command: str,
  ) -> None:
    concrete_chat_bot_instance.command_list = []
    expected_mocked_method = getattr(
        mocked_chat_cli_handler.return_value,
        mocked_command_prefix + invalid_command
    )

    concrete_chat_bot_instance.handle_command(invalid_command)

    mocked_chat_cli_handler.assert_not_called()
    expected_mocked_method.assert_not_called()

  @pytest.mark.parametrize("invalid_command", ["id", "help"])
  def test_handle__invalid_command__logging(
      self,
      concrete_chat_bot_instance: TypeChatBot,
      mocked_stream: StringIO,
      invalid_command: str,
  ) -> None:
    concrete_chat_bot_instance.command_list = []

    concrete_chat_bot_instance.handle_command(invalid_command)

    assert mocked_stream.getvalue() == \
        f"DEBUG - None - Received command: '{invalid_command}'\n"
