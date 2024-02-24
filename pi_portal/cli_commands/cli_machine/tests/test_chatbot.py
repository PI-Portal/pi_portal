"""Test the ChatBotCommand class."""

from unittest import mock

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.cli_machine import chatbot
from pi_portal.cli_commands.mixins import state


class TestChatBotCommand:
  """Test the ChatBotCommand class."""

  def test_initialize__inheritance(
      self,
      chatbot_command_instance: chatbot.ChatBotCommand,
  ) -> None:
    assert isinstance(chatbot_command_instance, command.CommandBase)
    assert isinstance(chatbot_command_instance, state.CommandManagedStateMixin)

  def test_invoke__calls(
      self,
      chatbot_command_instance: chatbot.ChatBotCommand,
      mocked_chatbot: mock.Mock,
  ) -> None:
    chatbot_command_instance.invoke()

    mocked_chatbot.assert_called_once_with()
    mocked_chatbot.return_value.start.assert_called_once_with()
