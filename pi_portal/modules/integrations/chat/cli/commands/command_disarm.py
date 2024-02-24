"""Chat CLI Disarm command."""

from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .bases.process_management_command import ChatProcessManagementCommandBase


class DisarmCommand(ChatProcessManagementCommandBase):
  """Chat CLI command to stop the camera process."""

  process_name = ProcessList.CAMERA
  process_command: Literal["stop"] = "stop"
