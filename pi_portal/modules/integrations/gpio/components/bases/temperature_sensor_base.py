"""TemperatureSensor class."""

import abc
from typing import Generic, Optional, TypeVar

from pi_portal.modules.integrations.gpio.components.bases import sensor_base
from typing_extensions import TypeAlias, TypedDict

TypeHardware = TypeVar("TypeHardware")
TypeGenericTemperateSensor: TypeAlias = (
    "TemperatureSensorBase[sensor_base.TypeGenericHardware]"
)


class TypeTemperatureData(TypedDict):
  """Typed representation of temperature sensor data."""

  temperature: Optional[float]
  humidity: Optional[float]


EMPTY_READING = TypeTemperatureData(temperature=None, humidity=None)


class TemperatureSensorBase(
    sensor_base.GPIOSensorBase[TypeTemperatureData, TypeHardware],
    abc.ABC,
    Generic[TypeHardware],
):
  """TemperatureSensor Temperature Sensor class.

  :param pin_number: The GPIO input number.
  :param pin_name: The name of this sensor in alerts and logs.
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
    """

    return EMPTY_READING  # pragma: no cover
