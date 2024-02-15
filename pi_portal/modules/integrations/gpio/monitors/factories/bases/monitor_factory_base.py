"""GPIO monitor factory base classes."""

import abc
from typing import Generic

from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.monitors.bases import monitor_base
from pi_portal.modules.integrations.gpio.monitors.bases.monitor_base import (
    TypeGenericGpio,
)


class MonitorFactoryBase(abc.ABC, Generic[TypeGenericGpio]):
  """Abstract factory for GPIOMonitorBase instances."""

  def __init__(self) -> None:
    self.state = state.State()

  @abc.abstractmethod
  def create(self) -> "monitor_base.GPIOMonitorBase[TypeGenericGpio]":
    """Override with creation logic."""
