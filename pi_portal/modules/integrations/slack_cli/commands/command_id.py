"""Slack CLI ID command."""

from .bases.command import CommandBase


class IDCommand(CommandBase):
  """Command to report the unique ID the bot is running with."""

  def invoke(self) -> None:
    """Send the unique id for this bot's instance."""

    self.slack_client.send_message(f"ID: {self.slack_client.config.log_uuid}")
