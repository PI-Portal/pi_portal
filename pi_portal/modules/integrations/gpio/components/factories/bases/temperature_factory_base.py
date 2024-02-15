"""GPIO temperature sensor factory base classes."""

import abc
from typing import Generic, Sequence, TypeVar

from pi_portal.modules.integrations.gpio.components.bases import (
    temperature_sensor_base,
)
from .sensor_factory_base import SensorFactoryBase

TypeHardware = TypeVar("TypeHardware")


class TemperatureSensorFactoryBase(
    SensorFactoryBase[
        temperature_sensor_base.TypeTemperatureData,
        TypeHardware,
    ],
    abc.ABC,
    Generic[TypeHardware],
):
  """Base factory for TemperatureSensorBase instances."""

  @abc.abstractmethod
  def create(
      self
  ) -> Sequence[temperature_sensor_base.TemperatureSensorBase[TypeHardware]]:
    """Override with creation logic."""
