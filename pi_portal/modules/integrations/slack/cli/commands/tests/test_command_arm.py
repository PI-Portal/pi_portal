"""Test the ArmCommand class."""

from pi_portal.modules.integrations.slack.cli.commands import ArmCommand
from pi_portal.modules.system.supervisor_config import ProcessList
from ..bases import process_management_command


class TestArmCommand:
  """Test the ArmCommand class."""

  def test_initialize__attributes(
      self,
      arm_command_instance: ArmCommand,
  ) -> None:
    assert arm_command_instance.process_name == ProcessList.CAMERA
    assert arm_command_instance.process_command == "start"

  def test_initialize__inheritance(
      self,
      arm_command_instance: ArmCommand,
  ) -> None:
    assert isinstance(
        arm_command_instance,
        process_management_command.ChatProcessManagementCommandBase,
    )
