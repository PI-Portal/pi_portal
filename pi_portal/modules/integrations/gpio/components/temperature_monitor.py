"""Temperature sensor monitor class."""

from typing import Sequence

from pi_portal import config
from pi_portal.modules.integrations.gpio.components.bases import (
    monitor,
    temperature_sensor,
)


class TemperatureSensorMonitor(
    monitor.GPIOMonitorBase[temperature_sensor.TemperatureSensor]
):
  """Temperature sensor monitor and logger.

  :param gpio_pins: A list of DHT11 sensors to monitor.
  """

  gpio_poll_interval = 60.0
  gpio_log_changes_only = False
  logger_name = "pi_portal_temperature"
  log_file_path = config.TEMPERATURE_MONITOR_LOGFILE_PATH

  def __init__(
      self, gpio_pins: Sequence[temperature_sensor.TemperatureSensor]
  ) -> None:
    super().__init__(gpio_pins)

  def _setup_gpio(self) -> None:
    """Disabled for DHT sensors."""

  def hook_log_state(
      self, gpio_pin: temperature_sensor.TemperatureSensor
  ) -> None:
    """Log customized messages when a state change is detected.

    :param gpio_pin: A GPIO pin to log an event for.
    """

    self.log.info(
        "TemperatureSensor:%s",
        gpio_pin.pin_name,
        extra={
            'sensor_type': gpio_pin.sensor_type,
            'sensor_name': gpio_pin.pin_name,
            'temperature': gpio_pin.current_state["temperature"],
            'humidity': gpio_pin.current_state["humidity"],
        }
    )
