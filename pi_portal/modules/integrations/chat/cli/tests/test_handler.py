"""Test ChatCLICommandHandler class."""

from unittest import mock

from pi_portal.modules.integrations.chat.cli import commands, handler


class TestChatCLICommandHandler:
  """Test the ChatCLICommandHandler class."""

  def test_initialize__attributes(
      self,
      cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_chat_bot: mock.Mock,
  ) -> None:
    assert cli_command_handler_instance.method_prefix == "command_"
    assert cli_command_handler_instance.chatbot == mocked_chat_bot

  def test_handle__mocked_command(
      self,
      cli_command_handler_instance: handler.ChatCLICommandHandler,
  ) -> None:
    mock_command = mock.Mock()

    cli_command_handler_instance.handle(mock_command)

    mock_command.assert_called_once_with(cli_command_handler_instance.chatbot)
    mock_command.return_value.invoke.assert_called_once_with()

  def test_id_command(
      self,
      mocked_cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_handler: mock.Mock,
  ) -> None:
    mocked_cli_command_handler_instance.command_id()

    mocked_handler.assert_called_with(commands.IDCommand)

  def test_arm_command(
      self,
      mocked_cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_handler: mock.Mock,
  ) -> None:
    mocked_cli_command_handler_instance.command_arm()

    mocked_handler.assert_called_with(commands.ArmCommand)

  def test_disarm_command(
      self,
      mocked_cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_handler: mock.Mock,
  ) -> None:
    mocked_cli_command_handler_instance.command_disarm()

    mocked_handler.assert_called_with(commands.DisarmCommand)

  def test_help_command(
      self,
      mocked_cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_handler: mock.Mock,
  ) -> None:
    mocked_cli_command_handler_instance.command_help()

    mocked_handler.assert_called_with(commands.HelpCommand)

  def test_restart_command(
      self,
      mocked_cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_handler: mock.Mock,
  ) -> None:
    mocked_cli_command_handler_instance.command_restart()

    mocked_handler.assert_called_with(commands.RestartCommand)

  def test_snapshot_command(
      self,
      mocked_cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_handler: mock.Mock,
  ) -> None:
    mocked_cli_command_handler_instance.command_snapshot()

    mocked_handler.assert_called_with(commands.SnapshotCommand)

  def test_status_command(
      self,
      mocked_cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_handler: mock.Mock,
  ) -> None:
    mocked_cli_command_handler_instance.command_status()

    mocked_handler.assert_called_with(commands.StatusCommand)

  def test_temp_command(
      self,
      mocked_cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_handler: mock.Mock,
  ) -> None:
    mocked_cli_command_handler_instance.command_temp()

    mocked_handler.assert_called_with(commands.TemperatureCommand)

  def test_uptime_command(
      self,
      mocked_cli_command_handler_instance: handler.ChatCLICommandHandler,
      mocked_handler: mock.Mock,
  ) -> None:
    mocked_cli_command_handler_instance.command_uptime()

    mocked_handler.assert_called_with(commands.UptimeCommand)
