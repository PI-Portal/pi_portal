"""StepBase class."""

import abc
import os

from . import base_step


class SystemCallError(Exception):
  """Raised when a system call fails."""


class SystemCallBase(base_step.StepBase, abc.ABC):
  """System call installer step."""

  def _system_call(self, command: str) -> None:
    self.log.info("Executing: '%s' ...", command)
    result = os.system(command)  # nosec B605
    if result != 0:
      self.log.error("Command: '%s' failed!", command)
      raise SystemCallError(f"Command: '{command}' failed!")
