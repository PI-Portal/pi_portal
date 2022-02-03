"""Slack CLI Help command."""

from pi_portal.modules.integrations.slack import cli
from .bases.command import SlackCommandBase


class HelpCommand(SlackCommandBase):
  """Slack CLI command to list the available commands.

  :param client: The configured slack client to use.
  """

  def invoke(self) -> None:
    """Send a list of available CLI commands."""

    self.slack_client.send_message(
        f"Available Commands: {', '.join(cli.get_available_commands())}"
    )
