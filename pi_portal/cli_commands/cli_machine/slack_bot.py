"""CLI command to start the Slack bot."""

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.mixins import state
from pi_portal.modules.integrations import slack


class SlackBotCommand(
    command.CommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to start the Slack bot."""

  def invoke(self) -> None:
    """Invoke the command."""

    slack_bot = slack.SlackBot()
    slack_bot.connect()
