"""Test the RestartCommand class."""

from unittest import mock

from pi_portal.modules.integrations.chat.cli.commands import RestartCommand
from ..bases import command


class TestRestartCommand:
  """Test the RestartCommand class."""

  def test_initialize__inheritance(
      self,
      restart_command_instance: RestartCommand,
  ) -> None:
    assert isinstance(
        restart_command_instance,
        command.ChatCommandBase,
    )

  def test_invoke__sends_correct_message(
      self,
      restart_command_instance: RestartCommand,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    restart_command_instance.invoke()

    mocked_chat_bot.task_scheduler_client.\
        chat_send_message.assert_called_once_with(
          "Rebooting myself ..."
        )

  def test_invoke__halts_chat_bot(
      self,
      restart_command_instance: RestartCommand,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    restart_command_instance.invoke()

    mocked_chat_bot.halt.assert_called_once_with()
