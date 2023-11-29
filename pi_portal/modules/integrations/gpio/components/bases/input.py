"""GPIOInputBase class."""

import abc
from typing import Any


class GPIOInputBase(abc.ABC):
  """GPIO input base representation.

  :param pin_number: The GPIO input number.
  :param pin_name: The name of this input in alerts and logs.
  :param initial_state: The value to initially set the state to.
  """

  pin_number: int
  pin_name: str
  current_state: Any
  last_state: Any

  def __init__(
      self, pin_number: int, pin_name: str, initial_state: Any
  ) -> None:
    self.pin_number = pin_number
    self.pin_name = pin_name
    self.last_state = None
    self.current_state = initial_state
    self.hook_setup_input()

  def poll(self) -> None:
    """Update the state of the GPIO input."""

    self.last_state = self.current_state
    self.current_state = self.hook_update_state()

  def has_changed(self) -> bool:
    """Query the state to see if it has changed since the last poll.

    :returns: A boolean indicating if the state has changed.
    """

    return bool(self.current_state != self.last_state)

  def hook_setup_input(self) -> None:
    """Override to initialize the GPIO input.  This is optional.

    :returns: The new GPIO state value.
    """

    return None  # pragma: no cover

  @abc.abstractmethod
  def hook_update_state(self) -> Any:
    """Override to return the current state of the GPIO Input.

    :returns: The new GPIO state value.
    """

    return None  # pragma: no cover

  @property
  def sensor_type(self) -> str:
    """Returns the name of the input type.
    The default behaviour is to return the implementation's class name.

    :returns: The inputs name.
    """
    return self.__class__.__name__
