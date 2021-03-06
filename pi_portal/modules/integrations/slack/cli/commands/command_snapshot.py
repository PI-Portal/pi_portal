"""Slack CLI Snapshot command."""

from typing import TYPE_CHECKING

from pi_portal.modules.integrations import motion
from pi_portal.modules.system.supervisor_config import (
    ProcessList,
    ProcessStatus,
)
from .bases.process_command import SlackProcessCommandBase

if TYPE_CHECKING:
  from pi_portal.modules.integrations.slack.bot import \
      SlackBot  # pragma: no cover


class SnapshotCommand(SlackProcessCommandBase):
  """Slack CLI command to take a snapshot with the camera.

  :param bot: The configured slack bot in use.
  """

  process_name = ProcessList.CAMERA

  def __init__(self, bot: "SlackBot"):
    super().__init__(bot)
    self.motion_client = motion.Motion()

  def hook_invoker(self) -> None:
    """Check if the camera is available, and then take a snapshot."""

    if self._is_camera_running():
      self._do_snapshot()
    else:
      self.slack_bot.slack_client.send_message(
          "Please `arm` the camera first ..."
      )

  def _is_camera_running(self) -> bool:
    return self.process.status_in([ProcessStatus.RUNNING])

  def _do_snapshot(self) -> None:
    try:
      self.motion_client.take_snapshot()
    except motion.MotionException:
      self.notifier.notify_error()
