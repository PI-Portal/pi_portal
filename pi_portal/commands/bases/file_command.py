"""Pi Portal file command base class."""

import abc

from . import command


class FileCommandBase(command.CommandBase, abc.ABC):
  """An generic, invokable command.

  :param file_name: The path to a valid filename.
  """

  def __init__(self, file_name: str) -> None:
    self.file_name = file_name
