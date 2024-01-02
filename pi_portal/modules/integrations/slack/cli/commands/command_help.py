"""Slack CLI Help command."""

from .bases.command import SlackCommandBase


class HelpCommand(SlackCommandBase):
  """Slack CLI command to list the available commands.

  :param bot: The configured slack bot in use.
  """

  def invoke(self) -> None:
    """Send a list of available CLI commands."""

    self.slack_bot.slack_client.send_message(
        f"Available Commands: {', '.join(self.slack_bot.command_list)}"
    )
