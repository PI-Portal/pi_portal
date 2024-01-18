"""Pi Portal base command class."""

import abc


class CommandBase(abc.ABC):
  """A generic, invokable command."""

  @abc.abstractmethod
  def invoke(self) -> None:
    """Invoke this command."""
