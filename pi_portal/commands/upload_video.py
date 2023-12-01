"""CLI command to send a Motion video to Slack and S3."""

import os
import shutil

from pi_portal import config
from pi_portal.modules.integrations import slack
from .bases import file_command
from .mixins import state


class UploadVideoCommand(
    file_command.FileCommandBase, state.CommandManagedStateMixin
):
  """CLI command to send a Motion video to Slack."""

  def invoke(self) -> None:
    """Invoke the command."""

    slack_client = slack.SlackClient()
    slack_client.send_file(self.file_name)
    shutil.move(
        self.file_name,
        os.path.join(
            config.VIDEO_UPLOAD_QUEUE_PATH, os.path.basename(self.file_name)
        )
    )
