"""Chat CLI Help command."""

from .bases.command import ChatCommandBase


class HelpCommand(ChatCommandBase):
  """Chat CLI command to list the available commands."""

  def invoke(self) -> None:
    """Send a list of available CLI commands."""

    self.chatbot.task_scheduler_client.chat_send_message(
        f"Available Commands: {', '.join(self.chatbot.command_list)}"
    )
