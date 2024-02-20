"""Chat CLI Restart command."""

import os
from typing import Callable, cast

from .bases.command import ChatCommandBase


class RestartCommand(ChatCommandBase):
  """Chat CLI command to restart the Bot process."""

  def invoke(self) -> None:
    """Restart the chat CLI bot."""

    self.chatbot.chat_client.send_message("Rebooting myself ...")
    # BaseSocketModeHandler is untyped
    close = cast(Callable[[], None], self.chatbot.web_socket.close)
    close()
    os._exit(1)  # pylint: disable=protected-access
