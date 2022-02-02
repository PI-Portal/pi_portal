"""Test the Slack CLI ID Command."""

from typing import Type

from pi_portal.modules.integrations.slack_cli.commands import command_id
from ..bases.tests.fixtures import command_harness


class TestArmCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI ID Command."""

  __test__ = True

  def get_test_class(self) -> Type[command_id.IDCommand]:
    return command_id.IDCommand

  def test_invoke(self) -> None:
    self.instance.invoke()
    self.mock_slack_client.send_message.assert_called_once_with(
        f"ID: {self.mock_slack_client.config.log_uuid}"
    )
