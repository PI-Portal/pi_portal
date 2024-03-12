"""Chat CLI Arm command."""

from pi_portal.modules.integrations.camera.service_client import CameraClient
from pi_portal.modules.system.supervisor_config import ProcessList
from pi_portal.modules.system.supervisor_process import (
    SupervisorProcessException,
)
from typing_extensions import Literal
from .bases.process_management_command import ChatProcessManagementCommandBase


class ArmCommand(ChatProcessManagementCommandBase):
  """Chat CLI command to start the camera process."""

  process_name = ProcessList.CAMERA
  process_command: Literal["start"] = "start"

  def hook_invoker(self) -> None:
    """Manage the configured process."""

    self.process.start_condition = lambda: True

    if self.process.is_running():
      raise SupervisorProcessException("Already running.")

    camera_client = CameraClient(self.chatbot.log)

    if camera_client.is_disk_space_available():
      super().hook_invoker()
      self.chatbot.task_scheduler_client.set_flag(
          "FLAG_CAMERA_DISABLED_BY_CRON",
          False,
      )
    else:
      self.notifier.notify_insufficient_disk_space()
