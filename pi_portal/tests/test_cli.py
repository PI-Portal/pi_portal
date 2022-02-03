"""Tests for the Click CLI."""

from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner
from .. import cli


@patch(cli.__name__ + ".configuration.state")
@patch(cli.__name__ + ".configuration.LoggingConfiguration")
class TestCLI(TestCase):
  """Test the Click CLI."""

  def setUp(self) -> None:
    self.runner = CliRunner()

  def check_logging(self, m_logger: Mock) -> None:
    m_logger.assert_called_once()

  def check_state(self, m_state: Mock) -> None:
    m_state.State.return_value.load.assert_called_once_with()

  @patch(cli.__name__ + ".integrations.door_monitor")
  def test_monitor(
      self,
      m_monitor: Mock,
      m_logger: Mock,
      m_state: Mock,
  ) -> None:
    command = "monitor"
    self.runner.invoke(cli.cli, command)

    self.check_logging(m_logger)
    self.check_state(m_state)

    m_monitor.DoorMonitor.assert_called_once_with()
    m_monitor.DoorMonitor.return_value.start.assert_called_once_with()
    m_logger.return_value.configure.assert_called_once()
    self.assertEqual(
        m_monitor.DoorMonitor.return_value.log,
        m_logger.return_value.configure.return_value
    )

  @patch(cli.__name__ + ".integrations.slack")
  def test_slack_bot(
      self,
      m_slack: Mock,
      m_logger: Mock,
      m_state: Mock,
  ) -> None:
    command = "slack_bot"
    self.runner.invoke(cli.cli, command)

    self.check_logging(m_logger)
    self.check_state(m_state)

    m_slack.SlackClient.assert_called_once_with()
    m_slack.SlackClient.return_value.subscribe.assert_called_once_with()

  @patch(cli.__name__ + ".integrations.slack")
  def test_upload_snapshot(
      self,
      m_slack: Mock,
      m_logger: Mock,
      m_state: Mock,
  ) -> None:
    mock_snapshot_name = __file__
    command = f"upload_snapshot {mock_snapshot_name}"
    self.runner.invoke(cli.cli, command)

    self.check_logging(m_logger)
    self.check_state(m_state)

    m_slack.SlackClient.assert_called_once_with()
    m_slack.SlackClient.return_value.send_snapshot.assert_called_once_with(
        mock_snapshot_name
    )

  @patch(cli.__name__ + ".integrations.slack")
  def test_upload_video(
      self,
      m_slack: Mock,
      m_logger: Mock,
      m_state: Mock,
  ) -> None:
    mock_video_name = __file__
    command = f"upload_video {mock_video_name}"
    self.runner.invoke(cli.cli, command)

    self.check_logging(m_logger)
    self.check_state(m_state)

    m_slack.SlackClient.assert_called_once_with()
    m_slack.SlackClient.return_value.send_video.assert_called_once_with(
        mock_video_name
    )

  @patch(cli.__name__ + ".system.installer")
  def test_installer(
      self,
      m_installer: Mock,
      m_logger: Mock,
      m_state: Mock,
  ) -> None:
    mock_config_file = __file__
    command = f"installer {mock_config_file}"
    self.runner.invoke(cli.cli, command)

    self.check_logging(m_logger)
    self.check_state(m_state)

    m_installer.installer.assert_called_once_with(mock_config_file)
