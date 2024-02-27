"""CLI command to start the Slack bot."""

from pi_portal.cli_commands.bases import command
from pi_portal.cli_commands.mixins import require_task_scheduler, state
from pi_portal.modules.integrations.chat.service import ChatBot


class ChatBotCommand(
    require_task_scheduler.CommandTaskSchedulerMixin,
    state.CommandManagedStateMixin,
    command.CommandBase,
):
  """CLI command to start the Slack bot."""

  def invoke(self) -> None:
    """Invoke the command."""

    self.require_task_scheduler()

    chatbot = ChatBot()
    chatbot.start()
