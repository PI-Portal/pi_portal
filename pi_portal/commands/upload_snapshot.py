"""CLI command to send a Motion snapshot to Slack."""

from pi_portal.modules.integrations import slack
from .bases import file_command
from .mixins import state


class UploadSnapshotCommand(
    file_command.FileCommandBase, state.CommandManagedStateMixin
):
  """CLI command to send a Motion snapshot to Slack."""

  def invoke(self) -> None:
    """Invoke the command."""

    slack_client = slack.SlackClient()
    slack_client.send_snapshot(self.file_name)
