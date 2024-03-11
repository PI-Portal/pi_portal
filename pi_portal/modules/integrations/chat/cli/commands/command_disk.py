"""Chat CLI Disk command."""

import shutil

from pi_portal import config
from pi_portal.modules.configuration import state
from .bases.command import ChatCommandBase


class DiskCommand(ChatCommandBase):
  """Chat CLI command to report the free space for camera storage."""

  def invoke(self) -> None:
    """Send the unique id for this bot's instance."""

    running_state = state.State()
    free_space = shutil.disk_usage(config.PATH_CAMERA_CONTENT).free / 1000000
    threshold_value = (
        running_state.user_config["CAMERA"]["DISK_SPACE_MONITOR"]["THRESHOLD"]
    )

    self.chatbot.task_scheduler_client.chat_send_message(
        f"Free space for camera storage: {free_space:.2f} MB.\n"
        f"Minimum required for camera operation is: {threshold_value:.2f} MB."
    )
