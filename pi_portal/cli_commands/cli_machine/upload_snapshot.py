"""CLI command to send a Motion snapshot to Slack."""

from pi_portal.cli_commands.bases import file_command
from pi_portal.cli_commands.mixins import state
from pi_portal.modules.tasks.service_client import TaskSchedulerServiceClient


class UploadSnapshotCommand(
    file_command.FileCommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to send a Motion snapshot to Slack."""

  def invoke(self) -> None:
    """Invoke the command."""

    service_client = TaskSchedulerServiceClient()
    service_client.chat_upload_snapshot(self.file_name)
