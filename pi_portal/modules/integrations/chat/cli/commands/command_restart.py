"""Chat CLI Restart command."""

from .bases.command import ChatCommandBase


class RestartCommand(ChatCommandBase):
  """Chat CLI command to restart the Bot process."""

  def invoke(self) -> None:
    """Restart the chat CLI bot."""

    self.chatbot.task_scheduler_client.chat_send_message("Rebooting myself ...")
    self.chatbot.halt()
