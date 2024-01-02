"""Test the Slack CLI Help Command."""

from pi_portal.modules.integrations.slack.cli.commands import command_help
from ..bases.tests.fixtures import command_harness


class TestHelpCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI Help Command."""

  __test__ = True

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_help.HelpCommand

  def test_invoke(self) -> None:
    self.mock_slack_bot.command_list = ['a', 'b', 'c']

    self.instance.invoke()

    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        f"Available Commands: {', '.join(self.mock_slack_bot.command_list)}"
    )
