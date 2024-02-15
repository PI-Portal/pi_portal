"""Temperature sensor monitor class."""

from typing import Sequence

from pi_portal import config
from pi_portal.modules.integrations.gpio.monitors.bases import monitor_base
from ..components.bases.temperature_sensor_base import (
    TypeGenericTemperateSensor,
)


class TemperatureSensorMonitor(
    monitor_base.GPIOMonitorBase[TypeGenericTemperateSensor],
):
  """Temperature sensor monitor and logger.

  :param gpio_pins: A list of temperature sensors to monitor.
  """

  gpio_poll_interval = 60.0
  gpio_log_changes_only = False
  logger_name = "temperature"
  log_file_path = config.LOG_FILE_TEMPERATURE_MONITOR

  def __init__(
      self,
      gpio_pins: Sequence[TypeGenericTemperateSensor],
  ) -> None:
    super().__init__(gpio_pins)

  def _setup_gpio(self) -> None:
    """Disabled for currently supported sensors."""

  def hook_log_state(
      self,
      gpio_pin: TypeGenericTemperateSensor,
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
