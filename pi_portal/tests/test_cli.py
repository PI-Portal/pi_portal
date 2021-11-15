"""Tests for the Click CLI."""

from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner
from .. import cli


class TestCLI(TestCase):
  """Test the Click CLI."""

  def setUp(self):
    self.runner = CliRunner()

  @patch(cli.__name__ + ".modules.monitor")
  def test_monitor(self, m_monitor):
    command = "monitor"
    self.runner.invoke(cli.cli, command)
    m_monitor.Monitor.assert_called_once_with()
    m_monitor.Monitor.return_value.start.assert_called_once_with()

  @patch(cli.__name__ + ".modules.slack")
  def test_slack_bot(self, m_slack):
    command = "slack_bot"
    self.runner.invoke(cli.cli, command)
    m_slack.Client.assert_called_once_with()
    m_slack.Client.return_value.subscribe.assert_called_once_with()

  @patch(cli.__name__ + ".modules.slack")
  def test_upload_video(self, m_slack):
    mock_video_name = __file__
    command = f"upload_video {mock_video_name}"
    self.runner.invoke(cli.cli, command)
    m_slack.Client.assert_called_once_with()
    m_slack.Client.return_value.send_video.assert_called_once_with(
        mock_video_name
    )

  @patch(cli.__name__ + ".modules.installer")
  def test_installer(self, m_installer):
    mock_config_file = __file__
    command = f"installer {mock_config_file}"
    self.runner.invoke(cli.cli, command)
    m_installer.installer.assert_called_once_with(mock_config_file)
