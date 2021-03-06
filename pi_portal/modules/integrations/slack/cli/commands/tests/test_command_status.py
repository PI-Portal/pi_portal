"""Test the Slack CLI Status Command."""

from pi_portal.modules.integrations.slack.cli.commands import command_status
from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)
from ..bases.tests.fixtures import process_status_command_harness


class TestStatusCommand(
    process_status_command_harness.ProcessStatusCommandBaseTestHarness
):
  """Test the Slack CLI Status Command."""

  __test__ = True
  expected_process_name = ProcessList.CAMERA

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = command_status.StatusCommand

  def test_invoke(self) -> None:
    self._mocked_process().status.return_value = ProcessStatus.RUNNING.value
    self.instance.invoke()
    self.mock_slack_bot.slack_client.send_message.assert_called_once_with(
        f"Status: {ProcessStatus.RUNNING.value}"
    )
