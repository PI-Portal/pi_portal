"""Test the Slack CLI Arm Command."""

from pi_portal.modules.integrations.slack.cli.commands import ArmCommand
from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from ..bases.tests.fixtures import process_management_command_harness


class TestArmCommand(
    process_management_command_harness.ProcessManagementCommandBaseTestHarness
):
  """Test the Slack CLI Arm Command."""

  __test__ = True
  expected_process_name = ProcessList.CAMERA
  expected_process_command: Literal["start"] = "start"

  @classmethod
  def setUpClass(cls) -> None:
    cls.test_class = ArmCommand
