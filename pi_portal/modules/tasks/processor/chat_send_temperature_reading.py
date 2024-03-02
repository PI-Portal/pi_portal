"""Processes requests to send the latest temperature reading via chat."""

from typing import List

from pi_portal.modules.integrations.log_file import temperature_monitor_logfile
from pi_portal.modules.tasks.enums import TaskType
from pi_portal.modules.tasks.processor.bases import processor_base
from pi_portal.modules.tasks.processor.mixins import chat_client
from pi_portal.modules.tasks.task import chat_send_temperature_reading


class ProcessorClass(
    chat_client.ChatClientMixin,
    processor_base.TaskProcessorBase[
        chat_send_temperature_reading.Args,
        chat_send_temperature_reading.ReturnType,
    ],
):
  """Processes requests to send the latest temperature reading via chat."""

  __slots__ = ()

  no_sensors_configured_message = "No sensors configured."
  no_measurement_message = "not yet measured"
  type = TaskType.CHAT_SEND_TEMPERATURE_READING

  def _process(
      self,
      task: processor_base.TaskBase[
          chat_send_temperature_reading.Args,
          chat_send_temperature_reading.ReturnType,
      ],
  ) -> chat_send_temperature_reading.ReturnType:

    multiline_message: List[str] = [task.args.header]

    reader = temperature_monitor_logfile.TemperatureMonitorLogFileReader()

    if reader.configured_sensor_count > 0:
      temperature_readings = reader.read_last_values()
      for sensor in temperature_readings.values():
        for name, reading in sensor.items():
          message_line = f"{name}: "
          if reading['temperature'] and reading['humidity']:
            message_line += f"{reading['temperature']}°C, "
            message_line += f"{reading['humidity']}% humidity"
          else:
            message_line += self.no_measurement_message
          multiline_message.append(message_line)
    else:
      multiline_message.append(self.no_sensors_configured_message)

    self.client.send_message("\n".join(multiline_message))
