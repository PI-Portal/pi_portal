"""Test the Slack CLI Restart Command."""

from unittest import mock

from pi_portal.modules.integrations.slack.cli.commands import command_restart
from ..bases.tests.fixtures import command_harness


class TestRestartCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI Restart Command."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_restart.RestartCommand

  @mock.patch(command_restart.__name__ + ".os._exit")
  def test_invoke(self, m_exit: mock.Mock) -> None:
    self.instance.invoke()
    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        "Rebooting myself ..."
    )
    self.mock_slack_bot.rtm.close.assert_called_once_with()
    m_exit.assert_called_once_with(1)
