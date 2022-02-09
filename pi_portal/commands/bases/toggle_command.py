"""Pi Portal toggle command base class."""

import abc

from . import command


class ToggleCommandBase(command.CommandBase, abc.ABC):
  """An generic, invokable command.

  :param toggle: A boolean to toggle a feature on or off.
  """

  def __init__(self, toggle: bool) -> None:
    self.toggle = toggle
