"""Test the Slack CLI Help Command."""

from typing import Type
from unittest import mock

from pi_portal.modules.integrations.slack_cli.commands import command_help
from ..bases.tests.fixtures import command_harness


class TestArmCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI Help Command."""

  __test__ = True

  def get_test_class(self) -> Type[command_help.HelpCommand]:
    return command_help.HelpCommand

  @mock.patch(command_help.__name__ + ".slack_cli.get_available_commands")
  def test_invoke(self, m_get: mock.Mock) -> None:
    m_get.return_value = ['a', 'b', 'c']
    self.instance.invoke()
    self.mock_slack_client.send_message.assert_called_once_with(
        f"Available Commands: {', '.join(m_get.return_value)}"
    )
