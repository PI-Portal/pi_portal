"""GPIOSensorBase class."""

import abc
from typing import Any

from . import input as gpio_input


class GPIOSensorBase(gpio_input.GPIOInputBase, abc.ABC):
  """GPIO sensor base representation.

  :param pin_number: The GPIO input number.
  :param pin_name: The name of this input in alerts and logs.
  :param initial_state: The value to initially set the state to.
  """

  pin_number: int
  pin_name: str
  current_state: Any
  last_state: Any
  hardware: Any

  def __init__(
      self, pin_number: int, pin_name: str, initial_state: Any
  ) -> None:
    super().__init__(pin_number, pin_name, initial_state)
    self.hardware = self.hook_setup_hardware()

  @abc.abstractmethod
  def hook_setup_hardware(self) -> Any:
    """Override to return the hardware sensor that can be used during polling.

    :returns: A pollable hardware interface.
    """

    return None  # pragma: no cover
