"""Slack CLI Help command."""

from pi_portal.modules.integrations.slack_cli import slack_cli
from .bases.command import CommandBase


class HelpCommand(CommandBase):
  """Slack CLI command to list the available commands."""

  def invoke(self) -> None:
    """Send a list of available CLI commands."""

    self.slack_client.send_message(
        f"Available Commands: {', '.join(slack_cli.get_available_commands())}"
    )
