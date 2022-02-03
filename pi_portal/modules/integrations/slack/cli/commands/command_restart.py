"""Slack CLI Restart command."""

import os

from .bases.command import SlackCommandBase


class RestartCommand(SlackCommandBase):
  """Slack CLI command to restart the Slack Bot process.

  :param client: The configured slack client to use.
  """

  def invoke(self) -> None:
    """Restart the Slack CLI bot."""

    self.slack_client.send_message("Rebooting myself ...")
    self.slack_client.rtm.close()
    os._exit(1)  # pylint: disable=protected-access
