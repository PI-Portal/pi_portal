"""Test the Slack CLI Restart Command."""

from typing import Type
from unittest import mock

from pi_portal.modules.integrations.slack_cli.commands import command_restart
from ..bases.tests.fixtures import command_harness


class TestArmCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI Restart Command."""

  __test__ = True

  def get_test_class(self) -> Type[command_restart.RestartCommand]:
    return command_restart.RestartCommand

  @mock.patch(command_restart.__name__ + ".os._exit")
  def test_invoke(self, m_exit: mock.Mock) -> None:
    self.instance.invoke()
    self.mock_slack_client.send_message.assert_called_once_with(
        "Rebooting myself ..."
    )
    self.mock_slack_client.rtm.close.assert_called_once_with()
    m_exit.assert_called_once_with(1)
