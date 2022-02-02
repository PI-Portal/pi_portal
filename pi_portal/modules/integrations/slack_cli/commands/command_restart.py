"""Slack CLI Restart command."""

import os

from .bases.command import CommandBase


class RestartCommand(CommandBase):
  """Slack CLI command to restart the Slack Bot process."""

  def invoke(self) -> None:
    """Restart the Slack CLI bot."""

    self.slack_client.send_message("Rebooting myself ...")
    self.slack_client.rtm.close()
    os._exit(1)  # pylint: disable=protected-access
