"""SystemCallActionBase class."""

import abc
import os

from . import base_action


class SystemCallError(Exception):
  """Raised when a system call fails."""


class SystemCallActionBase(base_action.ActionBase, abc.ABC):
  """Generic installer action component supporting system calls."""

  def system_call(self, command: str) -> None:
    """Execute the specified command as a system call.

    :param command: The command to execute.
    """

    self.log.info("Executing: '%s' ...", command)
    result = os.system(command)  # nosec B605
    if result != 0:
      self.log.error("Command: '%s' failed!", command)
      raise SystemCallError(f"Command: '{command}' failed!")
