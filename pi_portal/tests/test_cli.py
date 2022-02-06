"""Tests for the Click CLI."""

from unittest import TestCase
from unittest.mock import Mock, patch

from click.testing import CliRunner
from .. import cli


@patch(cli.__name__ + ".configuration.state")
class TestCLI(TestCase):
  """Test the Click CLI."""

  def setUp(self) -> None:
    self.runner = CliRunner()

  def check_state(self, m_state: Mock) -> None:
    m_state.State.return_value.load.assert_called_once_with()

  @patch(cli.__name__ + ".integrations.gpio")
  def test_monitor(
      self,
      m_factory: Mock,
      m_state: Mock,
  ) -> None:
    command = "monitor"
    self.runner.invoke(cli.cli, command)

    self.check_state(m_state)

    m_factory_instance = m_factory.DoorMonitorFactory.return_value
    m_monitor_instance = m_factory_instance.create.return_value

    m_factory.DoorMonitorFactory.assert_called_once_with()
    m_factory_instance.create.assert_called_once_with()
    m_monitor_instance.start.assert_called_once_with()

  @patch(cli.__name__ + ".integrations.slack")
  def test_slack_bot(
      self,
      m_slack: Mock,
      m_state: Mock,
  ) -> None:
    command = "slack_bot"
    self.runner.invoke(cli.cli, command)

    self.check_state(m_state)

    m_slack.SlackBot.assert_called_once_with()
    m_slack.SlackBot.return_value.connect.assert_called_once_with()

  @patch(cli.__name__ + ".integrations.slack")
  def test_upload_snapshot(
      self,
      m_slack: Mock,
      m_state: Mock,
  ) -> None:
    mock_snapshot_name = __file__
    command = f"upload_snapshot {mock_snapshot_name}"
    self.runner.invoke(cli.cli, command)

    self.check_state(m_state)

    m_slack.SlackClient.assert_called_once_with()
    m_slack.SlackClient.return_value.send_snapshot.assert_called_once_with(
        mock_snapshot_name
    )

  @patch(cli.__name__ + ".integrations.slack")
  def test_upload_video(
      self,
      m_slack: Mock,
      m_state: Mock,
  ) -> None:
    mock_video_name = __file__
    command = f"upload_video {mock_video_name}"
    self.runner.invoke(cli.cli, command)

    self.check_state(m_state)

    m_slack.SlackClient.assert_called_once_with()
    m_slack.SlackClient.return_value.send_video.assert_called_once_with(
        mock_video_name
    )

  @patch(cli.__name__ + ".system.installer")
  def test_installer(
      self,
      m_installer: Mock,
      m_state: Mock,
  ) -> None:
    mock_config_file = __file__
    command = f"installer {mock_config_file}"
    self.runner.invoke(cli.cli, command)

    self.check_state(m_state)

    m_installer.installer.assert_called_once_with(mock_config_file)
