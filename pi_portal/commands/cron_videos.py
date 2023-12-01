"""CLI command to archive all recorded videos."""

from pi_portal.modules.integrations.s3 import video_upload_cron
from .bases import command
from .mixins import state


class CronVideosCommand(
    command.CommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to archive all recorded videos."""

  interval: int = 30

  def invoke(self) -> None:
    """Invoke the command."""

    cron = video_upload_cron.VideoUploadCron(self.interval)
    cron.start()
