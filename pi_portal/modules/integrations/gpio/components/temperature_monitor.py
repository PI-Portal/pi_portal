"""Temperature sensor monitor class."""

from typing import Sequence, cast

from pi_portal import config
from pi_portal.modules.integrations.gpio.components import dht11_sensor
from pi_portal.modules.integrations.gpio.components.bases import \
    input as gpio_input
from pi_portal.modules.integrations.gpio.components.bases import monitor


class TemperatureSensorMonitor(monitor.GPIOMonitorBase):
  """Temperature sensor monitor and logger.

  :param gpio_pins: A list of DHT11 sensors to monitor.
  """

  gpio_poll_interval = 60.0
  gpio_log_changes_only = False
  logger_name = "pi_portal_temperature"
  log_file_path = config.TEMPERATURE_MONITOR_LOGFILE_PATH

  def __init__(self, gpio_pins: Sequence[dht11_sensor.DHT11]) -> None:
    super().__init__(gpio_pins)

  def _setup_gpio(self) -> None:
    """Disabled for DHT sensors."""

  def hook_log_state(self, gpio_pin: gpio_input.GPIOInputBase) -> None:
    """Log customized messages when a state change is detected.

    :param gpio_pin: A GPIO pin to log an event for.
    """

    state = cast(dht11_sensor.TypeTemperatureData, gpio_pin.current_state)
    self.log.info(
        "DHT11:%s",
        gpio_pin.pin_name,
        extra={
            'sensor_name': gpio_pin.pin_name,
            'temperature': state["temperature"],
            'humidity': state["humidity"],
        }
    )
