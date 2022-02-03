"""Test the Slack CLI ID Command."""

from typing import Type
from unittest import mock

from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.slack_cli.commands import command_id
from ..bases.tests.fixtures import command_harness


class TestArmCommand(command_harness.CommandBaseTestHarness):
  """Test the Slack CLI ID Command."""

  __test__ = True

  def get_test_class(self) -> Type[command_id.IDCommand]:
    return command_id.IDCommand

  @mock.patch(state.__name__ + ".State")
  def test_invoke(self, m_state: mock.Mock) -> None:
    self.instance.invoke()
    self.mock_slack_client.send_message.assert_called_once_with(
        f"ID: {m_state.return_value.log_uuid}"
    )
