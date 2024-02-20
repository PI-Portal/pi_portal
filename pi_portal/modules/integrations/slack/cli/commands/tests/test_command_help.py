"""Test the HelpCommand class."""

from unittest import mock

from pi_portal.modules.integrations.slack.cli.commands import HelpCommand
from ..bases import command


class TestHelpCommand:
  """Test the HelpCommand class."""

  def test_initialize__inheritance(
      self,
      help_command_instance: HelpCommand,
  ) -> None:
    assert isinstance(
        help_command_instance,
        command.ChatCommandBase,
    )

  def test_invoke__sends_correct_message(
      self,
      help_command_instance: HelpCommand,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    mocked_chat_bot.command_list = ['a', 'b', 'c']

    help_command_instance.invoke()

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        f"Available Commands: {', '.join(mocked_chat_bot.command_list)}"
    )
