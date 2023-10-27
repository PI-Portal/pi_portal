"""GPIO sensor factory base classes."""

import abc
from typing import Sequence

from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.components.bases import sensor


class SensorFactoryBase(abc.ABC):
  """Factory for GPIOSensorBase instances."""

  def __init__(self) -> None:
    self.state = state.State()

  @abc.abstractmethod
  def create(self) -> Sequence[sensor.GPIOSensorBase]:
    """Override with creation logic."""
