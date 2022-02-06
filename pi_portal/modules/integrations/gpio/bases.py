"""GPIO monitor factory base classes."""

import abc

from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.components.bases import monitor


class MonitorFactoryBase(abc.ABC):
  """Factory for GPIOMonitorBase instances."""

  def __init__(self) -> None:
    self.state = state.State()

  @abc.abstractmethod
  def create(self) -> monitor.GPIOMonitorBase:
    """Override with creation logic."""
