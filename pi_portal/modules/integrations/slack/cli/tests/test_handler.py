"""Test SlackCLICommandHandler class."""

from unittest import TestCase, mock

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.slack.cli import commands, handler


class TestSlackCLI(TestCase):
  """Test the SlackCLICommandHandler class."""

  def setUp(self) -> None:
    self.slack_client = mock.Mock()
    self.cli = handler.SlackCLICommandHandler(bot=self.slack_client)

  @mock_state.patch
  def test_initialize(self) -> None:
    self.assertEqual(self.cli.method_prefix, "command_")
    self.assertEqual(self.cli.slack_bot, self.slack_client)

  def test_handle(self) -> None:
    mock_command = mock.Mock()
    self.cli.handle(mock_command)
    mock_command.assert_called_once_with(self.slack_client)
    mock_command.return_value.invoke.assert_called_once()


class TestSlackCLICommands(TestCase):
  """Test the SlackCLICommandHandler class commands."""

  def setUp(self) -> None:
    self.slack_client = mock.Mock()
    self.mock_handle = mock.Mock()
    self.cli = handler.SlackCLICommandHandler(bot=self.slack_client)
    self.cli.handle = self.mock_handle  # type: ignore[method-assign]

  def test_id_command(self) -> None:
    self.cli.command_id()
    self.mock_handle.assert_called_with(commands.IDCommand)

  def test_arm_command(self) -> None:
    self.cli.command_arm()
    self.mock_handle.assert_called_with(commands.ArmCommand)

  def test_disarm_command(self) -> None:
    self.cli.command_disarm()
    self.mock_handle.assert_called_with(commands.DisarmCommand)

  def test_help_command(self) -> None:
    self.cli.command_help()
    self.mock_handle.assert_called_with(commands.HelpCommand)

  def test_restart_command(self) -> None:
    self.cli.command_restart()
    self.mock_handle.assert_called_with(commands.RestartCommand)

  def test_snapshot_command(self) -> None:
    self.cli.command_snapshot()
    self.mock_handle.assert_called_with(commands.SnapshotCommand)

  def test_status_command(self) -> None:
    self.cli.command_status()
    self.mock_handle.assert_called_with(commands.StatusCommand)

  def test_temp_command(self) -> None:
    self.cli.command_temp()
    self.mock_handle.assert_called_with(commands.TemperatureCommand)

  def test_uptime_command(self) -> None:
    self.cli.command_uptime()
    self.mock_handle.assert_called_with(commands.UptimeCommand)
