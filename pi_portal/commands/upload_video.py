"""CLI command to send a Motion video to Slack and S3."""

from pi_portal.modules.integrations import slack
from .bases import file_command


class UploadVideoCommand(file_command.FileCommandBase):
  """CLI command to send a Motion video to Slack and S3."""

  def invoke(self) -> None:
    """Invoke the command."""

    slack_client = slack.SlackClient()
    slack_client.send_video(self.file_name)
