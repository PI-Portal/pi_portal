"""Tests for the Click CLI."""

from typing import List, Tuple
from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner
from .. import cli


class TestCLI(TestCase):
  """Test the Click CLI."""

  def setUp(self) -> None:
    self.runner = CliRunner()

  def check_state(self, m_command: Mock, debug: bool) -> None:
    m_command.return_value.load_state.assert_called_once_with(debug=debug)
    m_command.return_value.load_state.reset_mock()

  def check_no_state(self, m_command: Mock) -> None:
    m_command.return_value.load_state.assert_not_called()

  def check_invoke(self, m_command: Mock) -> None:
    m_command.assert_called_once_with()
    m_command.return_value.invoke.assert_called_once_with()
    m_command.return_value.invoke.reset_mock()
    m_command.reset_mock()

  def check_invoke_with_file(self, m_command: Mock, file: str) -> None:
    m_command.assert_called_once_with(file)
    m_command.return_value.invoke.assert_called_once_with()
    m_command.return_value.invoke.reset_mock()
    m_command.reset_mock()

  def get_debug_subtests(self, command: str) -> List[Tuple[str, bool]]:
    return [(command, False), ("--debug " + command, True)]

  @patch(cli.__name__ + ".door_monitor")
  def test_monitor(
      self,
      m_command: Mock,
  ) -> None:
    for command, debug in self.get_debug_subtests("monitor"):
      self.runner.invoke(cli.cli, command)
      self.check_state(m_command.DoorMonitorCommand, debug)
      self.check_invoke(m_command.DoorMonitorCommand)

  @patch(cli.__name__ + ".slack_bot")
  def test_slack_bot(
      self,
      m_command: Mock,
  ) -> None:
    for command, debug in self.get_debug_subtests("slack_bot"):
      self.runner.invoke(cli.cli, command)
      self.check_state(m_command.SlackBotCommand, debug)
      self.check_invoke(m_command.SlackBotCommand)

  @patch(cli.__name__ + ".upload_snapshot")
  def test_upload_snapshot(
      self,
      m_command: Mock,
  ) -> None:
    mock_snapshot_name = __file__
    for command, debug in self.get_debug_subtests(
        f"upload_snapshot {mock_snapshot_name}"
    ):
      self.runner.invoke(cli.cli, command)
      self.check_state(m_command.UploadSnapshotCommand, debug)
      self.check_invoke_with_file(
          m_command.UploadSnapshotCommand, mock_snapshot_name
      )

  @patch(cli.__name__ + ".upload_video")
  def test_upload_video(
      self,
      m_command: Mock,
  ) -> None:
    mock_video_name = __file__
    for command, debug in self.get_debug_subtests(
        f"upload_video {mock_video_name}"
    ):
      self.runner.invoke(cli.cli, command)
      self.check_state(m_command.UploadVideoCommand, debug)
      self.check_invoke_with_file(m_command.UploadVideoCommand, mock_video_name)

  @patch(cli.__name__ + ".installer")
  def test_installer(
      self,
      m_command: Mock,
  ) -> None:
    mock_config_file = __file__
    command = f"installer {mock_config_file}"
    self.runner.invoke(cli.cli, command)
    self.check_no_state(m_command.InstallerCommand)
    self.check_invoke_with_file(m_command.InstallerCommand, mock_config_file)

  @patch(cli.__name__ + ".version")
  def test_version(
      self,
      m_command: Mock,
  ) -> None:
    command = "version"
    self.runner.invoke(cli.cli, command)
    self.check_no_state(m_command.VersionCommand)
    self.check_invoke(m_command.VersionCommand)
