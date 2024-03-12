"""Chat CLI Disarm command."""

from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .bases.process_management_command import ChatProcessManagementCommandBase


class DisarmCommand(ChatProcessManagementCommandBase):
  """Chat CLI command to stop the camera process."""

  process_name = ProcessList.CAMERA
  process_command: Literal["stop"] = "stop"

  def hook_invoker(self) -> None:
    """Manage the configured process."""

    super().hook_invoker()
    self.chatbot.task_scheduler_client.set_flag(
        "FLAG_CAMERA_DISABLED_BY_CRON",
        False,
    )
