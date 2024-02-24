"""CLI command to start the Slack bot."""

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.mixins import state
from pi_portal.modules.integrations.chat.service import ChatBot


class ChatBotCommand(
    command.CommandBase,
    state.CommandManagedStateMixin,
):
  """CLI command to start the Slack bot."""

  def invoke(self) -> None:
    """Invoke the command."""

    chatbot = ChatBot()
    chatbot.start()
