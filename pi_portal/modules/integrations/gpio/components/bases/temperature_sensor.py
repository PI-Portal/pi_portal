"""TemperatureSensor class."""

import abc
from typing import Optional

from pi_portal.modules.integrations.gpio.components.bases import \
    sensor as gpio_sensor
from typing_extensions import TypedDict


class TypeTemperatureData(TypedDict):
  """Typed representation of temperature sensor data."""

  temperature: Optional[float]
  humidity: Optional[float]


EMPTY_READING = TypeTemperatureData(temperature=None, humidity=None)


class TemperatureSensor(gpio_sensor.GPIOSensorBase, abc.ABC):
  """TemperatureSensor Temperature Sensor class.

  :param pin_number: The GPIO input number.
  :param pin_name: The name of this door in alerts and logs.
  """

  current_state: TypeTemperatureData

  def __init__(
      self,
      pin_number: int,
      pin_name: str,
  ) -> None:
    super().__init__(pin_number, pin_name, EMPTY_READING)

  @abc.abstractmethod
  def hook_update_state(self) -> TypeTemperatureData:
    """Retrieve new state for the GPIO input.

    :returns: The new GPIO state value.
    :raises: RuntimeError
    """
    return EMPTY_READING  # pragma: no cover
