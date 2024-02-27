"""Chat CLI Temperature command."""

from typing import List

from pi_portal.modules.integrations.log_file import temperature_monitor_logfile
from .bases.command import ChatCommandBase


class TemperatureCommand(ChatCommandBase):
  """Chat CLI command to show the last known temperature sensor values."""

  def invoke(self) -> None:
    """Report the last known temperature sensor values."""

    multiline_message: List[str] = ["No sensors configured."]

    reader = temperature_monitor_logfile.TemperatureMonitorLogFileReader()

    if reader.configured_sensor_count > 0:
      multiline_message = []
      temperature_readings = reader.read_last_values()
      for sensor in temperature_readings.values():
        for name, reading in sensor.items():
          message_line = f"{name}: "
          if reading['temperature'] and reading['humidity']:
            message_line += f"{reading['temperature']}°C, "
            message_line += f"{reading['humidity']}% humidity"
          else:
            message_line += "not yet measured"
          multiline_message.append(message_line)

    self.chatbot.task_scheduler_client.chat_send_message(
        "\n".join(multiline_message)
    )
