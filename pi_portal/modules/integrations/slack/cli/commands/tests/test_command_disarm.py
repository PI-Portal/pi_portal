"""Test the Slack CLI Disarm Command."""

from pi_portal.modules.integrations.slack.cli.commands import DisarmCommand
from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from ..bases.tests.fixtures import process_management_command_harness


class TestDisarmCommand(
    process_management_command_harness.ProcessManagementCommandBaseTestHarness
):
  """Test the Slack CLI Disarm Command."""

  __test__ = True
  expected_process_name = ProcessList.CAMERA
  expected_process_command: Literal["stop"] = "stop"

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = DisarmCommand
