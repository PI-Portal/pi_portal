"""Chat CLI ID command."""

from pi_portal.modules.configuration import state
from .bases.command import ChatCommandBase


class IDCommand(ChatCommandBase):
  """Chat CLI command to report the unique ID the bot is running with."""

  def invoke(self) -> None:
    """Send the unique id for this bot's instance."""

    running_state = state.State()
    self.chatbot.task_scheduler_client.chat_send_message(
        f"ID: {running_state.log_uuid}"
    )
