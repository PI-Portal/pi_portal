"""CLI command to start the Slack bot."""

from pi_portal.modules.integrations import slack
from .bases import command


class SlackBotCommand(command.CommandBase):
  """CLI command to start the Slack bot."""

  def invoke(self) -> None:
    """Invoke the command."""

    slack_bot = slack.SlackBot()
    slack_bot.connect()
