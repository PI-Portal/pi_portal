"""GPIOSensorBase class."""

import abc
from typing import Any, Generic, TypeVar

from . import input_base as gpio_input

TypeState = TypeVar("TypeState")
TypeHardware = TypeVar("TypeHardware")
TypeGenericHardware = Any


class GPIOSensorBase(
    gpio_input.GPIOInputBase[TypeState],
    abc.ABC,
    Generic[TypeState, TypeHardware],
):
  """GPIO sensor base representation.

  :param pin_number: The GPIO input number.
  :param pin_name: The name of this input in alerts and logs.
  :param initial_state: The value to initially set the state to.
  """

  hardware: TypeHardware

  def __init__(
      self, pin_number: int, pin_name: str, initial_state: TypeState
  ) -> None:
    super().__init__(pin_number, pin_name, initial_state)
    self.hardware = self.hook_setup_hardware()

  @abc.abstractmethod
  def hook_setup_hardware(self) -> TypeHardware:
    """Override to return the hardware sensor that can be used during polling.

    :returns: A pollable hardware interface.
    """

    return None  # type: ignore[return-value]  # pragma:  no cover
