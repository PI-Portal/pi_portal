"""CLI command to send a Motion snapshot to Slack."""

from pi_portal.modules.integrations import slack
from .bases import file_command


class UploadSnapshotCommand(file_command.FileCommandBase):
  """CLI command to send a Motion snapshot to Slack."""

  def invoke(self) -> None:
    """Invoke the command."""

    slack_client = slack.SlackClient()
    slack_client.send_snapshot(self.file_name)
