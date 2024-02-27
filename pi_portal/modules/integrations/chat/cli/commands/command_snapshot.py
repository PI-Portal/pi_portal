"""Chat CLI Snapshot command."""

from pi_portal.modules.configuration import state
from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)
from .bases.process_command import ChatProcessCommandBase


class SnapshotCommand(ChatProcessCommandBase):
  """Chat CLI command to take a snapshot with the camera."""

  process_name = ProcessList.CAMERA

  def hook_invoker(self) -> None:
    """Check if the camera is available, and then take a snapshot."""

    if self._is_camera_running():
      self._do_snapshot()
    else:
      self.chatbot.task_scheduler_client.chat_send_message(
          "Please `arm` the camera first ..."
      )

  def _is_camera_running(self) -> bool:
    return self.process.status_in([ProcessStatus.RUNNING])

  def _do_snapshot(self) -> None:
    user_config = state.State().user_config
    for camera_index, _ in enumerate(user_config["MOTION"]["CAMERAS"]):
      self.chatbot.task_scheduler_client.camera_snapshot(camera=camera_index)
