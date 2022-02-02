"""Slack CLI Snapshot command."""

from typing import TYPE_CHECKING

from pi_portal.modules.integrations import motion
from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)
from .bases.process_command import ProcessCommandBase

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack import Client  # pragma: no cover


class SnapshotCommand(ProcessCommandBase):
  """Slack CLI command to take a snapshot with the camera.

  :param client: The configured slack client to use.
  """

  process_name = ProcessList.CAMERA

  def __init__(self, client: "Client"):
    super().__init__(client)
    self.motion_client = motion.Motion()

  def hook_invoker(self) -> None:
    """Check if the camera is available, and then take a snapshot."""

    if self._is_camera_running():
      self._do_snapshot()
    else:
      self.slack_client.send_message("Please `arm` the camera first ...")

  def _is_camera_running(self) -> bool:
    return self.process.status_in([ProcessStatus.RUNNING])

  def _do_snapshot(self) -> None:
    try:
      self.motion_client.take_snapshot()
    except motion.MotionException:
      self.notifier.notify_error()
