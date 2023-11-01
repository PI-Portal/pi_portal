"""GPIO monitor factory base classes."""

import abc
from typing import Generic

from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.components.bases import monitor
from pi_portal.modules.integrations.gpio.components.bases.monitor import (
    TypeGenericGpio,
)


class MonitorFactoryBase(abc.ABC, Generic[TypeGenericGpio]):
  """Factory for GPIOMonitorBase instances."""

  def __init__(self) -> None:
    self.state = state.State()

  @abc.abstractmethod
  def create(self) -> monitor.GPIOMonitorBase[TypeGenericGpio]:
    """Override with creation logic."""
