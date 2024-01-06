"""Tests for the Click CLI."""

from typing import Any, List, Optional, Tuple
from unittest.mock import Mock, patch

from click.testing import CliRunner
from .. import cli


class TestCLI:
  """Test the Click CLI."""

  def check_state(
      self,
      m_command: Mock,
      debug: bool,
      file_path: Optional[str] = None
  ) -> None:
    if file_path is None:
      m_command.return_value.load_state.assert_called_once_with(debug=debug)
    else:
      m_command.return_value.load_state.assert_called_once_with(
          debug=debug,
          file_path=file_path,
      )
    m_command.return_value.load_state.reset_mock()

  def check_no_state(self, m_command: Mock) -> None:
    m_command.return_value.load_state.assert_not_called()

  def check_invoke(self, m_command: Mock) -> None:
    m_command.assert_called_once_with()
    m_command.return_value.invoke.assert_called_once_with()
    m_command.return_value.invoke.reset_mock()
    m_command.reset_mock()

  def check_invoke_variable(self, m_command: Mock, args: List[Any]) -> None:
    m_command.assert_called_once_with(*args)
    m_command.return_value.invoke.assert_called_once_with()
    m_command.return_value.invoke.reset_mock()
    m_command.reset_mock()

  def get_debug_subtests(self, command: str) -> List[Tuple[str, bool]]:
    return [(command, False), ("--debug " + command, True)]

  @patch(cli.__name__ + ".cron_videos")
  def test_cron_videos__invoke(
      self,
      m_command: Mock,
      cli_runner: CliRunner,
  ) -> None:
    for command, debug in self.get_debug_subtests("cron_videos"):

      cli_runner.invoke(cli.cli, command)

      self.check_state(m_command.CronVideosCommand, debug)
      self.check_invoke(m_command.CronVideosCommand)

  @patch(cli.__name__ + ".door_monitor")
  def test_door_monitor__invoke(
      self,
      m_command: Mock,
      cli_runner: CliRunner,
  ) -> None:
    for command, debug in self.get_debug_subtests("door_monitor"):

      cli_runner.invoke(cli.cli, command)

      self.check_state(m_command.DoorMonitorCommand, debug)
      self.check_invoke(m_command.DoorMonitorCommand)

  @patch(cli.__name__ + ".installer")
  def test_installer__invoke(
      self,
      m_command: Mock,
      cli_runner: CliRunner,
  ) -> None:
    mock_config_file = __file__
    for flag, confirmation in [("", False), ("-y", True)]:
      for command, debug in self.get_debug_subtests(
          f"install_config {flag} {mock_config_file}"
      ):

        cli_runner.invoke(cli.cli, command)

        self.check_state(
            m_command.InstallerCommand, debug, file_path=mock_config_file
        )
        self.check_invoke_variable(
            m_command.InstallerCommand,
            [mock_config_file, confirmation],
        )

  @patch(cli.__name__ + ".slack_bot")
  def test_slack_bot__invoke(
      self,
      m_command: Mock,
      cli_runner: CliRunner,
  ) -> None:
    for command, debug in self.get_debug_subtests("slack_bot"):

      cli_runner.invoke(cli.cli, command)

      self.check_state(m_command.SlackBotCommand, debug)
      self.check_invoke(m_command.SlackBotCommand)

  @patch(cli.__name__ + ".temperature_monitor")
  def test_temp_monitor__invoke(
      self,
      m_command: Mock,
      cli_runner: CliRunner,
  ) -> None:
    for command, debug in self.get_debug_subtests("temp_monitor"):

      cli_runner.invoke(cli.cli, command)

      self.check_state(m_command.TemperatureMonitorCommand, debug)
      self.check_invoke(m_command.TemperatureMonitorCommand)

  @patch(cli.__name__ + ".upload_snapshot")
  def test_upload_snapshot__invoke(
      self,
      m_command: Mock,
      cli_runner: CliRunner,
  ) -> None:
    mock_snapshot_name = __file__
    for command, debug in self.get_debug_subtests(
        f"upload_snapshot {mock_snapshot_name}"
    ):

      cli_runner.invoke(cli.cli, command)

      self.check_state(m_command.UploadSnapshotCommand, debug)
      self.check_invoke_variable(
          m_command.UploadSnapshotCommand,
          [mock_snapshot_name],
      )

  @patch(cli.__name__ + ".upload_video")
  def test_upload_video__invoke(
      self,
      m_command: Mock,
      cli_runner: CliRunner,
  ) -> None:
    mock_video_name = __file__
    for command, debug in self.get_debug_subtests(
        f"upload_video {mock_video_name}"
    ):

      cli_runner.invoke(cli.cli, command)

      self.check_state(m_command.UploadVideoCommand, debug)
      self.check_invoke_variable(
          m_command.UploadVideoCommand,
          [mock_video_name],
      )

  @patch(cli.__name__ + ".version")
  def test_version__invoke(
      self,
      m_command: Mock,
      cli_runner: CliRunner,
  ) -> None:
    command = "version"

    cli_runner.invoke(cli.cli, command)

    self.check_no_state(m_command.VersionCommand)
    self.check_invoke(m_command.VersionCommand)
