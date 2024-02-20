"""Test the RestartCommand class."""

from unittest import mock

from pi_portal.modules.integrations.slack.cli.commands import RestartCommand
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

    mocked_chat_bot.chat_client.send_message.assert_called_once_with(
        "Rebooting myself ..."
    )

  def test_invoke__closes_chat_bot(
      self,
      restart_command_instance: RestartCommand,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    restart_command_instance.invoke()

    mocked_chat_bot.web_socket.close.assert_called_once_with()

  def test_invoke__terminates_process(
      self,
      restart_command_instance: RestartCommand,
      mocked_os_module: mock.Mock,
  ) -> None:
    restart_command_instance.invoke()

    # pylint: disable=protected-access
    mocked_os_module._exit.assert_called_once_with(1)
