"""Tests for the Click CLI."""

from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner
from .. import cli


@patch(cli.__name__ + ".state")
class TestCLI(TestCase):
  """Test the Click CLI."""

  def setUp(self) -> None:
    self.runner = CliRunner()

  def check_state(self, m_state: Mock) -> None:
    m_state.State.return_value.load.assert_called_once_with()

  def check_invoke(self, m_command: Mock) -> None:
    m_command.assert_called_once_with()
    m_command.return_value.invoke.assert_called_once_with()

  def check_invoke_with_file(self, m_command: Mock, file: str) -> None:
    m_command.assert_called_once_with(file)
    m_command.return_value.invoke.assert_called_once_with()

  @patch(cli.__name__ + ".door_monitor")
  def test_monitor(
      self,
      m_command: Mock,
      m_state: Mock,
  ) -> None:
    command = "monitor"
    self.runner.invoke(cli.cli, command)
    self.check_state(m_state)
    self.check_invoke(m_command.DoorMonitorCommand)

  @patch(cli.__name__ + ".slack_bot")
  def test_slack_bot(
      self,
      m_command: Mock,
      m_state: Mock,
  ) -> None:
    command = "slack_bot"
    self.runner.invoke(cli.cli, command)
    self.check_state(m_state)
    self.check_invoke(m_command.SlackBotCommand)

  @patch(cli.__name__ + ".upload_snapshot")
  def test_upload_snapshot(
      self,
      m_command: Mock,
      m_state: Mock,
  ) -> None:
    mock_snapshot_name = __file__
    command = f"upload_snapshot {mock_snapshot_name}"
    self.runner.invoke(cli.cli, command)
    self.check_state(m_state)
    self.check_invoke_with_file(
        m_command.UploadSnapshotCommand, mock_snapshot_name
    )

  @patch(cli.__name__ + ".upload_video")
  def test_upload_video(
      self,
      m_command: Mock,
      m_state: Mock,
  ) -> None:
    mock_video_name = __file__
    command = f"upload_video {mock_video_name}"
    self.runner.invoke(cli.cli, command)
    self.check_state(m_state)
    self.check_invoke_with_file(m_command.UploadVideoCommand, mock_video_name)

  @patch(cli.__name__ + ".installer")
  def test_installer(
      self,
      m_command: Mock,
      m_state: Mock,
  ) -> None:
    mock_config_file = __file__
    command = f"installer {mock_config_file}"
    self.runner.invoke(cli.cli, command)
    self.check_state(m_state)
    self.check_invoke_with_file(m_command.InstallerCommand, mock_config_file)
