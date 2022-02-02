"""Test SlackCLI class."""

from unittest import TestCase, mock

from pi_portal.modules.configuration.tests.fixtures import mock_state
from pi_portal.modules.integrations.slack_cli import commands, slack_cli


class TestGetAvailableCommands(TestCase):
  """Test the get_available_commands function."""

  def test_call(self) -> None:
    registered_commands = [
        'arm',
        'disarm',
        'help',
        'id',
        'restart',
        'snapshot',
        'status',
        'uptime',
    ]
    result = slack_cli.get_available_commands()
    self.assertEqual(result, registered_commands)


class TestSlackCLI(TestCase):
  """Test the SlackCLI class."""

  def setUp(self) -> None:
    self.slack_client = mock.Mock()
    self.cli = slack_cli.SlackCLI(client=self.slack_client)

  @mock_state.patch
  def test_initialize(self) -> None:
    self.assertEqual(self.cli.method_prefix, "command_")
    self.assertEqual(self.cli.slack_client, self.slack_client)

  def test_invoke(self) -> None:
    mock_command = mock.Mock()
    self.cli.invoke(mock_command)
    mock_command.assert_called_once_with(self.slack_client)
    mock_command.return_value.invoke.assert_called_once()


class TestSlackCLICommands(TestCase):
  """Test the SlackCLI class commands."""

  def setUp(self) -> None:
    self.slack_client = mock.Mock()
    self.mock_invoke = mock.Mock()
    self.cli = slack_cli.SlackCLI(client=self.slack_client)
    self.cli.invoke = self.mock_invoke  # type: ignore[assignment]

  def test_id_command(self) -> None:
    self.cli.command_id()
    self.mock_invoke.assert_called_with(commands.IDCommand)

  def test_arm_command(self) -> None:
    self.cli.command_arm()
    self.mock_invoke.assert_called_with(commands.ArmCommand)

  def test_disarm_command(self) -> None:
    self.cli.command_disarm()
    self.mock_invoke.assert_called_with(commands.DisarmCommand)

  def test_help_command(self) -> None:
    self.cli.command_help()
    self.mock_invoke.assert_called_with(commands.HelpCommand)

  def test_restart_command(self) -> None:
    self.cli.command_restart()
    self.mock_invoke.assert_called_with(commands.RestartCommand)

  def test_snapshot_command(self) -> None:
    self.cli.command_snapshot()
    self.mock_invoke.assert_called_with(commands.SnapshotCommand)

  def test_status_command(self) -> None:
    self.cli.command_status()
    self.mock_invoke.assert_called_with(commands.StatusCommand)

  def test_uptime_command(self) -> None:
    self.cli.command_uptime()
    self.mock_invoke.assert_called_with(commands.UptimeCommand)
