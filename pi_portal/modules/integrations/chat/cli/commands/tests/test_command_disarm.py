"""Test the DisarmCommand class."""

from pi_portal.modules.integrations.chat.cli.commands import DisarmCommand
from pi_portal.modules.system.supervisor_config import ProcessList
from ..bases import process_management_command


class TestDisarmCommand:
  """Test the DisarmCommand class."""

  def test_initialize__attributes(
      self,
      disarm_command_instance: DisarmCommand,
  ) -> None:
    assert disarm_command_instance.process_name == ProcessList.CAMERA
    assert disarm_command_instance.process_command == "stop"

  def test_initialize__inheritance(
      self,
      disarm_command_instance: DisarmCommand,
  ) -> None:
    assert isinstance(
        disarm_command_instance,
        process_management_command.ChatProcessManagementCommandBase,
    )
