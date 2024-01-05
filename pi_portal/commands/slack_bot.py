"""CLI command to start the Slack bot."""

from pi_portal.modules.integrations import slack
from .bases import command
from .mixins import state


class SlackBotCommand(
    command.CommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to start the Slack bot."""

  def invoke(self) -> None:
    """Invoke the command."""

    slack_bot = slack.SlackBot()
    slack_bot.connect()
