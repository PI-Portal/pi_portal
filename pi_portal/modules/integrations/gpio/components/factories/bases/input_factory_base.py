"""GPIOInputBase factory base class."""

import abc
from typing import Generic, Sequence, TypeVar

from pi_portal.modules.configuration import state
from pi_portal.modules.integrations.gpio.components.bases import input_base

TypeState = TypeVar("TypeState")


class GPIOInputFactoryBase(abc.ABC, Generic[TypeState]):
  """Base factory for GPIOInputBase instances."""

  def __init__(self) -> None:
    self.state = state.State()

  @abc.abstractmethod
  def create(self) -> Sequence[input_base.GPIOInputBase[TypeState]]:
    """Override with creation logic."""
