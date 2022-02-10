"""DHT11 class."""

from typing import Any, Optional

from pi_portal.modules.integrations.gpio.components.bases import \
    sensor as gpio_sensor
from pi_portal.modules.integrations.gpio.shim import adafruit_dht, board
from typing_extensions import TypedDict


class TypeTemperatureData(TypedDict):
  """Typed representation of temperature sensor data."""

  temperature: Optional[float]
  humidity: Optional[float]


EMPTY_READING = TypeTemperatureData(temperature=None, humidity=None)


class DHT11(gpio_sensor.GPIOSensorBase):
  """DHT11 Temperature Sensor class.

  :param pin_number: The GPIO input number.
  :param pin_name: The name of this door in alerts and logs.
  """

  def __init__(
      self,
      pin_number: int,
      pin_name: str,
  ) -> None:
    super().__init__(pin_number, pin_name, EMPTY_READING)

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

  def hook_update_state(self) -> Any:
    """Retrieve new state for the GPIO input.

    :returns: The new GPIO state value.
    :raises: RuntimeError
    """

    try:
      temperature = self.hardware.temperature
      humidity = self.hardware.humidity
    except RuntimeError:
      return self.current_state

    return TypeTemperatureData(
        temperature=temperature,
        humidity=humidity,
    )
