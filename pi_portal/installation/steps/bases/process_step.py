"""ProcessStepBase class."""
import abc
import logging

from pi_portal.modules.system import process
from . import base_step


class ProcessStepBase(base_step.StepBase, abc.ABC):
  """Process management installer step."""

  pid_file_path: str
  process: process.Process

  def __init__(
      self,
      log: logging.Logger,
      pid_file_path: str,
  ) -> None:
    super().__init__(log)
    self.pid_file_path = pid_file_path
    self.process = process.Process(pid_file_location=pid_file_path)
