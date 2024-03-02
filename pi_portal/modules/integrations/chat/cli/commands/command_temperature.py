"""Chat CLI Temperature command."""

from .bases.command import ChatCommandBase


class TemperatureCommand(ChatCommandBase):
  """Chat CLI command to show the last known temperature sensor values."""

  def invoke(self) -> None:
    """Report the last known temperature sensor values."""

    self.chatbot.task_scheduler_client.chat_send_temperature_reading()
