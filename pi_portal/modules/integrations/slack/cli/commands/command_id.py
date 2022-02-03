"""Slack CLI ID command."""

from pi_portal.modules.configuration import state
from .bases.command import SlackCommandBase


class IDCommand(SlackCommandBase):
  """Command to report the unique ID the bot is running with.

  :param client: The configured slack client to use.
  """

  def invoke(self) -> None:
    """Send the unique id for this bot's instance."""

    running_state = state.State()
    self.slack_client.send_message(f"ID: {running_state.log_uuid}")