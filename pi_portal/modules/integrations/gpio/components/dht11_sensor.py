"""DHT11 class."""

from typing import Any

from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor_base,
)
from pi_portal.modules.python.rpi import adafruit_dht, board


class DHT11(temperature_sensor_base.TemperatureSensorBase[adafruit_dht.DHT11]):
  """DHT11 Temperature Sensor class.

  :param: pin_number: The GPIO input number.
  :param pin_name: The name of this sensor in alerts and logs.
  """

  def hook_board_pin(self) -> Any:
    """Retrieve the hardware location of the GPIO pin.

    :returns: The hardware pin location.
    """
    return getattr(board, f"D{self.pin_number}")

  def hook_setup_hardware(self) -> adafruit_dht.DHT11:
    """Retrieve the adafruit_dht sensor object for the DHT11.

    :returns: The hardware sensor interface.
    """

    return adafruit_dht.DHT11(
        self.hook_board_pin(),
        use_pulseio=False,
    )

  def hook_update_state(
      self,
      retries: int = 3,
  ) -> temperature_sensor_base.TypeTemperatureData:
    """Retrieve new state for the GPIO input.
    :param retries: The number of times to retry a failed sensor reading.

    :returns: The new GPIO state value.
    """

    if retries < 1:
      return self.current_state

    try:
      temperature = self.hardware.temperature
      humidity = self.hardware.humidity
    except RuntimeError:
      return self.hook_update_state(retries - 1)

    return temperature_sensor_base.TypeTemperatureData(
        temperature=temperature,
        humidity=humidity,
    )
