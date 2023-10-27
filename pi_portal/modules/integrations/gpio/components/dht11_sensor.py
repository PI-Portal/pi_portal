"""DHT11 class."""

from typing import Any

from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor,
)
from pi_portal.modules.integrations.gpio.shim import adafruit_dht, board


class DHT11(temperature_sensor.TemperatureSensor):
  """DHT11 Temperature Sensor class.

  :param: pin_number: The GPIO input number.
  :param pin_name: The name of this door in alerts and logs.
  """

  def hook_board_pin(self) -> Any:
    """Retrieve the hardware location of the GPIO pin.

    :returns: The hardware pin location.
    """
    return getattr(board, f"D{self.pin_number}")

  def hook_setup_hardware(self) -> Any:
    """Retrieve the adafruit_dht sensor object for the DHT11.

    :returns: The hardware sensor interface.
    """

    return adafruit_dht.DHT11(  # type: ignore[attr-defined]
      self.hook_board_pin(),
      use_pulseio=False,
    )

  def hook_update_state(
      self, retries: int = 3
  ) -> temperature_sensor.TypeTemperatureData:
    """Retrieve new state for the GPIO input.
    :param retries: The number of times to retry a failed sensor reading.

    :returns: The new GPIO state value.
    :raises: RuntimeError
    """

    if retries < 1:
      return self.current_state

    try:
      temperature = self.hardware.temperature
      humidity = self.hardware.humidity
    except RuntimeError:
      return self.hook_update_state(retries - 1)

    return temperature_sensor.TypeTemperatureData(
        temperature=temperature,
        humidity=humidity,
    )
