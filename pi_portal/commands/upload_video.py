"""CLI command to send a Motion video to Slack and S3."""

from pi_portal.modules.integrations import slack
from .bases import file_command
from .mixins import state


class UploadVideoCommand(
    file_command.FileCommandBase, state.CommandManagedStateMixin
):
  """CLI command to send a Motion video to Slack and S3."""

  def invoke(self) -> None:
    """Invoke the command."""

    slack_client = slack.SlackClient()
    slack_client.send_video(self.file_name)
