"""Test the ChatCommandBase class."""

from unittest import mock

import pytest
from pi_portal.cli_commands.bases.command import CommandBase
from pi_portal.modules.integrations.chat.cli import notifier
from pi_portal.modules.integrations.chat.cli.commands.bases import command


class TestChatCommandBase:
  """Test the ChatCommandBase class."""

  def test_initialize__inheritance(
      self,
      concrete_command_instance: command.ChatCommandBase,
  ) -> None:
    assert isinstance(
        concrete_command_instance,
        CommandBase,
    )
    assert isinstance(
        concrete_command_instance,
        command.ChatCommandBase,
    )

  def test_initialize__bot(
      self,
      concrete_command_instance: command.ChatCommandBase,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    assert concrete_command_instance.chatbot == mocked_chat_bot

  def test_initialize__notifier(
      self,
      concrete_command_instance: command.ChatCommandBase,
      mocked_chat_client: mock.Mock,
  ) -> None:
    assert isinstance(
        concrete_command_instance.notifier,
        notifier.ChatCLINotifier,
    )
    assert concrete_command_instance.notifier.chat_client == (
        mocked_chat_client
    )

  def test_invoke__raises_exception(
      self,
      concrete_command_instance: command.ChatCommandBase,
  ) -> None:
    with pytest.raises(NotImplementedError):
      concrete_command_instance.invoke()
