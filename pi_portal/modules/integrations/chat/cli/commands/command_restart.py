"""Chat CLI Restart command."""

from .bases.command import ChatCommandBase


class RestartCommand(ChatCommandBase):
  """Chat CLI command to restart the Bot process."""

  def invoke(self) -> None:
    """Restart the chat CLI bot."""

    self.chatbot.chat_client.send_message("Rebooting myself ...")
    self.chatbot.halt()
