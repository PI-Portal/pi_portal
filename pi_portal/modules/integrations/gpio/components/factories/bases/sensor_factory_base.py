"""GPIO sensor factory base classes."""

import abc
from typing import Generic, Sequence, TypeVar

from pi_portal.modules.integrations.gpio.components.bases import sensor_base
from .input_factory_base import GPIOInputFactoryBase

TypeState = TypeVar("TypeState")
TypeHardware = TypeVar("TypeHardware")


class SensorFactoryBase(
    GPIOInputFactoryBase[TypeState],
    abc.ABC,
    Generic[TypeState, TypeHardware],
):
  """Base factory for GPIOSensorBase instances."""

  @abc.abstractmethod
  def create(
      self
  ) -> Sequence[sensor_base.GPIOSensorBase[TypeState, TypeHardware]]:
    """Override with creation logic."""
