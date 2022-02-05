"""Slack CLI Restart command."""

import os

from .bases.command import SlackCommandBase


class RestartCommand(SlackCommandBase):
  """Slack CLI command to restart the Slack Bot process.

  :param bot: The configured slack bot in use.
  """

  def invoke(self) -> None:
    """Restart the Slack CLI bot."""

    self.slack_bot.slack_client.send_message("Rebooting myself ...")
    self.slack_bot.rtm.close()
    os._exit(1)  # pylint: disable=protected-access
