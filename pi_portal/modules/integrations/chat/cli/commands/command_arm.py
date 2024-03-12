"""Chat CLI Arm command."""

from pi_portal.modules.integrations.camera.service_client import CameraClient
from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .bases.process_management_command import ChatProcessManagementCommandBase


class ArmCommand(ChatProcessManagementCommandBase):
  """Chat CLI command to start the camera process."""

  process_name = ProcessList.CAMERA
  process_command: Literal["start"] = "start"

  def hook_invoker(self) -> None:
    """Manage the configured process."""

    camera_client = CameraClient(self.chatbot.log)
    if camera_client.is_disk_space_available():
      super().hook_invoker()
    else:
      self.notifier.notify_insufficient_disk_space()
