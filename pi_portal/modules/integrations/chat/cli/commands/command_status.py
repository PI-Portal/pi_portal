"""Chat CLI Status command."""

from pi_portal.modules.system.supervisor_config import ProcessList
from typing_extensions import Literal
from .bases.process_status_command import ChatProcessStatusCommandBase


class StatusCommand(ChatProcessStatusCommandBase):
  """Chat CLI command to report the status of the camera."""

  process_name = ProcessList.CAMERA
  process_command: Literal["status"] = "status"

  def hook_invoker(self) -> None:
    """Report if the camera is running or not."""

    super().hook_invoker()
    self.chatbot.task_scheduler_client.chat_send_message(
        f"Status: {self.result}"
    )
