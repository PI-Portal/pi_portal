"""CLI command to send a Motion video to Slack and S3."""

from pi_portal.cli_commands.bases import file_command
from pi_portal.cli_commands.mixins import state
from pi_portal.modules.tasks.service_client import TaskSchedulerServiceClient


class UploadVideoCommand(
    file_command.FileCommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to send a Motion video to Slack."""

  def invoke(self) -> None:
    """Invoke the command."""

    service_client = TaskSchedulerServiceClient()
    service_client.chat_upload_video(self.file_name)
