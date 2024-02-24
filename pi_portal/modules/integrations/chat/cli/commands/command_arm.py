"""Chat CLI Arm command."""

from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .bases.process_management_command import ChatProcessManagementCommandBase


class ArmCommand(ChatProcessManagementCommandBase):
  """Chat CLI command to start the camera process."""

  process_name = ProcessList.CAMERA
  process_command: Literal["start"] = "start"
